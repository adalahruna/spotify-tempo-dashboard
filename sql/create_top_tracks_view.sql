-- ============================================
-- CREATE TOP TRACKS MATERIALIZED VIEW
-- ============================================
-- Purpose: Pre-compute popular tracks with popularity score
-- Benefits: Fast queries, accurate results, easy maintenance
-- Author: Dashboard Team
-- Date: 2024

-- Drop existing view if exists
DROP MATERIALIZED VIEW IF EXISTS top_tracks_view CASCADE;

-- Create materialized view with popularity scoring
CREATE MATERIALIZED VIEW top_tracks_view AS
WITH popular_artists AS (
    -- Define list of popular/mainstream artists
    SELECT unnest(ARRAY[
        'Drake', 'Taylor Swift', 'Ed Sheeran', 'The Weeknd', 'Ariana Grande',
        'Post Malone', 'Billie Eilish', 'Justin Bieber', 'Dua Lipa', 'Harry Styles',
        'Bruno Mars', 'Daft Punk', 'Calvin Harris', 'Rihanna', 'Beyoncé',
        'Adele', 'Coldplay', 'Maroon 5', 'Imagine Dragons', 'OneRepublic',
        'Sia', 'Katy Perry', 'Lady Gaga', 'Sam Smith', 'Shawn Mendes',
        'Khalid', 'Halsey', 'Camila Cabello', 'Olivia Rodrigo', 'BTS',
        'Bad Bunny', 'J Balvin', 'The Chainsmokers', 'Marshmello', 'David Guetta',
        'Avicii', 'Martin Garrix', 'Zedd', 'Kygo', 'Ellie Goulding',
        'Miley Cyrus', 'Selena Gomez', 'Jonas Brothers', 'Charlie Puth', 'Troye Sivan',
        'Lewis Capaldi', 'Lizzo', 'Doja Cat', 'SZA', 'Lil Nas X'
    ]) AS artist_name
),
artist_matches AS (
    -- Find tracks from popular artists with stricter matching
    SELECT DISTINCT ON (t.id)
        t.*,
        pa.artist_name as matched_artist
    FROM spotify_tracks_raw t
    CROSS JOIN popular_artists pa
    WHERE 
        -- Multiple conditions for better matching
        (
            -- Exact match
            LOWER(t.artists) = LOWER(pa.artist_name)
            OR
            -- Starts with artist name + separator
            LOWER(t.artists) LIKE LOWER(pa.artist_name) || ',%'
            OR
            LOWER(t.artists) LIKE LOWER(pa.artist_name) || ';%'
            OR
            -- Artist is in a list (with separators)
            LOWER(t.artists) LIKE '%,' || LOWER(pa.artist_name) || ',%'
            OR
            LOWER(t.artists) LIKE '%,' || LOWER(pa.artist_name)
            OR
            -- Bracket notation: ['Artist Name']
            LOWER(t.artists) LIKE '%[''''' || LOWER(pa.artist_name) || ''''']%'
        )
        AND t.year >= 2010
        AND t.year <= 2024
        AND t.danceability > 0.5
        AND t.energy > 0.4
        AND t.valence > 0.2
        AND t.instrumentalness < 0.5
        AND t.speechiness < 0.4
        AND t.acousticness < 0.7
        AND t.duration_ms BETWEEN 120000 AND 360000
        AND t.tempo BETWEEN 60 AND 200
        -- Filter out non-English tracks (Cyrillic, Chinese, Japanese, Korean)
        AND NOT (t.name ~ '[А-Яа-яЁё]')
        AND NOT (t.name ~ '[一-龥]')
        AND NOT (t.name ~ '[ぁ-ん]')
        AND NOT (t.name ~ '[가-힣]')
        -- Also filter by track name - must have mostly ASCII characters
        AND LENGTH(t.name) > 2
        AND LENGTH(REGEXP_REPLACE(t.name, '[^A-Za-z0-9 ]', '', 'g')) > LENGTH(t.name) * 0.3
)
SELECT 
    id,
    name,
    artists,
    year,
    tempo,
    danceability,
    energy,
    valence,
    acousticness,
    instrumentalness,
    liveness,
    speechiness,
    loudness,
    duration_ms,
    matched_artist,
    -- Tempo zone classification
    CASE 
        WHEN tempo >= 100 AND tempo < 120 THEN 'sweet_spot'
        WHEN tempo < 80 THEN 'slow'
        WHEN tempo >= 80 AND tempo < 100 THEN 'moderate'
        WHEN tempo >= 120 AND tempo < 140 THEN 'upbeat'
        ELSE 'fast'
    END as tempo_zone,
    -- Boolean for sweet spot
    CASE 
        WHEN tempo >= 100 AND tempo < 120 THEN true
        ELSE false
    END as in_sweet_spot,
    -- Popularity score calculation
    (
        danceability * 0.35 +           -- Dance appeal (35%)
        energy * 0.30 +                 -- Energy level (30%)
        valence * 0.15 +                -- Mood positivity (15%)
        (1 - acousticness) * 0.10 +     -- Production quality (10%)
        (year - 2010) / 14.0 * 0.10     -- Recency factor (10%)
    ) as popularity_score,
    -- Hit potential score (for ML features)
    (
        POWER(danceability * energy, 0.5) * 0.6 +
        valence * 0.2 +
        (1 - instrumentalness) * 0.2
    ) as hit_potential
