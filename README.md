# DDN Jenkins Testing Framework

**Automated Robot Framework Testing Suite for DDN Storage Products**

This repository contains the complete testing infrastructure for Jenkins CI/CD automation of DDN storage product testing.

## 🏗️ Project Structure

```
ddn-jenkins-testing/
├── robot-tests/              # Robot Framework test suites
│   ├── ddn_basic_tests.robot      # Basic DDN storage tests
│   ├── ddn_advanced_tests.robot   # Advanced multi-tenancy tests
│   └── DDN_Keywords.py            # Python keywords library
├── implementation/           # MongoDB listener and utilities
│   ├── __init__.py                # Package init
│   └── mongodb_robot_listener.py  # MongoDB failure reporter
├── reports/                  # Test execution reports
│   └── .gitkeep
├── jenkins/                  # Jenkins configuration
│   ├── Jenkinsfile               # Pipeline definition
│   └── jenkins-job-config.xml    # Job configuration
├── scripts/                  # Build and utility scripts
│   ├── run-tests.sh             # Linux test execution
│   └── setup-environment.sh     # Environment setup
├── .env.example              # Environment variables template
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 📋 Test Suites

### Basic Tests (16 test cases)
- **EXAScaler Tests (4)**: Lustre connectivity, cluster status, throughput, striped files
- **AI400X Tests (4)**: Storage platform, GPU optimization, model checkpoints, data loading
- **Infinia Tests (4)**: Orchestration, LLM training, checkpointing, edge-core-cloud
- **IntelliFlash Tests (3)**: System connectivity, flash CRUD, deduplication
- **Integration Test (1)**: Full AI training pipeline

### Advanced Tests (7 test cases)
- **Multi-Tenancy (4)**: Domain isolation, namespace isolation, quota management, usage stats
- **S3 Security (2)**: Bucket isolation, cross-tenant access prevention
- **Audit (1)**: Tenant operation logging

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Jenkins with Docker support
- MongoDB Atlas account
- DDN Storage infrastructure access

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/Sushrut-01/ddn-jenkins-testing.git
cd ddn-jenkins-testing
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your MongoDB URI and DDN endpoints
```

4. **Run tests locally:**
```bash
python3 -m robot --outputdir reports --listener implementation.mongodb_robot_listener.MongoDBListener robot-tests/
```

## 🔧 Jenkins Integration

### Jenkins Job Setup

1. **Create Freestyle Project** named `DDN-Nightly-Tests`

2. **Source Code Management:**
   - Repository: `https://github.com/Sushrut-01/ddn-jenkins-testing.git`
   - Branch: `main`

3. **Build Steps** → Execute shell:
```bash
#!/bin/bash
python3 -m pip install --quiet --upgrade pip --break-system-packages
python3 -m pip install --quiet --break-system-packages robotframework pymongo python-dotenv boto3 requests

export MONGODB_URI='mongodb+srv://username:password@cluster.mongodb.net/ddn_tests?retryWrites=true&w=majority'
export JOB_NAME="$JOB_NAME"
export BUILD_NUMBER="$BUILD_NUMBER"

python3 -m robot --outputdir reports --listener implementation.mongodb_robot_listener.MongoDBListener robot-tests/
```

4. **Schedule (optional):**
   - Build Triggers → Build periodically
   - Schedule: `H */6 * * *` (every 6 hours)

### Cron Schedule Examples
```
*/10 * * * *    # Every 10 minutes (testing)
H */6 * * *     # Every 6 hours (regular)
H 0 * * *       # Daily at midnight
H 0 * * 1       # Weekly on Monday
```

## 📊 MongoDB Integration

Tests automatically report failures to MongoDB Atlas via the Robot Framework listener.

**Collections:**
- `test_failures`: Failed test cases with full context
- Build tracking with unique IDs
- Timestamps for trend analysis

**Dashboard Integration:**
- API: http://localhost:5006
- UI: http://localhost:5173

## 🧪 Test Execution

### Local Execution
```bash
# Run all tests
python3 -m robot --outputdir reports robot-tests/

# Run specific suite
python3 -m robot --outputdir reports robot-tests/ddn_basic_tests.robot

# Run with tags
python3 -m robot --outputdir reports --include critical robot-tests/

# Dry run (validation)
python3 -m robot --dryrun robot-tests/
```

### Jenkins Execution
- Manual: Click "Build Now" in Jenkins UI
- CLI: `java -jar jenkins-cli.jar -s http://localhost:8081/ build DDN-Nightly-Tests`
- Scheduled: Automatic via cron trigger

## 📝 Environment Variables

Required environment variables:

```bash
# MongoDB Configuration
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/ddn_tests
MONGODB_DB=ddn_tests

# DDN Endpoints
DDN_EXASCALER_ENDPOINT=http://exascaler.ddn.local
DDN_AI400X_ENDPOINT=http://ai400x.ddn.local
DDN_INFINIA_ENDPOINT=http://infinia.ddn.local
DDN_INTELLIFLASH_ENDPOINT=http://intelliflash.ddn.local
DDN_EMF_ENDPOINT=http://emf.ddn.local
DDN_S3_ENDPOINT=http://s3.exascaler.ddn.local

# API Credentials
DDN_API_KEY=your-api-key
DDN_API_SECRET=your-api-secret
DDN_S3_ACCESS_KEY=your-s3-access-key
DDN_S3_SECRET_KEY=your-s3-secret-key

# Jenkins Variables (auto-populated)
JOB_NAME=$JOB_NAME
BUILD_NUMBER=$BUILD_NUMBER
BUILD_URL=$BUILD_URL
GIT_COMMIT=$GIT_COMMIT
GIT_BRANCH=$GIT_BRANCH
```

## 📈 Test Reports

After execution, reports are generated in the `reports/` directory:

- `output.xml`: Machine-readable test results
- `log.html`: Detailed test execution log
- `report.html`: Summary report with statistics

View reports:
```bash
# Open report in browser (Linux)
xdg-open reports/report.html

# Windows
start reports/report.html

# Mac
open reports/report.html
```

## 🔍 Troubleshooting

### Common Issues

1. **"Get Environment Variable" error**
   - **Fix:** Ensure `Library    BuiltIn` is in test Settings

2. **MongoDB connection failed**
   - **Fix:** Check MONGODB_URI encoding (@ must be %40)
   - Use single quotes in bash: `export MONGODB_URI='...'`

3. **Import error: No module named 'implementation'**
   - **Fix:** Ensure `implementation/__init__.py` exists

4. **Tests fail: Connection refused**
   - **Fix:** DDN infrastructure must be accessible from Jenkins
   - Check network connectivity and DNS resolution

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -am 'Add new test suite'`
4. Push to branch: `git push origin feature/my-feature`
5. Create Pull Request

## 📄 License

Copyright © 2025 DDN Storage. All rights reserved.

## 📞 Support

For issues or questions:
- GitHub Issues: https://github.com/Sushrut-01/ddn-jenkins-testing/issues
- Email: support@ddn.com

---

**Last Updated:** November 24, 2025
**Version:** 1.0.0
**Jenkins Compatible:** 2.x+
**Robot Framework:** 7.3.2+
**Python:** 3.13+
