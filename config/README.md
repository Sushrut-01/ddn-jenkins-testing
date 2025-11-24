# DDN Testing Framework - Configuration Files

This directory contains configuration files for different test environments and settings.

## Configuration Files

### 1. `environments.yaml`
Environment-specific settings (dev, staging, production):
```yaml
dev:
  exascaler_endpoint: http://exascaler.dev.ddn.local
  timeout: 30
staging:
  exascaler_endpoint: http://exascaler.staging.ddn.local
  timeout: 60
production:
  exascaler_endpoint: http://exascaler.ddn.local
  timeout: 120
```

### 2. `test_settings.yaml`
General test execution settings:
```yaml
test_execution:
  max_retries: 3
  retry_interval: 2s
  timeout: 30s
  parallel_execution: false
  
reporting:
  output_format: html
  include_screenshots: true
  log_level: INFO
```

### 3. `jenkins.yaml`
Jenkins-specific configuration:
```yaml
jenkins:
  job_name: DDN-Nightly-Tests
  cron_schedule: "H */6 * * *"
  build_retention: 10
  artifacts:
    - reports/*.html
    - reports/*.xml
```

### 4. `mongodb.yaml`
MongoDB Atlas configuration:
```yaml
mongodb:
  database: ddn_tests
  collection: test_failures
  connection_timeout: 5000
  retry_writes: true
```

## Usage

### In Robot Framework

```robot
*** Settings ***
Variables    ${CURDIR}/../config/test_settings.yaml

*** Test Cases ***
Test With Config
    Log    Max retries: ${test_execution}[max_retries]
```

### In Python

```python
import yaml
import os

def load_config(config_file):
    config_path = os.path.join(os.path.dirname(__file__), '../config', config_file)
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

# Usage
config = load_config('environments.yaml')
endpoint = config['dev']['exascaler_endpoint']
```

## Environment Selection

Select environment via environment variable:
```bash
export TEST_ENVIRONMENT=staging
python3 -m robot robot-tests/
```

## Best Practices

1. **Separate by concern:** One file per configuration type
2. **Environment isolation:** Different configs for dev/staging/prod
3. **No secrets:** Use environment variables for credentials
4. **Version control:** Commit configs (without secrets)
5. **Validation:** Validate config on load
