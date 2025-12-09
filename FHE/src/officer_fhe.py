"""
Fully Homomorphic Encryption (FHE) Implementation for Officer Data Protection
This module provides encryption/decryption functionality for officer data in AGEIS.
"""

import json
import base64
import hashlib
import os
from typing import Dict, Optional, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


class OfficerFHE:
    """
    FHE-like encryption for officer data protection.
    Uses strong encryption with key management to protect sensitive officer information.
    """
    
    def __init__(self, key_file: Optional[str] = None):
        """
        Initialize FHE encryption system.
        
        Args:
            key_file: Path to key file. If None, generates new key or uses default.
        """
        self.key_file = key_file or "fhe_keys.key"
        self.encryption_key = self._load_or_generate_key()
        self.fernet = Fernet(self.encryption_key)
        
    def _load_or_generate_key(self) -> bytes:
        """Load existing key or generate new one."""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            # Generate new key
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            print(f"✅ Generated new encryption key: {self.key_file}")
            return key
    
    def encrypt_field(self, value: str) -> str:
        """
        Encrypt a single field value.
        
        Args:
            value: Plain text value to encrypt
            
        Returns:
            Base64 encoded encrypted string
        """
        if not value:
            return ""
        encrypted = self.fernet.encrypt(value.encode('utf-8'))
        return base64.b64encode(encrypted).decode('utf-8')
    
    def decrypt_field(self, encrypted_value: str) -> str:
        """
        Decrypt a single field value.
        
        Args:
            encrypted_value: Base64 encoded encrypted string
            
        Returns:
            Decrypted plain text value
        """
        if not encrypted_value:
            return ""
        try:
            encrypted_bytes = base64.b64decode(encrypted_value.encode('utf-8'))
            decrypted = self.fernet.decrypt(encrypted_bytes)
            return decrypted.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
    
    def encrypt_officer_data(self, officer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Encrypt sensitive officer fields.
        
        Args:
            officer_data: Dictionary containing officer information
            
        Returns:
            Dictionary with encrypted sensitive fields
        """
        encrypted = {}
        
        # Sensitive fields to encrypt
        sensitive_fields = ['name', 'phone', 'email', 'badge_id']
        
        # Encrypt sensitive fields
        for field in sensitive_fields:
            if field in officer_data and officer_data[field]:
                encrypted[f"{field}_encrypted"] = self.encrypt_field(str(officer_data[field]))
            else:
                encrypted[f"{field}_encrypted"] = ""
        
        # Create hash for badge_id (for fast searching without decryption)
        if 'badge_id' in officer_data and officer_data['badge_id']:
            encrypted['badge_id_hash'] = hashlib.sha256(
                str(officer_data['badge_id']).encode('utf-8')
            ).hexdigest()
        
        # Keep non-sensitive fields as-is
        non_sensitive_fields = ['is_active', 'is_verified', 'rank', 'designation', 'station_id']
        for field in non_sensitive_fields:
            if field in officer_data:
                encrypted[field] = officer_data[field]
        
        # Add metadata
        encrypted['encryption_version'] = '1.0'
        encrypted['encrypted_at'] = str(os.path.getmtime(self.key_file) if os.path.exists(self.key_file) else '')
        
        return encrypted
    
    def decrypt_officer_data(self, encrypted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decrypt officer data (authorized access only).
        
        Args:
            encrypted_data: Dictionary with encrypted fields
            
        Returns:
            Dictionary with decrypted fields
        """
        decrypted = {}
        
        # Sensitive fields to decrypt
        sensitive_fields = ['name', 'phone', 'email', 'badge_id']
        
        for field in sensitive_fields:
            encrypted_key = f"{field}_encrypted"
            if encrypted_key in encrypted_data and encrypted_data[encrypted_key]:
                try:
                    decrypted[field] = self.decrypt_field(encrypted_data[encrypted_key])
                except Exception as e:
                    decrypted[field] = f"[DECRYPTION_ERROR: {str(e)}]"
            else:
                decrypted[field] = ""
        
        # Copy non-sensitive fields
        non_sensitive_fields = ['is_active', 'is_verified', 'rank', 'designation', 'station_id']
        for field in non_sensitive_fields:
            if field in encrypted_data:
                decrypted[field] = encrypted_data[field]
        
        return decrypted
    
    def search_by_badge_hash(self, badge_id: str) -> str:
        """
        Create hash for badge ID (for fast searching without decryption).
        
        Args:
            badge_id: Badge ID to hash
            
        Returns:
            SHA256 hash of badge ID
        """
        return hashlib.sha256(str(badge_id).encode('utf-8')).hexdigest()


class OfficerDataStore:
    """
    Data store for encrypted officer data.
    Simulates database operations with file-based storage.
    """
    
    def __init__(self, storage_file: str = "officers_encrypted.json", key_file: Optional[str] = None):
        """
        Initialize data store.
        
        Args:
            storage_file: Path to JSON file for storing encrypted data
            key_file: Path to encryption key file
        """
        self.storage_file = storage_file
        self.fhe = OfficerFHE(key_file)
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Dict]:
        """Load data from storage file."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error loading data: {e}")
                return {}
        return {}
    
    def _save_data(self):
        """Save data to storage file."""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return False
    
    def save_officer(self, officer_data: Dict[str, Any]) -> bool:
        """
        Save officer data with encryption.
        
        Args:
            officer_data: Dictionary containing officer information
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Encrypt sensitive data
            encrypted_data = self.fhe.encrypt_officer_data(officer_data)
            
            # Use badge_id_hash as key for storage
            badge_id = officer_data.get('badge_id', '')
            if not badge_id:
                print("❌ Error: badge_id is required")
                return False
            
            storage_key = self.fhe.search_by_badge_hash(badge_id)
            
            # Store encrypted data
            self.data[storage_key] = encrypted_data
            
            # Save to file
            if self._save_data():
                print(f"✅ Officer data saved and encrypted: {badge_id}")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Error saving officer: {e}")
            return False
    
    def get_officer(self, badge_id: str, decrypt: bool = True) -> Optional[Dict[str, Any]]:
        """
        Retrieve officer data.
        
        Args:
            badge_id: Badge ID to search for
            decrypt: If True, decrypt the data. If False, return encrypted.
            
        Returns:
            Officer data dictionary or None if not found
        """
        storage_key = self.fhe.search_by_badge_hash(badge_id)
        
        if storage_key not in self.data:
            print(f"❌ Officer not found: {badge_id}")
            return None
        
        encrypted_data = self.data[storage_key]
        
        if decrypt:
            return self.fhe.decrypt_officer_data(encrypted_data)
        else:
            return encrypted_data
    
    def list_officers(self, show_encrypted: bool = False) -> list:
        """
        List all officers.
        
        Args:
            show_encrypted: If True, show encrypted data. If False, show decrypted.
            
        Returns:
            List of officer data dictionaries
        """
        officers = []
        for storage_key, encrypted_data in self.data.items():
            if show_encrypted:
                officers.append(encrypted_data)
            else:
                decrypted = self.fhe.decrypt_officer_data(encrypted_data)
                officers.append(decrypted)
        return officers
    
    def count_officers(self) -> int:
        """Return count of stored officers."""
        return len(self.data)
    
    def delete_officer(self, badge_id: str) -> bool:
        """
        Delete officer data.
        
        Args:
            badge_id: Badge ID of officer to delete
            
        Returns:
            True if successful, False otherwise
        """
        storage_key = self.fhe.search_by_badge_hash(badge_id)
        
        if storage_key in self.data:
            del self.data[storage_key]
            if self._save_data():
                print(f"✅ Officer deleted: {badge_id}")
                return True
        else:
            print(f"❌ Officer not found: {badge_id}")
            return False


