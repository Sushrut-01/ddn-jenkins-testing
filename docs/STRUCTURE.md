# DDN Testing Framework - Complete Structure Documentation

## 📁 Complete Directory Structure

```
ddn-jenkins-testing/
│
├── 📄 README.md                          # Main documentation
├── 📄 requirements.txt                   # Python dependencies
├── 📄 .env.example                       # Environment variables template
├── 📄 .gitignore                         # Git ignore rules
│
├── 📂 robot-tests/                       # ⭐ Test Suites
│   ├── ddn_basic_tests.robot            # 16 basic DDN storage tests
│   ├── ddn_advanced_tests.robot         # 7 advanced multi-tenancy tests
│   └── DDN_Keywords.py                  # Python keyword library
│
├── 📂 resources/                         # ⭐ Shared Resources
│   ├── common.robot                     # Common keywords & variables
│   ├── api_helpers.robot                # API testing helpers
│   └── validation.robot                 # Response validation keywords
│
├── 📂 implementation/                    # ⭐ MongoDB Integration
│   ├── __init__.py                      # Package init
│   ├── mongodb_robot_listener.py        # MongoDB failure reporter
│   └── security/                        # PII redaction (optional)
│
├── 📂 test-data/                         # ⭐ Test Data Files
│   ├── api/                             # API request payloads
│   │   ├── create_domain.json
│   │   ├── create_namespace.json
│   │   └── create_bucket.json
│   ├── files/                           # Test files for upload/download
│   │   ├── small_file.txt
│   │   ├── medium_file.dat
│   │   └── large_file.bin
│   ├── credentials/                     # ⚠️ NOT IN GIT
│   │   ├── .gitignore
│   │   └── README.md
│   └── expected/                        # Expected API responses
│       └── health_response.json
│
├── 📂 config/                            # ⭐ Configuration Files
│   ├── test_settings.yaml               # Test execution settings
│   ├── environments.yaml                # Environment configs
│   ├── jenkins.yaml                     # Jenkins settings
│   └── mongodb.yaml                     # MongoDB settings
│
├── 📂 libraries/                         # ⭐ Custom Python Libraries
│   ├── __init__.py
│   ├── DDNStorageLibrary.py             # Custom DDN library
│   ├── MongoDBHelpers.py                # MongoDB utilities
│   └── PerformanceMetrics.py            # Performance measurement
│
├── 📂 reports/                           # ⭐ Test Reports (Generated)
│   ├── .gitignore                       # Ignore generated reports
│   ├── .gitkeep                         # Keep directory
│   ├── README.md                        # Report documentation
│   ├── output.xml                       # Robot Framework XML (generated)
│   ├── log.html                         # Detailed HTML log (generated)
│   ├── report.html                      # Summary HTML report (generated)
│   └── screenshots/                     # Failure screenshots (generated)
│
├── 📂 scripts/                           # ⭐ Utility Scripts
│   ├── run-tests.sh                     # Execute tests (Linux)
│   ├── run-tests.bat                    # Execute tests (Windows)
│   ├── setup-environment.sh             # Environment setup
│   ├── cleanup.sh                       # Clean old reports
│   └── generate-test-data.py            # Generate test files
│
├── 📂 jenkins/                           # ⭐ Jenkins Configuration
│   ├── Jenkinsfile                      # Pipeline definition
│   ├── jenkins-job-config.xml           # Freestyle job config
│   ├── jenkins-build-script.sh          # Build script
│   └── README.md                        # Jenkins setup guide
│
└── 📂 docs/                              # ⭐ Documentation
    ├── ARCHITECTURE.md                  # Framework architecture
    ├── TEST_GUIDE.md                    # How to write tests
    ├── SETUP.md                         # Setup instructions
    ├── TROUBLESHOOTING.md               # Common issues
    └── API.md                           # API documentation
```

## 🎯 Key Components Explained

### 1. Test Suites (`robot-tests/`)
**Purpose:** Contains actual test cases  
**Files:**
- `*.robot` - Robot Framework test suites
- `DDN_Keywords.py` - Python-based custom keywords

