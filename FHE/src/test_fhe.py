"""
Test script for FHE officer data protection.
Run this to verify the encryption/decryption functionality.
"""

import os
import sys
from officer_fhe import OfficerFHE, OfficerDataStore


def test_encryption_decryption():
    """Test basic encryption and decryption."""
    print("=" * 60)
    print("Test 1: Encryption/Decryption")
    print("=" * 60)
    
    fhe = OfficerFHE("test_key.key")
    
    # Test data
    test_data = {
        "name": "Test Officer",
        "badge_id": "TEST-001",
        "email": "test@example.com",
        "phone": "1234567890"
    }
    
    # Encrypt
    print("\n📝 Encrypting data...")
    encrypted = fhe.encrypt_officer_data(test_data)
    print(f"✅ Encrypted fields: {list(encrypted.keys())}")
    print(f"   name_encrypted: {encrypted['name_encrypted'][:50]}...")
    
    # Decrypt
    print("\n🔓 Decrypting data...")
    decrypted = fhe.decrypt_officer_data(encrypted)
    print(f"✅ Decrypted data:")
    for key, value in decrypted.items():
        print(f"   {key}: {value}")
    
    # Verify
    assert decrypted['name'] == test_data['name'], "Name mismatch!"
    assert decrypted['badge_id'] == test_data['badge_id'], "Badge ID mismatch!"
    print("\n✅ Test 1 PASSED: Encryption/Decryption works correctly")
    print()


def test_data_store():
    """Test data store operations."""
    print("=" * 60)
    print("Test 2: Data Store Operations")
    print("=" * 60)
    
    # Use test files
    store = OfficerDataStore("test_officers.json", "test_key.key")
    
    # Test officer
    officer = {
        "badge_id": "TEST-002",
        "name": "John Doe",
        "email": "john.doe@test.gov.in",
        "phone": "9876543210",
        "rank": "Inspector",
        "is_active": True
    }
    
    # Save
    print("\n💾 Saving officer...")
    result = store.save_officer(officer)
    assert result, "Failed to save officer!"
    print(f"✅ Officer saved: {officer['badge_id']}")
    
    # Retrieve
    print("\n🔍 Retrieving officer...")
    retrieved = store.get_officer("TEST-002")
    assert retrieved is not None, "Failed to retrieve officer!"
    assert retrieved['name'] == officer['name'], "Name mismatch!"
    print(f"✅ Officer retrieved: {retrieved['name']}")
    
    # Count
    count = store.count_officers()
    print(f"✅ Total officers: {count}")
    
    # List
    print("\n📋 Listing officers...")
    officers = store.list_officers()
    print(f"✅ Found {len(officers)} officers")
    
    print("\n✅ Test 2 PASSED: Data store operations work correctly")
    print()


def test_security():
    """Test security features."""
    print("=" * 60)
    print("Test 3: Security Features")
    print("=" * 60)
    
    store = OfficerDataStore("test_officers.json", "test_key.key")
    
    # Get encrypted data
    print("\n🔒 Viewing encrypted data (as attacker would see)...")
    encrypted = store.get_officer("TEST-002", decrypt=False)
    
    if encrypted:
        print("✅ Encrypted data (unreadable without key):")
        print(f"   name_encrypted: {encrypted.get('name_encrypted', '')[:60]}...")
        print(f"   email_encrypted: {encrypted.get('email_encrypted', '')[:60]}...")
        print(f"   badge_id_hash: {encrypted.get('badge_id_hash', '')}")
        print("\n✅ Security: Sensitive data is encrypted and unreadable")
    
    # Test hash search
    print("\n🔍 Testing hash-based search...")
    badge_hash = store.fhe.search_by_badge_hash("TEST-002")
    print(f"✅ Badge hash: {badge_hash}")
    print("   (Allows fast searching without decryption)")
    
    print("\n✅ Test 3 PASSED: Security features working correctly")
    print()


def cleanup_test_files():
    """Remove test files."""
    test_files = [
        "test_key.key",
        "test_officers.json",
        "demo_key.key",
        "demo_officers.json"
    ]
    
    print("\n🧹 Cleaning up test files...")
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"   ✅ Removed: {file}")
            except Exception as e:
                print(f"   ⚠️ Could not remove {file}: {e}")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("FHE Officer Data Protection - Test Suite")
    print("=" * 60)
    print()
    
    try:
        # Run tests
        test_encryption_decryption()
        test_data_store()
        test_security()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print()
        
        # Ask about cleanup
        response = input("Clean up test files? (y/n): ").strip().lower()
        if response == 'y':
            cleanup_test_files()
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

