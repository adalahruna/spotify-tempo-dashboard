-- ============================================
-- TEST QUERIES FOR RECOMMENDATION SYSTEM
-- Database: spotify_music_db (1,204,025 tracks)
-- ============================================

-- TEST 1: Happy/Upbeat Songs
-- ============================================
SELECT 'TEST 1: Happy/Upbeat Songs' as test_name;
SELECT name, artists, tempo, valence, energy, danceability
FROM spotify_tracks_raw
WHERE 
    valence > 0.6 
    AND energy > 0.6
    AND tempo BETWEEN 100 AND 140
    AND danceability > 0.5
ORDER BY valence DESC, energy DESC
LIMIT 10;

SELECT COUNT(*) as total_happy_tracks
FROM spotify_tracks_raw
WHERE valence > 0.6 AND energy > 0.6;

-- TEST 2: Sad/Melancholic Songs
-- ============================================
SELECT 'TEST 2: Sad/Melancholic Songs' as test_name;
SELECT name, artists, tempo, valence, energy, acousticness
FROM spotify_tracks_raw
WHERE 
    valence < 0.4
    AND energy < 0.4
    AND tempo BETWEEN 60 AND 100
ORDER BY valence ASC, acousticness DESC
LIMIT 10;

SELECT COUNT(*) as total_sad_tracks
FROM spotify_tracks_raw
WHERE valence < 0.4 AND energy < 0.4;

-- TEST 3: Workout/Gym Songs
-- ============================================
SELECT 'TEST 3: Workout/Gym Songs' as test_name;
SELECT name, artists, tempo, energy, danceability, loudness
FROM spotify_tracks_raw
WHERE 
    energy > 0.7
    AND tempo BETWEEN 120 AND 180
    AND danceability > 0.6
ORDER BY energy DESC, tempo DESC
LIMIT 10;

SELECT COUNT(*) as total_workout_tracks
FROM spotify_tracks_raw
WHERE energy > 0.7 AND tempo BETWEEN 120 AND 180;

-- TEST 4: Study/Focus Songs
-- ============================================
SELECT 'TEST 4: Study/Focus Songs' as test_name;
SELECT name, artists, tempo, energy, instrumentalness, speechiness
FROM spotify_tracks_raw
WHERE 
    energy < 0.4
    AND instrumentalness > 0.5
    AND speechiness < 0.1
    AND tempo BETWEEN 70 AND 110
ORDER BY instrumentalness DESC
LIMIT 10;

SELECT COUNT(*) as total_focus_tracks
FROM spotify_tracks_raw
WHERE energy < 0.4 AND instrumentalness > 0.5;

-- TEST 5: Relaxation Songs
-- ============================================
SELECT 'TEST 5: Relaxation/Sleep Songs' as test_name;
SELECT name, artists, tempo, energy, acousticness, loudness
FROM spotify_tracks_raw
WHERE 
    energy < 0.3
    AND acousticness > 0.6
    AND tempo BETWEEN 60 AND 90
ORDER BY energy ASC, tempo ASC
LIMIT 10;

SELECT COUNT(*) as total_relax_tracks
FROM spotify_tracks_raw
WHERE energy < 0.3 AND acousticness > 0.6;

-- TEST 6: Party/Dance Songs
-- ============================================
SELECT 'TEST 6: Party/Dance Songs' as test_name;
SELECT name, artists, tempo, energy, danceability, valence
FROM spotify_tracks_raw
WHERE 
    energy > 0.7
    AND danceability > 0.7
    AND valence > 0.6
    AND tempo BETWEEN 110 AND 130
ORDER BY danceability DESC, energy DESC
LIMIT 10;

SELECT COUNT(*) as total_party_tracks
FROM spotify_tracks_raw
WHERE energy > 0.7 AND danceability > 0.7 AND tempo BETWEEN 110 AND 130;

-- TEST 7: Tempo Similarity (Shape of You = 96 BPM)
-- ============================================
SELECT 'TEST 7: Similar Tempo to Shape of You (96 BPM)' as test_name;
SELECT name, artists, tempo, danceability, energy,
       ABS(tempo - 96) as tempo_diff
FROM spotify_tracks_raw
WHERE 
    tempo BETWEEN 90 AND 102
    AND danceability > 0.6
ORDER BY ABS(tempo - 96) ASC
LIMIT 10;

-- TEST 8: Sweet Spot Analysis
-- ============================================
SELECT 'TEST 8: Sweet Spot (100-120 BPM) Distribution' as test_name;
SELECT 
    CASE 
        WHEN tempo < 80 THEN 'Very Slow (<80)'
        WHEN tempo BETWEEN 80 AND 100 THEN 'Slow (80-100)'
        WHEN tempo BETWEEN 100 AND 120 THEN '★ Sweet Spot (100-120)'
        WHEN tempo BETWEEN 120 AND 140 THEN 'Fast (120-140)'
        ELSE 'Very Fast (>140)'
    END as tempo_zone,
    COUNT(*) as track_count,
    ROUND(AVG(danceability)::numeric, 3) as avg_danceability,
    ROUND(AVG(energy)::numeric, 3) as avg_energy,
    ROUND(AVG(valence)::numeric, 3) as avg_valence
