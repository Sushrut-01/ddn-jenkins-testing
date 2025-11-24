# Python Testing with Robot Framework - Complete Guide

## 🐍 Python + Robot Framework Integration

Robot Framework is a **Python-based** testing framework. All keywords can be written in Python.

## 📋 Test Report Types Generated

### Automatic Reports (No Configuration Needed)

When you run:
```bash
python3 -m robot --outputdir reports robot-tests/
```

**5 Report Types Generated:**

### 1. **output.xml** (XML Report)
```
reports/output.xml
```
- **Format:** XML (JUnit compatible)
- **Size:** 100-500 KB
- **Contains:**
  - All test results
  - Execution times
  - Keywords executed
  - Error messages
  - Variable values
- **Used By:**
  - Jenkins Test Result plugin
  - CI/CD dashboards
  - Report parsers
  - Trend analysis tools

**Example Structure:**
```xml
<robot>
  <suite name="DDN Basic Tests">
    <test name="EXAScaler Should Connect">
      <status status="FAIL" starttime="..." endtime="...">
        ConnectionError: ...
      </status>
    </test>
  </suite>
</robot>
```

### 2. **log.html** (Detailed Console Log)
```
reports/log.html
```
- **Format:** HTML with JavaScript
- **Size:** 500 KB - 5 MB
- **Contains:**
  - Step-by-step execution
  - Expandable keyword tree
  - Arguments and return values
  - Timing for each keyword
  - Screenshots embedded
  - Full stack traces
  - Console output

**Features:**
- ✅ Search functionality
- ✅ Expand/collapse all
- ✅ Filter by test status
- ✅ Direct links to failures

### 3. **report.html** (Summary Dashboard)
```
reports/report.html
```
- **Format:** HTML
- **Size:** 200-800 KB
- **Contains:**
  - Test statistics (pass/fail)
  - Execution times
  - Tag-based grouping
  - Suite-level results
  - Charts and graphs

**Example View:**
```
=====================================
Test Statistics by Tag
=====================================
Critical Tests    7 failed, 0 passed
High Priority    16 failed, 0 passed
-------------------------------------
Total            23 failed, 0 passed
```

### 4. **Console Output** (Real-time Log)
```
Terminal stdout or Jenkins Console Output
```
- **Format:** Plain text
- **Contains:**
  - Real-time test execution
  - Print statements
  - MongoDB Listener messages
  - Installation logs
  - Error messages

**Example:**
```
Running Robot Framework tests...
==============================================================================
Robot-Tests :: DDN Test Suites
==============================================================================
[MongoDB Listener] Connected to MongoDB: ddn_tests
[MongoDB Listener] ✓ Failure stored: Test Name (ID: 123)
Test Case Name | FAIL |
ConnectionError: ...
==============================================================================
23 tests, 0 passed, 23 failed
==============================================================================
```

### 5. **Screenshots/** (Visual Evidence)
```
reports/screenshots/selenium-screenshot-*.png
```
- **Format:** PNG images
- **Generated:** On test failure (if using Browser/Selenium library)
- **Size:** 50-500 KB each
- **Naming:** `selenium-screenshot-{timestamp}.png`

## 🔧 Python Keyword Library Example

**DDN_Keywords.py** (Already in framework):
```python
import os
import requests
from robot.api import logger

class DDN_Keywords:
    """Python-based Robot Framework keywords"""
    
    ROBOT_LIBRARY_SCOPE = 'SUITE'
    
    def __init__(self):
        self.endpoint = os.getenv('DDN_ENDPOINT', 'http://ddn.local')
    
    def get_exascaler_health(self):
        """
        Get EXAScaler health status
        Returns response object
        """
        url = f"{self.endpoint}/api/v1/health"
        response = requests.get(url)
        logger.info(f"Health check: {response.status_code}")
        return response
```

## 📊 Viewing Reports

### Local Development
```bash
# Windows
start reports/report.html
start reports/log.html

# Linux
xdg-open reports/report.html

# Mac
open reports/report.html
```

### Jenkins
- **Console Log:** Build → Console Output
- **Test Results:** Build → Test Result
- **HTML Reports:** Build → Build Artifacts → reports/
- **XML:** Parsed by Robot Framework Plugin