**Report Types Generated:**
1. **output.xml** - Machine-readable test results
2. **log.html** - Detailed step-by-step execution log
3. **report.html** - High-level summary report
4. **screenshots/** - Visual evidence of failures
5. **xunit.xml** (optional) - JUnit format for CI/CD

### 2. Resources (`resources/`)
**Purpose:** Shared, reusable keywords and variables  
**Benefits:**
- Code reuse across test suites
- Centralized configuration
- Easier maintenance

### 3. Implementation (`implementation/`)
**Purpose:** MongoDB integration and custom listeners  
**Features:**
- Real-time failure reporting to MongoDB Atlas
- Test execution tracking
- PII redaction (optional)

### 4. Test Data (`test-data/`)
**Purpose:** Input data for tests  
**Categories:**
- **API payloads:** JSON request bodies
- **Test files:** Binary/text files for I/O tests
- **Credentials:** ⚠️ NEVER commit! (use env vars)
- **Expected results:** Validation data

### 5. Configuration (`config/`)
**Purpose:** Environment and execution settings  
**Files:**
- `test_settings.yaml` - General settings
- `environments.yaml` - Dev/Staging/Prod configs
- `jenkins.yaml` - CI/CD settings
- `mongodb.yaml` - Database config

### 6. Libraries (`libraries/`)
**Purpose:** Custom Python libraries for advanced functionality  
**Use Cases:**
- Complex API interactions
- Performance measurements
- Database operations
- Custom assertions

### 7. Reports (`reports/`)
**Purpose:** Store generated test reports  
**Auto-Generated After Each Run:**
```
reports/
├── output.xml          # Full test data (XML)
├── log.html            # Detailed execution log
├── report.html         # Summary dashboard
└── screenshots/        # Failure evidence
```

**Viewing:**
```bash
# Open in browser
start reports/report.html      # Windows
xdg-open reports/report.html   # Linux
open reports/report.html       # Mac
```

### 8. Scripts (`scripts/`)
**Purpose:** Automation and utility scripts  
**Examples:**
- Test execution wrapper
- Environment setup
- Test data generation
- Report archiving
- Cleanup utilities

### 9. Jenkins (`jenkins/`)
**Purpose:** CI/CD integration configuration  
**Files:**
- `Jenkinsfile` - Pipeline as code
- `jenkins-job-config.xml` - Job definition
- Build scripts and hooks

### 10. Documentation (`docs/`)
**Purpose:** Comprehensive project documentation  
**Topics:**
- Architecture overview
- Test writing guide
- Setup instructions
- Troubleshooting
- API reference

## 📊 Report Types in Detail

### 1. output.xml (Machine-Readable)
**Size:** Medium (100-500 KB)  
**Format:** XML  
**Content:**
- All test results
- Execution times
- Keywords executed
- Variables used
- Error messages

**Usage:**
- CI/CD parsing
- Trend analysis
- Report generation
- Custom dashboards

### 2. log.html (Detailed Log)
**Size:** Large (500 KB - 5 MB)  
**Format:** HTML with JavaScript  
**Content:**
- Step-by-step execution
- Expandable keyword hierarchy
- Arguments and return values
- Timing information
- Screenshots embedded
- Full error stack traces

**Usage:**
- Debugging
- Detailed analysis
- Understanding test flow

### 3. report.html (Summary Report)
**Size:** Medium (200-800 KB)  
**Format:** HTML  
**Content:**
- Pass/Fail statistics
- Test execution times
- Tag-based grouping
- Suite-level summary
- Trend graphs (if configured)

**Usage:**
- Quick overview
- Management reporting
- Build status verification

### 4. Screenshots (Visual Evidence)
**Size:** Variable (50-500 KB each)  
**Format:** PNG  
**Content:**
- Browser state at failure
- UI element visibility
- Error messages visible
- Timestamped filenames

**Usage:**
- Visual debugging
- UI issue identification
- Bug reports

### 5. xunit.xml (CI/CD Integration)
**Size:** Small (10-50 KB)  
**Format:** JUnit-compatible XML  
**Content:**
- Test names
- Pass/Fail status
- Execution times
- Error messages

**Usage:**
- Jenkins test result plugin
- CI/CD dashboards
- Historical tracking

## 🔧 Essential Testing Framework Components

### Minimum Required (Core)
1. ✅ Test suites (`robot-tests/`)
2. ✅ Test execution script (`scripts/run-tests.sh`)
3. ✅ Dependencies (`requirements.txt`)
4. ✅ Environment config (`.env.example`)
5. ✅ Documentation (`README.md`)

### Recommended (Professional)
6. ✅ Shared resources (`resources/`)
7. ✅ Test data (`test-data/`)
8. ✅ Configuration (`config/`)
9. ✅ Reports directory (`reports/`)
10. ✅ CI/CD integration (`jenkins/`)

### Advanced (Enterprise)
11. ✅ Custom libraries (`libraries/`)
12. ✅ MongoDB integration (`implementation/`)
13. ✅ Comprehensive docs (`docs/`)
14. ✅ Utility scripts (`scripts/`)
15. ✅ Security features (PII redaction)

## 🚀 Quick Reference

### Run Tests
```bash
# All tests
python3 -m robot --outputdir reports robot-tests/

# Specific suite
python3 -m robot --outputdir reports robot-tests/ddn_basic_tests.robot

# With tags
python3 -m robot --outputdir reports --include critical robot-tests/

# With MongoDB listener
python3 -m robot --outputdir reports \
    --listener implementation.mongodb_robot_listener.MongoDBListener \
    robot-tests/
```

### View Reports
```bash
# Summary report
start reports/report.html

# Detailed log
start reports/log.html

# Raw XML
cat reports/output.xml
```

### Generate Test Data
```bash
# 100MB test file
python scripts/generate-test-data.py --size 100MB --output test-data/files/

# API payloads
python scripts/generate-api-payloads.py --tenant tenant1
```

### Jenkins Execution
```bash
# Trigger build
java -jar jenkins-cli.jar -s http://localhost:8081/ build DDN-Nightly-Tests

# View console
java -jar jenkins-cli.jar -s http://localhost:8081/ console DDN-Nightly-Tests 4
```

## 📈 Report Locations

### Local Development
- **Reports:** `./reports/`
- **Logs:** `./reports/log.html`
- **Screenshots:** `./reports/screenshots/`

### Jenkins
- **Artifacts:** Build → Build Artifacts → reports/
- **Console:** Build → Console Output
- **Test Results:** Build → Test Result

### MongoDB Atlas
- **Dashboard:** http://localhost:5173
- **API:** http://localhost:5006/api/failures
- **Collection:** `ddn_tests.test_failures`

---

**Last Updated:** November 24, 2025  
**Framework Version:** 1.0.0  
**Total Directories:** 10  
**Total Files:** 25+