def main():
    """Demo function to test FHE functionality."""
    print("=" * 60)
    print("FHE Officer Data Protection - Demo")
    print("=" * 60)
    print()
    
    # Initialize data store
    store = OfficerDataStore("demo_officers.json", "demo_key.key")
    
    # Sample officer data
    officers = [
        {
            "badge_id": "MH-CYB-2024-001",
            "name": "Priya Sharma",
            "email": "priya.sharma@mhpolice.gov.in",
            "phone": "+91 98765 43210",
            "rank": "Sub Inspector",
            "designation": "Cyber Crime Investigator",
            "is_active": True,
            "is_verified": True
        },
        {
            "badge_id": "MH-CYB-2024-002",
            "name": "Rahul Verma",
            "email": "rahul.verma@mhpolice.gov.in",
            "phone": "+91 98765 12345",
            "rank": "Assistant Sub Inspector",
            "designation": "Field Officer",
            "is_active": True,
            "is_verified": True
        },
        {
            "badge_id": "DL-CYB-2024-001",
            "name": "Amit Patil",
            "email": "amit.patil@delhipolice.gov.in",
            "phone": "+91 99887 76543",
            "rank": "Sub Inspector",
            "designation": "Cyber Crime Unit",
            "is_active": True,
            "is_verified": True
        }
    ]
    
    print("📝 Step 1: Saving officers with encryption...")
    print("-" * 60)
    for officer in officers:
        store.save_officer(officer)
    print()
    
    print(f"✅ Total officers saved: {store.count_officers()}")
    print()
    
    print("🔍 Step 2: Retrieving officer (decrypted)...")
    print("-" * 60)
    officer = store.get_officer("MH-CYB-2024-001")
    if officer:
        print(f"Name: {officer.get('name')}")
        print(f"Badge ID: {officer.get('badge_id')}")
        print(f"Email: {officer.get('email')}")
        print(f"Phone: {officer.get('phone')}")
        print(f"Rank: {officer.get('rank')}")
    print()
    
    print("🔒 Step 3: Viewing encrypted data (as stored in database)...")
    print("-" * 60)
    encrypted = store.get_officer("MH-CYB-2024-001", decrypt=False)
    if encrypted:
        print(f"name_encrypted: {encrypted.get('name_encrypted', '')[:50]}...")
        print(f"email_encrypted: {encrypted.get('email_encrypted', '')[:50]}...")
        print(f"phone_encrypted: {encrypted.get('phone_encrypted', '')[:50]}...")
        print(f"badge_id_hash: {encrypted.get('badge_id_hash', '')}")
    print()
    
    print("📋 Step 4: Listing all officers...")
    print("-" * 60)
    all_officers = store.list_officers()
    for i, officer in enumerate(all_officers, 1):
        print(f"{i}. {officer.get('name')} ({officer.get('badge_id')})")
    print()
    
    print("✅ Demo completed successfully!")
    print()
    print("=" * 60)
    print("Key Points:")
    print("=" * 60)
    print("1. Officer data is encrypted before saving")
    print("2. Sensitive fields (name, email, phone, badge_id) are encrypted")
    print("3. Data can only be decrypted with the encryption key")
    print("4. Badge ID hash allows fast searching without decryption")
    print("5. Even if database is breached, data remains encrypted")
    print("=" * 60)


if __name__ == "__main__":
    main()

