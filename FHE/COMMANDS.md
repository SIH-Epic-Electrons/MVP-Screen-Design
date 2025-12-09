# FHE - Command Guide

## Quick Commands

### Option 1: Using Batch Files (Windows)

```bash
# Run demo only
FHE\run_demo.bat

# Run tests only
FHE\run_tests.bat

# Run everything (demo + tests)
FHE\run_all.bat
```

### Option 2: Using Python Directly

```bash
# Navigate to src folder
cd FHE\src

# Install dependencies (first time only)
pip install -r requirements.txt

# Run demo
python officer_fhe.py

# Run tests
python test_fhe.py
```

### Option 3: Using PowerShell

```powershell
# Navigate to src folder
cd FHE\src

# Install dependencies
pip install -r requirements.txt

# Run demo
python officer_fhe.py

# Run tests
python test_fhe.py
```

## Step-by-Step Instructions

### First Time Setup

1. **Install Python** (if not already installed)
   - Download from python.org
   - Make sure Python is in PATH

2. **Install Dependencies**
   ```bash
   cd FHE\src
   pip install -r requirements.txt
   ```

3. **Verify Installation**
   ```bash
   python -c "import cryptography; print('✅ Cryptography installed')"
   ```

### Running the Demo

The demo will:
- Create sample officer data
- Encrypt and save it
- Retrieve and decrypt it
- Show encrypted vs decrypted data

**Command:**
```bash
cd FHE\src
python officer_fhe.py
```

**Expected Output:**
```
============================================================
FHE Officer Data Protection - Demo
============================================================

✅ Generated new encryption key: demo_key.key
📝 Step 1: Saving officers with encryption...
✅ Officer data saved and encrypted: MH-CYB-2024-001
✅ Officer data saved and encrypted: MH-CYB-2024-002
✅ Officer data saved and encrypted: DL-CYB-2024-001

✅ Total officers saved: 3

🔍 Step 2: Retrieving officer (decrypted)...
Name: Priya Sharma
Badge ID: MH-CYB-2024-001
Email: priya.sharma@mhpolice.gov.in
Phone: +91 98765 43210
Rank: Sub Inspector

🔒 Step 3: Viewing encrypted data (as stored in database)...
name_encrypted: gAAAAABl...
email_encrypted: gAAAAABl...
phone_encrypted: gAAAAABl...
badge_id_hash: a1b2c3d4e5f6...

📋 Step 4: Listing all officers...
1. Priya Sharma (MH-CYB-2024-001)
2. Rahul Verma (MH-CYB-2024-002)
3. Amit Patil (DL-CYB-2024-001)

✅ Demo completed successfully!
```

### Running Tests

The test suite verifies:
- Encryption/decryption works correctly
- Data store operations function properly
- Security features are working

**Command:**
```bash
cd FHE\src
python test_fhe.py
```

**Expected Output:**
```
============================================================
FHE Officer Data Protection - Test Suite
============================================================

============================================================
Test 1: Encryption/Decryption
============================================================

📝 Encrypting data...
✅ Encrypted fields: ['name_encrypted', 'phone_encrypted', ...]
   name_encrypted: gAAAAABl...

🔓 Decrypting data...
✅ Decrypted data:
   name: Test Officer
   badge_id: TEST-001
   ...

✅ Test 1 PASSED: Encryption/Decryption works correctly

============================================================
Test 2: Data Store Operations
============================================================
...

✅ ALL TESTS PASSED!
```

## Troubleshooting

### Error: "pip is not recognized"
- Install Python from python.org
- Make sure to check "Add Python to PATH" during installation
- Restart terminal after installation

### Error: "No module named 'cryptography'"
```bash
pip install cryptography
```

### Error: "Permission denied"
- Run terminal as Administrator
- Or use: `pip install --user -r requirements.txt`

### Error: "Python not found"
- Make sure Python is installed
- Check PATH: `python --version`
- Use full path: `C:\Python39\python.exe officer_fhe.py`

## File Locations

After running:
- **Encryption keys**: `FHE\src\*.key` (keep these secure!)
- **Data files**: `FHE\src\*.json` (encrypted officer data)

## Clean Up Test Files

To remove test files:
```bash
cd FHE\src
del test_key.key test_officers.json demo_key.key demo_officers.json
```

Or let the test script clean up (it will ask).

## Integration with AGEIS

To use in AGEIS backend:

1. Copy `FHE\src\officer_fhe.py` to `AEGIS-\backend\app\fhe\`
2. Import in your officer service
3. Use `OfficerDataStore` or `OfficerFHE` classes

Example:
```python
from app.fhe.officer_fhe import OfficerFHE

fhe = OfficerFHE("production_key.key")
encrypted = fhe.encrypt_officer_data(officer_data)
```

## Need Help?

1. Check `FHE\README.md` for overview
2. Check `FHE\docs\` for detailed documentation
3. Check `FHE\src\README.md` for code documentation
4. Run tests to verify everything works

