# FHE Implementation - Source Code

This folder contains the working implementation of FHE (Fully Homomorphic Encryption) for protecting officer data in AGEIS.

## Files

- `officer_fhe.py` - Main FHE encryption/decryption module
- `test_fhe.py` - Test suite to verify functionality
- `requirements.txt` - Python dependencies

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Demo

Run the demo to see FHE in action:

```bash
python officer_fhe.py
```

This will:
1. Create sample officer data
2. Encrypt and save it
3. Retrieve and decrypt it
4. Show encrypted vs decrypted data

### Run Tests

Run the test suite:

```bash
python test_fhe.py
```

This will verify:
- Encryption/decryption works correctly
- Data store operations function properly
- Security features are working

### Programmatic Usage

```python
from officer_fhe import OfficerDataStore

# Initialize data store
store = OfficerDataStore("officers.json", "encryption_key.key")

# Save officer with encryption
officer_data = {
    "badge_id": "MH-CYB-2024-001",
    "name": "Priya Sharma",
    "email": "priya.sharma@mhpolice.gov.in",
    "phone": "+91 98765 43210",
    "rank": "Sub Inspector",
    "is_active": True
}

store.save_officer(officer_data)

# Retrieve officer (decrypted)
officer = store.get_officer("MH-CYB-2024-001")
print(officer['name'])  # Priya Sharma

# View encrypted data (as stored in database)
encrypted = store.get_officer("MH-CYB-2024-001", decrypt=False)
print(encrypted['name_encrypted'])  # Encrypted string
```

## Key Features

1. **Automatic Encryption**: Sensitive fields (name, email, phone, badge_id) are automatically encrypted
2. **Secure Storage**: Data is stored encrypted in JSON format
3. **Fast Search**: Uses hash-based lookup for badge IDs (no decryption needed)
4. **Key Management**: Encryption keys are stored securely in separate files
5. **Authorized Access**: Only authorized users with the key can decrypt data

## Security Notes

- Encryption keys are stored in `.key` files - keep these secure!
- Never commit encryption keys to version control
- Use different keys for development and production
- Rotate keys periodically for enhanced security

## Integration with AGEIS

To integrate with AGEIS backend:

1. Copy `officer_fhe.py` to `backend/app/fhe/`
2. Import and use in officer service:
   ```python
   from app.fhe.officer_fhe import OfficerFHE
   ```
3. Encrypt data before saving to database
4. Decrypt only when authorized user requests data

