# Credentials Directory

⚠️ **SECURITY WARNING:** This directory should NEVER be committed to git!

## Purpose

Store test credentials and secrets that should not be in version control:
- API keys
- Access tokens
- SSH private keys
- Database passwords
- S3 access keys
- OAuth client secrets

## Usage

### Load from Environment Variables (Recommended)

```robot
*** Settings ***
Library    OperatingSystem

*** Test Cases ***
Test With Credentials
    ${api_key}=    Get Environment Variable    DDN_API_KEY
    ${api_secret}=    Get Environment Variable    DDN_API_SECRET
```

### Load from File (Local Testing Only)

```python
# In Python keyword library
import json
import os

def load_credentials(credential_file):
    creds_path = os.path.join(os.path.dirname(__file__), '../test-data/credentials', credential_file)
    with open(creds_path, 'r') as f:
        return json.load(f)
```

## File Structure (Examples)

**api_credentials.json:**
```json
{
  "api_key": "your-api-key",
  "api_secret": "your-secret"
}
```

**s3_credentials.json:**
```json
{
  "access_key_id": "AKIAIOSFODNN7EXAMPLE",
  "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}
```

## Best Practices

1. **Never commit** credentials to git
2. **Use environment variables** in CI/CD
3. **Rotate credentials** regularly
4. **Use different credentials** for each environment
5. **Encrypt sensitive files** if must store locally

## .gitignore

This entire directory is ignored by git (see parent `.gitignore`)
