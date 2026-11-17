"""
Test Firebase Connection
Make sure credentials work before syncing data
"""

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# ==============================================
# CONFIGURATION
# ==============================================
CREDENTIALS_PATH = r'D:\Semester 5\BIG DATA\Project\firebase-credentials.json'

# ==============================================
# MAIN
# ==============================================

def main():
    print("=" * 60)
    print("🔥 FIREBASE CONNECTION TEST")
    print("=" * 60)
    
    # Step 1: Initialize Firebase
    print("\n📋 Step 1: Initializing Firebase...")
    try:
        cred = credentials.Certificate(CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred)
        print("   ✅ Firebase initialized!")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print(f"\n💡 Make sure file exists: {CREDENTIALS_PATH}")
        return
    
    # Step 2: Connect to Firestore
    print("\n📋 Step 2: Connecting to Firestore...")
    try:
        db = firestore.client()
        print("   ✅ Connected to Firestore!")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Step 3: Write test document
    print("\n📋 Step 3: Writing test document...")
    try:
        test_data = {
            'test': True,
            'message': 'Hello from Python!',
            'timestamp': datetime.now(),
            'project': 'spotify-tempo-analysis'
        }
        
        doc_ref = db.collection('_test').document('connection_test')
        doc_ref.set(test_data)
        print("   ✅ Test document written!")
        print(f"   📄 Collection: _test")
        print(f"   📄 Document: connection_test")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Step 4: Read test document
    print("\n📋 Step 4: Reading test document...")
    try:
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            print("   ✅ Test document read successfully!")
            print(f"   📄 Data: {data}")
        else:
            print("   ⚠️  Document not found")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Step 5: Delete test document
    print("\n📋 Step 5: Cleaning up...")
    try:
        doc_ref.delete()
        print("   ✅ Test document deleted!")
    except Exception as e:
        print(f"   ⚠️  Cleanup failed: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ CONNECTION TEST SUCCESSFUL!")
    print("=" * 60)
    print("\n💡 Next steps:")
    print("   1. Check Firebase Console to see the test")
    print("   2. Run sync script to transfer PostgreSQL → Firestore")
    print(f"\n🔗 Firebase Console:")
    print(f"   https://console.firebase.google.com/")

if __name__ == "__main__":
    main()
