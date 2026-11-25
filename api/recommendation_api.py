"""
RECOMMENDATION API
==================
Smart music recommendation dengan conversational filtering
Bahasa Indonesia, user-friendly, no technical terms
"""

from flask import Blueprint, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os

recommend_bp = Blueprint('recommend', __name__)

# Database connection (akan di-import dari search_api)
def get_db_connection():
    """Get PostgreSQL connection"""
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if DATABASE_URL:
        import urllib.parse as urlparse
        url = urlparse.urlparse(DATABASE_URL)
        DB_CONFIG = {
            'host': url.hostname,
            'port': url.port,
            'database': url.path[1:],
            'user': url.username,
            'password': url.password
        }
    else:
        DB_CONFIG = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 5432)),
            'database': os.getenv('DB_NAME', 'spotify_music_db'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'runadb')
        }
    
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)


# ============================================
# MOOD MAPPINGS (Indonesia)
# ============================================

MOOD_MAPPINGS = {
    # 😊 Senang-senang
    'senang': {
        'joget': {
            'filters': {
                'danceability': (0.7, 1.0),
                'tempo': (100, 130),
                'valence': (0.6, 1.0)
            },
            'description': 'Lagu groovy & catchy buat goyang'
        },
        'nyanyi': {
            'filters': {
                'speechiness': (0.1, 0.3),
                'valence': (0.7, 1.0),
                'energy': (0.5, 1.0)
            },
            'description': 'Lagu enak buat sing-along'
        },
        'santai': {
            'filters': {
                'energy': (0.5, 0.7),
                'valence': (0.6, 1.0)
            },
            'description': 'Mood booster yang santai'
        },
        'pagi_cerah': {
            'filters': {
                'valence': (0.7, 1.0),
                'energy': (0.5, 0.7)
            },
            'description': 'Feel good vibes buat pagi'
        }
    },
    
    # 💪 Olahraga
    'olahraga': {
        'lari_cardio': {
            'filters': {
                'energy': (0.8, 1.0),
                'tempo': (140, 180)
            },
            'description': 'Lagu cepat & energik buat lari'
        },
        'gym_beban': {
            'filters': {
                'energy': (0.7, 0.9),
                'tempo': (110, 140)
            },
            'description': 'Lagu semangat yang stabil'
        },
        'yoga': {
            'filters': {
                'energy': (0.2, 0.4),
                'acousticness': (0.5, 1.0),
                'tempo': (60, 90)
            },
            'description': 'Lagu tenang & rileks'
        },
        'sepeda': {
            'filters': {
                'energy': (0.6, 0.8),
                'tempo': (110, 140)
            },
            'description': 'Lagu sedang & menyenangkan'
        }
    },
    
    # 📚 Belajar/Kerja
    'belajar': {
        'fokus_maksimal': {
            'filters': {
                'instrumentalness': (0.7, 1.0),
                'speechiness': (0.0, 0.05),
                'energy': (0.0, 0.3)
            },
            'description': 'Tanpa lirik, full konsentrasi'
        },
        'musik_latar': {
            'filters': {
                'energy': (0.3, 0.5),
                'speechiness': (0.0, 0.2)
            },
            'description': 'Ada lirik tapi gak ganggu'
        },
        'santai_kerja': {
            'filters': {
                'acousticness': (0.5, 1.0),
                'energy': (0.3, 0.5)
            },
            'description': 'Lagu enak didenger'
        }
    },
    
    # 😢 Galau/Sedih
    'galau': {
        'nangis_curhat': {
            'filters': {
                'valence': (0.1, 0.3),
                'energy': (0.3, 0.6)
            },
            'description': 'Lagu sedih yang relate'
        },
        'melow_merenung': {
            'filters': {
                'valence': (0.2, 0.4),
                'acousticness': (0.5, 1.0),
                'tempo': (60, 90),
                'energy': (0.2, 0.5)
            },
            'description': 'Lagu pelan & menenangkan'
        },
        'hujan': {
            'filters': {
                'valence': (0.3, 0.5),
                'energy': (0.2, 0.4),
                'acousticness': (0.4, 1.0)
            },
            'description': 'Lagu buat nemenin ujan'
        }
    },
    
    # 💤 Santai/Tidur
    'santai': {
        'tidur': {
            'filters': {
                'energy': (0.0, 0.2),
                'loudness': (-30, -15),
                'tempo': (40, 70)
            },
            'description': 'Super pelan & tenang'
        },
        'meditasi': {
            'filters': {
                'instrumentalness': (0.7, 1.0),
                'energy': (0.1, 0.3),
                'tempo': (50, 80)
            },
            'description': 'Fokus & ketenangan'
        },
        'baca_buku': {
            'filters': {
                'energy': (0.2, 0.4),
                'acousticness': (0.5, 1.0),
                'speechiness': (0.0, 0.05)
            },
            'description': 'Background musik lembut'
        },
        'ngopi': {
            'filters': {
                'energy': (0.3, 0.5),
                'valence': (0.4, 0.7)
            },
            'description': 'Lagu enak & nyaman'
        }
    },
    
    # 🎉 Pesta/Nongkrong
    'pesta': {
        'dance_party': {
            'filters': {
                'danceability': (0.7, 1.0),
                'energy': (0.7, 1.0),
                'tempo': (110, 130)
            },
            'description': 'Lagu buat nge-dance'
        },
        'hype_party': {
            'filters': {
                'energy': (0.8, 1.0),
                'valence': (0.7, 1.0),
                'tempo': (120, 140)
            },
            'description': 'Super energik & hype'
        },
        'santai_nongkrong': {
            'filters': {
                'energy': (0.5, 0.7),
                'valence': (0.6, 1.0),
                'tempo': (90, 120)
            },
            'description': 'Chill vibes bareng temen'
        },
        'preparty': {
            'filters': {
                'energy': (0.6, 0.8),
                'tempo': (100, 130)
            },
            'description': 'Build up energy'
        }
    },
    
    # 🚗 Nyetir/Perjalanan
    'nyetir': {
        'jalan_tol': {
            'filters': {
                'tempo': (110, 130),
                'energy': (0.5, 0.7),
                'valence': (0.5, 0.8)
            },
            'description': 'Enak buat cruise'
        },
        'macet': {
            'filters': {
                'tempo': (80, 100),
                'energy': (0.4, 0.6)
            },
            'description': 'Santai biar gak stress'
        },
        'malam': {
            'filters': {
                'tempo': (80, 110),
                'energy': (0.3, 0.6),
                'valence': (0.4, 0.7)
            },
            'description': 'Mood chill & santai'
        },
        'roadtrip': {
            'filters': {
                'tempo': (100, 130),
                'energy': (0.6, 0.8),
                'valence': (0.6, 1.0)
            },
            'description': 'Petualang & bebas'
        }
    },
    
    # ❤️ Romantis
    'romantis': {
        'intimate': {
            'filters': {
                'energy': (0.2, 0.5),
                'acousticness': (0.5, 1.0),
                'valence': (0.5, 0.8)
            },
            'description': 'Lembut & personal'
        },
        'kencan': {
            'filters': {
                'energy': (0.4, 0.6),
                'valence': (0.6, 0.9),
                'tempo': (80, 110)
            },
            'description': 'Manis & menyenangkan'
        },
        'slow_dance': {
            'filters': {
                'danceability': (0.6, 0.9),
                'tempo': (60, 90),
                'valence': (0.6, 0.9)
            },
            'description': 'Dance berdua'
        },
        'love_songs': {
            'filters': {
                'valence': (0.6, 0.9),
                'acousticness': (0.3, 1.0)
            },
            'description': 'Lagu cinta klasik'
        }
    }
}


