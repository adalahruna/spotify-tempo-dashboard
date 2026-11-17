import firebase_admin
from firebase_admin import credentials, firestore

# Initialize
cred = credentials.Certificate('../firebase-credentials.json')
try:
    app = firebase_admin.get_app()
except:
    app = firebase_admin.initialize_app(cred)

db = firestore.client()

# Check global stats
print("Checking Firestore data...")
print("-" * 50)

doc = db.collection('summary').document('global_stats').get()
if doc.exists:
    print("✅ global_stats exists!")
    data = doc.to_dict()
    print(f"   Total tracks: {data.get('total_tracks', 'N/A')}")
    print(f"   Avg tempo: {data.get('avg_tempo', 'N/A')}")
    print(f"   Sweet spot %: {data.get('sweet_spot_percentage', 'N/A')}")
else:
    print("❌ global_stats NOT FOUND! Run sync script first!")

print()

# Check tempo zones
zones = db.collection('tempo_zones').limit(5).stream()
zone_count = sum(1 for _ in zones)
print(f"Tempo zones count: {zone_count} (expected: 5)")

print()

# Check top tracks
top_doc = db.collection('top_tracks').document('sweet_spot_top_100').get()
if top_doc.exists:
    tracks = top_doc.to_dict().get('tracks', [])
    print(f"✅ Top tracks: {len(tracks)} tracks")
else:
    print("❌ Top tracks NOT FOUND!")