FROM spotify_tracks_raw
GROUP BY 
    CASE 
        WHEN tempo < 80 THEN 1
        WHEN tempo BETWEEN 80 AND 100 THEN 2
        WHEN tempo BETWEEN 100 AND 120 THEN 3
        WHEN tempo BETWEEN 120 AND 140 THEN 4
        ELSE 5
    END,
    CASE 
        WHEN tempo < 80 THEN 'Very Slow (<80)'
        WHEN tempo BETWEEN 80 AND 100 THEN 'Slow (80-100)'
        WHEN tempo BETWEEN 100 AND 120 THEN '★ Sweet Spot (100-120)'
        WHEN tempo BETWEEN 120 AND 140 THEN 'Fast (120-140)'
        ELSE 'Very Fast (>140)'
    END
ORDER BY 
    CASE 
        WHEN tempo < 80 THEN 1
        WHEN tempo BETWEEN 80 AND 100 THEN 2
        WHEN tempo BETWEEN 100 AND 120 THEN 3
        WHEN tempo BETWEEN 120 AND 140 THEN 4
        ELSE 5
    END;

-- TEST 9: Advanced Scoring (Running at 140 BPM)
-- ============================================
SELECT 'TEST 9: Smart Recommendation - Running at 140 BPM' as test_name;
SELECT 
    name, 
    artists, 
    tempo, 
    energy, 
    valence,
    danceability,
    ROUND(
        (
            (1 - ABS(tempo - 140) / 100.0) * 0.4 +
            energy * 0.3 +
            valence * 0.2 +
            danceability * 0.1
        )::numeric, 
        3
    ) as relevance_score
FROM spotify_tracks_raw
WHERE 
    tempo BETWEEN 130 AND 150
    AND energy > 0.6
    AND valence > 0.5
ORDER BY relevance_score DESC
LIMIT 10;

-- TEST 10: Data Coverage Check
-- ============================================
SELECT 'TEST 10: Data Quality & Coverage' as test_name;
SELECT 
    COUNT(*) as total_tracks,
    COUNT(CASE WHEN valence IS NOT NULL THEN 1 END) as has_valence,
    COUNT(CASE WHEN energy IS NOT NULL THEN 1 END) as has_energy,
    COUNT(CASE WHEN tempo IS NOT NULL THEN 1 END) as has_tempo,
    COUNT(CASE WHEN danceability IS NOT NULL THEN 1 END) as has_danceability,
    COUNT(CASE WHEN acousticness IS NOT NULL THEN 1 END) as has_acousticness,
    COUNT(CASE WHEN instrumentalness IS NOT NULL THEN 1 END) as has_instrumentalness,
    ROUND(AVG(valence)::numeric, 3) as avg_valence,
    ROUND(AVG(energy)::numeric, 3) as avg_energy,
    ROUND(AVG(tempo)::numeric, 2) as avg_tempo,
    ROUND(MIN(tempo)::numeric, 2) as min_tempo,
    ROUND(MAX(tempo)::numeric, 2) as max_tempo
FROM spotify_tracks_raw;

-- ============================================
-- SUMMARY: Track counts per emotion category
-- ============================================
SELECT 'SUMMARY: Tracks Available Per Category' as summary;
SELECT 
    'Happy/Upbeat' as category,
    COUNT(*) as track_count,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM spotify_tracks_raw))::numeric, 2) as percentage
FROM spotify_tracks_raw
WHERE valence > 0.6 AND energy > 0.6
UNION ALL
SELECT 
    'Sad/Melancholic',
    COUNT(*),
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM spotify_tracks_raw))::numeric, 2)
FROM spotify_tracks_raw
WHERE valence < 0.4 AND energy < 0.4
UNION ALL
SELECT 
    'Energetic/Workout',
    COUNT(*),
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM spotify_tracks_raw))::numeric, 2)
FROM spotify_tracks_raw
WHERE energy > 0.7 AND tempo > 120
UNION ALL
SELECT 
    'Calm/Focus',
    COUNT(*),
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM spotify_tracks_raw))::numeric, 2)
FROM spotify_tracks_raw
WHERE energy < 0.4 AND instrumentalness > 0.5
UNION ALL
SELECT 
    'Relax/Sleep',
    COUNT(*),
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM spotify_tracks_raw))::numeric, 2)
FROM spotify_tracks_raw
WHERE energy < 0.3 AND acousticness > 0.6
UNION ALL
SELECT 
    'Party/Dance',
    COUNT(*),
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM spotify_tracks_raw))::numeric, 2)
FROM spotify_tracks_raw
WHERE energy > 0.7 AND danceability > 0.7
UNION ALL
SELECT 
    '★ Sweet Spot Zone',
    COUNT(*),
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM spotify_tracks_raw))::numeric, 2)
FROM spotify_tracks_raw
WHERE tempo BETWEEN 100 AND 120;