# ============================================
# RECOMMENDATION ENDPOINT
# ============================================

@recommend_bp.route('/recommend', methods=['POST'])
def get_recommendations():
    """
    Smart recommendation based on mood & activity
    
    Request JSON:
    {
        "mood": "olahraga",
        "activity": "lari_cardio",
        "intensity": "maximum",  # calm, moderate, energetic, maximum
        "limit": 20
    }
    
    Returns: List of recommended tracks with match scores
    """
    try:
        data = request.json
        mood = data.get('mood')
        activity = data.get('activity')
        intensity = data.get('intensity', 'moderate')
        limit = min(int(data.get('limit', 20)), 100)
        
        if not mood or not activity:
            return jsonify({
                'success': False,
                'error': 'Mood dan activity harus diisi'
            }), 400
        
        # Get filter configuration
        if mood not in MOOD_MAPPINGS:
            return jsonify({
                'success': False,
                'error': f'Mood "{mood}" tidak ditemukan'
            }), 400
        
        if activity not in MOOD_MAPPINGS[mood]:
            return jsonify({
                'success': False,
                'error': f'Activity "{activity}" tidak ditemukan untuk mood "{mood}"'
            }), 400
        
        config = MOOD_MAPPINGS[mood][activity]
        filters = config['filters'].copy()  # Make a copy to modify
        description = config['description']
        
        # Apply intensity modifiers
        intensity_modifiers = {
            'calm': {'energy_mult': 0.7, 'tempo_mult': 0.85},
            'moderate': {'energy_mult': 1.0, 'tempo_mult': 1.0},
            'energetic': {'energy_mult': 1.15, 'tempo_mult': 1.1},
            'maximum': {'energy_mult': 1.3, 'tempo_mult': 1.2}
        }
        
        modifier = intensity_modifiers.get(intensity, intensity_modifiers['moderate'])
        
        # Adjust energy range based on intensity
        if 'energy' in filters:
            energy_min, energy_max = filters['energy']
            # Scale but keep within 0-1 bounds
            filters['energy'] = (
                max(0.0, min(1.0, energy_min * modifier['energy_mult'])),
                min(1.0, energy_max * modifier['energy_mult'])
            )
        
        # Adjust tempo range based on intensity
        if 'tempo' in filters:
            tempo_min, tempo_max = filters['tempo']
            # Scale tempo
            filters['tempo'] = (
                max(40, tempo_min * modifier['tempo_mult']),
                min(200, tempo_max * modifier['tempo_mult'])
            )
        
        # Build SQL query with weighted scoring
        conn = get_db_connection()
        cur = conn.cursor()
        
        sql = """
            SELECT 
                id, name, artists, year,
                tempo, energy, valence, danceability,
                acousticness, instrumentalness, 
                speechiness, loudness,
                -- Calculate match score (0-1)
                (
        """
        
        params = {}
        score_parts = []
        weight_total = 0
        
        # Build dynamic scoring based on filters
        filter_weights = {
            'energy': 0.20,        # Reduced from 0.25
            'tempo': 0.20,         # Reduced from 0.25
            'valence': 0.12,       # Reduced from 0.15
            'danceability': 0.12,  # Reduced from 0.15
            'acousticness': 0.08,  # Reduced from 0.1
            'instrumentalness': 0.04,  # Reduced from 0.05
            'speechiness': 0.02,   # Reduced from 0.03
            'loudness': 0.02       # Same
        }
        
        for feature, (min_val, max_val) in filters.items():
            if feature in filter_weights:
                weight = filter_weights[feature]
                weight_total += weight
                
                if feature == 'tempo':
                    # Tempo scoring (closer to middle of range = better)
                    mid_tempo = (min_val + max_val) / 2
                    score_parts.append(f"""
                        (1.0 - LEAST(1.0, ABS(tempo - {mid_tempo}) / {(max_val - min_val) / 2})) * {weight}
                    """)
                elif feature == 'loudness':
                    # Loudness scoring (normalized to 0-1)
                    score_parts.append(f"""
                        CASE 
                            WHEN loudness BETWEEN {min_val} AND {max_val} 
                            THEN {weight}
                            ELSE {weight * 0.3}
                        END
                    """)
                else:
                    # Standard feature scoring (0-1 range)
                    score_parts.append(f"""
                        CASE 
                            WHEN {feature} BETWEEN {min_val} AND {max_val}
                            THEN {weight}
                            ELSE {weight * 0.3}
                        END
                    """)
        
        # Add recency score (20% weight) - favor newer tracks
        recency_weight = 0.10
        weight_total += recency_weight
        score_parts.append(f"""
            ((year - 1920.0) / (2020.0 - 1920.0)) * {recency_weight}
        """)
        
        # Add danceability bonus (10% weight) - proxy for popularity
        dance_bonus_weight = 0.10
        weight_total += dance_bonus_weight
        score_parts.append(f"""
            (danceability * {dance_bonus_weight})
        """)
        
        sql += " + ".join(score_parts)
        sql += f"""
                ) / {weight_total} as match_score,
                -- Sweet spot bonus indicator
                CASE 
                    WHEN tempo BETWEEN 100 AND 120 THEN true
                    ELSE false
                END as in_sweet_spot
            FROM spotify_tracks_raw
            WHERE 1=1
        """
        
        # Add WHERE filters
        for feature, (min_val, max_val) in filters.items():
            if feature == 'tempo':
                sql += f" AND tempo BETWEEN {min_val} AND {max_val}"
            elif feature == 'loudness':
                sql += f" AND loudness BETWEEN {min_val} AND {max_val}"
            else:
                # For 0-1 features, allow some tolerance
                tolerance = 0.1
                sql += f" AND {feature} BETWEEN {max(0, min_val - tolerance)} AND {min(1, max_val + tolerance)}"
        
        # Sort by: match_score DESC, sweet_spot bonus, year DESC
        sql += """ 
            ORDER BY 
                match_score DESC,
                in_sweet_spot DESC,
                year DESC
            LIMIT %s
        """
        params['limit'] = limit
        
        cur.execute(sql, (limit,))
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        # Add natural language descriptions
        for track in results:
            track['match_description'] = generate_match_description(track, filters)
        
        return jsonify({
            'success': True,
            'mood': mood,
            'activity': activity,
            'intensity': intensity,
            'description': description,
            'filters_applied': filters,
            'count': len(results),
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def generate_match_description(track, filters):
    """Generate natural language description for match quality"""
    
    descriptions = []
    
    # Tempo description
    if 'tempo' in filters:
        tempo = track['tempo']
        min_t, max_t = filters['tempo']
        if min_t <= tempo <= max_t:
            if tempo < 80:
                descriptions.append('Pelan')
            elif tempo < 110:
                descriptions.append('Sedang')
            elif tempo < 140:
                descriptions.append('Cepat')
            else:
                descriptions.append('Super cepat')
    
    # Energy description
    if 'energy' in filters:
        energy = track['energy']
        if energy > 0.7:
            descriptions.append('Energik')
        elif energy > 0.5:
            descriptions.append('Semangat')
        elif energy > 0.3:
            descriptions.append('Santai')
        else:
            descriptions.append('Tenang')
    
    # Valence description
    if 'valence' in filters:
        valence = track['valence']
        if valence > 0.7:
            descriptions.append('Senang')
        elif valence < 0.3:
            descriptions.append('Sedih')
    
    # Danceability
    if 'danceability' in filters and track['danceability'] > 0.7:
        descriptions.append('Groovy')
    
    # Acousticness
    if 'acousticness' in filters and track['acousticness'] > 0.5:
        descriptions.append('Akustik')
    
    # Instrumentalness
    if 'instrumentalness' in filters and track['instrumentalness'] > 0.5:
        descriptions.append('Instrumental')
    
    # Recency bonus - show if track is recent
    year = track.get('year')
    if year and year >= 2015:
        descriptions.append('🔥 Hits')
    elif year and year >= 2010:
        descriptions.append('Modern')
    
    # Sweet spot bonus
    if track.get('in_sweet_spot') or (100 <= track['tempo'] <= 120):
        descriptions.append('⭐ Sweet spot')
    
    return ' & '.join(descriptions[:4]) if descriptions else 'Cocok'


# ============================================
# GET AVAILABLE MOODS & ACTIVITIES
# ============================================

@recommend_bp.route('/moods', methods=['GET'])
def get_moods():
    """Get list of available moods and their activities"""
    
    moods_list = []
    
    mood_info = {
        'senang': {'emoji': '😊', 'label': 'Senang-senang'},
        'olahraga': {'emoji': '💪', 'label': 'Olahraga'},
        'belajar': {'emoji': '📚', 'label': 'Belajar/Kerja'},
        'galau': {'emoji': '😢', 'label': 'Galau/Sedih'},
        'santai': {'emoji': '💤', 'label': 'Santai/Tidur'},
        'pesta': {'emoji': '🎉', 'label': 'Pesta/Nongkrong'},
        'nyetir': {'emoji': '🚗', 'label': 'Nyetir/Perjalanan'},
        'romantis': {'emoji': '❤️', 'label': 'Romantis'}
    }
    
    for mood_id, activities in MOOD_MAPPINGS.items():
        mood_data = {
            'id': mood_id,
            'emoji': mood_info[mood_id]['emoji'],
            'label': mood_info[mood_id]['label'],
            'activities': []
        }
        
        for activity_id, config in activities.items():
            mood_data['activities'].append({
                'id': activity_id,
                'description': config['description']
            })
        
        moods_list.append(mood_data)
    
    return jsonify({
        'success': True,
        'moods': moods_list
    })