## 🎯 Report Generation Commands

### Basic Execution
```bash
# Generate all default reports
python3 -m robot --outputdir reports robot-tests/
```

### With Timestamps
```bash
# Add timestamp to report filenames
python3 -m robot --outputdir reports --timestampoutputs robot-tests/
```

### Custom Report Names
```bash
python3 -m robot \
    --outputdir reports \
    --output custom_output.xml \
    --log custom_log.html \
    --report custom_report.html \
    robot-tests/
```

### With XUnit Format (Additional)
```bash
# Also generate xunit.xml for Jenkins
python3 -m robot \
    --outputdir reports \
    --xunit xunit.xml \
    robot-tests/
```

### Combine Multiple Runs
```bash
# Merge multiple test run XMLs
rebot --outputdir reports \
    run1/output.xml \
    run2/output.xml \
    run3/output.xml
```

## 📈 MongoDB Reports (6th Report Type)

In addition to Robot Framework's 5 standard reports, our framework adds:

### 6. **MongoDB Atlas Storage**
```python
# Configured in implementation/mongodb_robot_listener.py
```

**Collection:** `test_failures`

**Document Structure:**
```json
{
  "_id": "69242648f804239dc435506b",
  "test_name": "Domain Should Create...",
  "suite_name": "Ddn Advanced Tests",
  "status": "FAIL",
  "error_message": "ConnectionError: ...",
  "timestamp": "2025-11-24T09:21:15.123Z",
  "build_id": "3",
  "job_name": "DDN-Nightly-Tests",
  "duration_ms": 234,
  "tags": ["multi-tenancy", "domain"]
}
```

**Access:**
- Dashboard: http://localhost:5173
- API: http://localhost:5006/api/failures
- MongoDB Compass: Direct connection

## 🔍 Report Locations

### After Test Run
```
reports/
├── output.xml          ← XML report (JUnit compatible)
├── log.html            ← Detailed execution log
├── report.html         ← Summary dashboard
└── screenshots/        ← Failure screenshots
    └── selenium-screenshot-*.png
```

### In Jenkins
```
Jenkins Build #4
├── Console Output      ← Real-time console log
├── Test Result         ← Parsed from output.xml
└── Build Artifacts
    └── reports/
        ├── output.xml
        ├── log.html
        └── report.html
```

### In MongoDB
```
MongoDB Atlas
└── ddn_tests (database)
    └── test_failures (collection)
        ├── Document 1 (Build #3)
        ├── Document 2 (Build #3)
        └── ... (856+ documents)
```

## 🎯 Complete Report Summary

| # | Report Type | Format | Size | Generated By | Location |
|---|-------------|--------|------|--------------|----------|
| 1 | output.xml | XML | 100-500KB | Robot Framework | `reports/output.xml` |
| 2 | log.html | HTML+JS | 500KB-5MB | Robot Framework | `reports/log.html` |
| 3 | report.html | HTML | 200-800KB | Robot Framework | `reports/report.html` |
| 4 | Console | Text | Varies | Robot Framework | Jenkins Console |
| 5 | Screenshots | PNG | 50-500KB ea | Robot Framework | `reports/screenshots/` |
| 6 | MongoDB | JSON | ~1KB ea | Custom Listener | MongoDB Atlas |

**Total:** 6 comprehensive report types covering all testing needs!

## ✅ What You Get

### Immediate (After Test Run)
- ✅ XML report for CI/CD
- ✅ HTML detailed log for debugging
- ✅ HTML summary for quick overview
- ✅ Console output for real-time monitoring
- ✅ Screenshots for visual debugging

### Long-term (MongoDB)
- ✅ Historical failure tracking
- ✅ Trend analysis
- ✅ Dashboard visualization
- ✅ API access for custom reports

## 🚀 Quick Start

```bash
# 1. Run tests
cd ddn-jenkins-testing
python3 -m robot --outputdir reports --listener implementation.mongodb_robot_listener.MongoDBListener robot-tests/

# 2. View HTML reports
start reports/report.html

# 3. Check MongoDB
# Visit: http://localhost:5173

# 4. View console log
# Scroll up in terminal
```

---

**Framework Ready!** All 6 report types configured and working! 🎉
