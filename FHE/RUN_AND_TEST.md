# Quick Commands to Run and Test FHE

## 🚀 Run Demo (See it in action)

### Windows PowerShell/CMD:
```bash
cd FHE\src
python officer_fhe.py
```

### Or use batch file:
```bash
FHE\run_demo.bat
```

## 🧪 Run Tests (Verify functionality)

### Windows PowerShell/CMD:
```bash
cd FHE\src
python test_fhe.py
```

### Or use batch file:
```bash
FHE\run_tests.bat
```

## 🔄 Run Everything (Demo + Tests)

### Windows PowerShell/CMD:
```bash
cd FHE\src
python officer_fhe.py
python test_fhe.py
```

### Or use batch file:
```bash
FHE\run_all.bat
```

## 📋 Step-by-Step

### 1. Install Dependencies (First time only)
```bash
cd FHE\src
pip install -r requirements.txt
```

### 2. Run Demo
```bash
python officer_fhe.py
```

**Expected Output:**
- ✅ Encryption key generated
- ✅ Officers saved and encrypted
- ✅ Data retrieved and decrypted
- ✅ Encrypted data shown (unreadable)

### 3. Run Tests
```bash
python test_fhe.py
```

**Expected Output:**
- ✅ Test 1: Encryption/Decryption PASSED
- ✅ Test 2: Data Store Operations PASSED
- ✅ Test 3: Security Features PASSED
- ✅ ALL TESTS PASSED!

## 🧹 Clean Up Test Files

After testing, remove generated files:
```bash
cd FHE\src
del demo_key.key demo_officers.json test_key.key test_officers.json
```

## 📊 What Gets Created

When you run the code:
- `demo_key.key` - Encryption key (keep secure!)
- `demo_officers.json` - Encrypted officer data
- `test_key.key` - Test encryption key
- `test_officers.json` - Test encrypted data

## ✅ Quick Verification

Run this to verify everything works:
```bash
cd FHE\src
python -c "from officer_fhe import OfficerFHE; print('✅ FHE module loaded successfully')"
```

