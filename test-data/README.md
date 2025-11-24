# Test Data Directory

This directory contains test data files used by Robot Framework test suites.

## Directory Structure

```
test-data/
├── api/                    # API test payloads
│   ├── create_domain.json
│   ├── create_namespace.json
│   ├── set_quota.json
│   └── create_bucket.json
├── files/                  # Test files for upload/download
│   ├── small_file.txt
│   ├── medium_file.dat
│   └── large_file.bin
├── credentials/            # Test credentials (NOT COMMITTED)
│   └── .gitignore
├── expected/               # Expected test results
│   ├── health_response.json
│   └── cluster_status.json
└── fixtures/               # Test fixtures and mocks
    └── mock_responses.json
```

## Usage

### In Robot Framework Tests

```robot
*** Settings ***
Variables    ${CURDIR}/../test-data/api/create_domain.json

*** Test Cases ***
Create Domain Test
    ${payload}=    Load JSON From File    ${CURDIR}/../test-data/api/create_domain.json
    ${response}=    POST    ${DDN_API}/domains    json=${payload}
```

### In Python Keywords

```python
import json
import os

def load_test_data(filename):
    """Load test data from test-data directory"""
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, '../test-data', filename)
    with open(file_path, 'r') as f:
        return json.load(f)
```

## Test Data Types

### 1. API Payloads
JSON files for API requests:
- Domain creation
- Namespace setup
- Quota configuration
- S3 bucket creation
- User provisioning

### 2. Test Files
Binary/text files for I/O tests:
- **Small:** 1KB - 1MB (quick tests)
- **Medium:** 1MB - 100MB (throughput tests)
- **Large:** 100MB - 10GB (stress tests)

### 3. Expected Results
JSON schemas for response validation:
- Health check responses
- Status API responses
- List/query responses

### 4. Credentials (NOT IN GIT)
Test user credentials:
- API keys
- S3 access keys
- OAuth tokens
- SSH keys

**⚠️ SECURITY:** Never commit credentials to git!

### 5. Fixtures
Mock data for testing:
- Simulated API responses
- Test database records
- Cache data

## Data Generation

For large test files, generate dynamically:

```bash
# Generate 1GB test file
dd if=/dev/urandom of=test-data/files/1gb_file.bin bs=1M count=1024

# Generate 100MB test file
python -c "with open('test-data/files/100mb_file.bin', 'wb') as f: f.write(b'0' * 100 * 1024 * 1024)"
```

## Data Cleanup

Test data in `test-data/files/` should be cleaned up:
- After test execution
- Before committing to git
- Use `.gitignore` for large files

## Best Practices

1. **Small Files:** Commit to git (<10MB)
2. **Large Files:** Generate dynamically or use external storage
3. **Credentials:** NEVER commit, use environment variables
4. **Sensitive Data:** Redact or anonymize
5. **Versioning:** Tag test data with version numbers

## .gitignore Rules

```gitignore
# Large test files
*.bin
*.dat
files/*.txt

# Credentials
credentials/*
!credentials/.gitignore

# Generated data
generated/
```