FROM artist_matches
ORDER BY popularity_score DESC;

-- Create indexes for performance
CREATE INDEX idx_top_tracks_popularity ON top_tracks_view(popularity_score DESC);
CREATE INDEX idx_top_tracks_year ON top_tracks_view(year DESC);
CREATE INDEX idx_top_tracks_tempo ON top_tracks_view(tempo);
CREATE INDEX idx_top_tracks_dance ON top_tracks_view(danceability DESC);
CREATE INDEX idx_top_tracks_energy ON top_tracks_view(energy DESC);
CREATE INDEX idx_top_tracks_artist ON top_tracks_view(matched_artist);
CREATE INDEX idx_top_tracks_zone ON top_tracks_view(tempo_zone);
CREATE INDEX idx_top_tracks_sweet_spot ON top_tracks_view(in_sweet_spot) WHERE in_sweet_spot = true;

-- Create GIN index for text search
CREATE INDEX idx_top_tracks_name_gin ON top_tracks_view USING gin(to_tsvector('english', name));
CREATE INDEX idx_top_tracks_artists_gin ON top_tracks_view USING gin(to_tsvector('english', artists));

-- Grant permissions
GRANT SELECT ON top_tracks_view TO PUBLIC;

-- Add comments for documentation
COMMENT ON MATERIALIZED VIEW top_tracks_view IS 'Pre-computed top tracks from popular artists (2010-2024) with popularity scoring';
COMMENT ON COLUMN top_tracks_view.popularity_score IS 'Composite score: dance(35%) + energy(30%) + valence(15%) + production(10%) + recency(10%)';
COMMENT ON COLUMN top_tracks_view.hit_potential IS 'Viral potential score based on danceability, energy, and valence';
COMMENT ON COLUMN top_tracks_view.matched_artist IS 'Which popular artist matched (for filtering)';

-- Refresh strategy (run periodically)
-- REFRESH MATERIALIZED VIEW CONCURRENTLY top_tracks_view;

-- Stats
SELECT 
    COUNT(*) as total_tracks,
    COUNT(DISTINCT matched_artist) as unique_artists,
    MIN(year) as earliest_year,
    MAX(year) as latest_year,
    ROUND(AVG(popularity_score)::numeric, 3) as avg_popularity,
    COUNT(*) FILTER (WHERE in_sweet_spot) as sweet_spot_tracks
FROM top_tracks_view;

-- Sample top 10
SELECT 
    name,
    matched_artist as artist,
    year,
    ROUND(tempo::numeric, 1) as tempo,
    ROUND(popularity_score::numeric, 3) as score
FROM top_tracks_view
ORDER BY popularity_score DESC
LIMIT 10;
