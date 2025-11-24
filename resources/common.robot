*** Settings ***
Documentation    Common resource file for DDN Storage testing
...              Contains reusable keywords, variables, and configurations
...              Import this file in your test suites for shared functionality

Library          BuiltIn
Library          Collections
Library          String
Library          DateTime
Library          OperatingSystem

*** Variables ***
# Test Configuration
${TEST_TIMEOUT}              30s
${API_TIMEOUT}               10s
${RETRY_INTERVAL}            2s
${MAX_RETRIES}               3

# Test Data Paths
${TEST_DATA_DIR}             ${CURDIR}/../test-data
${CONFIG_DIR}                ${CURDIR}/../config
${REPORTS_DIR}               ${CURDIR}/../reports

# DDN Endpoints (defaults - override with env vars)
${DEFAULT_EXASCALER_HOST}    exascaler.ddn.local
${DEFAULT_AI400X_HOST}       ai400x.ddn.local
${DEFAULT_INFINIA_HOST}      infinia.ddn.local
${DEFAULT_INTELLIFLASH_HOST} intelliflash.ddn.local

# HTTP Status Codes
${HTTP_OK}                   200
${HTTP_CREATED}              201
${HTTP_ACCEPTED}             202
${HTTP_NO_CONTENT}           204
${HTTP_BAD_REQUEST}          400
${HTTP_UNAUTHORIZED}         401
${HTTP_FORBIDDEN}            403
${HTTP_NOT_FOUND}            404
${HTTP_SERVER_ERROR}         500

# Test Data
@{TEST_FILE_SIZES}           1MB    10MB    100MB    1GB    10GB
@{STRIPE_COUNTS}             1      2       4        8      16
@{PARALLEL_STREAMS}          1      2       4        8      16      32

*** Keywords ***
Setup Test Environment
    [Documentation]    Common setup for all test suites
    Log    Setting up test environment    level=INFO
    ${build_id}=    Get Build ID
    Set Suite Variable    ${BUILD_ID}    ${build_id}
    ${timestamp}=    Get Current Timestamp
    Set Suite Variable    ${TEST_START_TIME}    ${timestamp}

Teardown Test Environment
    [Documentation]    Common teardown for all test suites
    ${timestamp}=    Get Current Timestamp
    ${duration}=    Subtract Date From Date    ${timestamp}    ${TEST_START_TIME}
    Log    Test suite completed in ${duration} seconds    level=INFO

Get Build ID
    [Documentation]    Get Jenkins BUILD_NUMBER or generate local ID
    ${build_id}=    Get Environment Variable    BUILD_NUMBER    default=local-${EMPTY}
    ${build_id}=    Set Variable If    '${build_id}' == 'local-${EMPTY}'
    ...    local-${TIMESTAMP}
    ...    ${build_id}
    RETURN    ${build_id}

Get Current Timestamp
    [Documentation]    Get current timestamp in epoch format
    ${timestamp}=    Get Current Date    result_format=epoch
    RETURN    ${timestamp}

Wait Until Service Ready
    [Documentation]    Wait until a service endpoint is responsive
    ...    Arguments:
    ...    - endpoint: URL to check
    ...    - timeout: Maximum wait time (default: 60s)
    ...    - interval: Check interval (default: 5s)
    [Arguments]    ${endpoint}    ${timeout}=60s    ${interval}=5s
    Wait Until Keyword Succeeds    ${timeout}    ${interval}
    ...    Check Service Health    ${endpoint}

Check Service Health
    [Documentation]    Check if service health endpoint returns 200
    [Arguments]    ${endpoint}
    ${response}=    Run Keyword And Return Status
    ...    Should Be Equal As Numbers    ${response.status_code}    200
    Should Be True    ${response}    Service ${endpoint} is not healthy

Retry On Failure
    [Documentation]    Retry a keyword multiple times on failure
    ...    Arguments:
    ...    - keyword: Keyword name to retry
    ...    - retries: Number of retry attempts (default: 3)
    ...    - interval: Wait between retries (default: 2s)
    ...    - *args: Arguments to pass to keyword
    [Arguments]    ${keyword}    ${retries}=${MAX_RETRIES}    ${interval}=${RETRY_INTERVAL}    @{args}
    Wait Until Keyword Succeeds    ${retries}x    ${interval}
    ...    Run Keyword    ${keyword}    @{args}

Generate Random String
    [Documentation]    Generate random alphanumeric string
    [Arguments]    ${length}=8
    ${random}=    Evaluate    ''.join(random.choices(string.ascii_lowercase + string.digits, k=${length}))    modules=random,string
    RETURN    ${random}

Generate Test File Name
    [Documentation]    Generate unique test file name with timestamp
    [Arguments]    ${prefix}=test    ${extension}=.dat
    ${timestamp}=    Get Current Date    result_format=%Y%m%d_%H%M%S
    ${random}=    Generate Random String    length=6
    ${filename}=    Set Variable    ${prefix}_${timestamp}_${random}${extension}
    RETURN    ${filename}

Convert Size To Bytes
    [Documentation]    Convert size string (1GB, 100MB) to bytes
    [Arguments]    ${size_string}
    ${size_string}=    Convert To Uppercase    ${size_string}
    ${value}=    Evaluate    int(''.join(filter(str.isdigit, '${size_string}')))
    ${unit}=    Evaluate    ''.join(filter(str.isalpha, '${size_string}'))
    
    ${bytes}=    Run Keyword If    '${unit}' == 'B'       Set Variable    ${value}
    ...    ELSE IF    '${unit}' == 'KB'      Evaluate    ${value} * 1024
    ...    ELSE IF    '${unit}' == 'MB'      Evaluate    ${value} * 1024 * 1024
    ...    ELSE IF    '${unit}' == 'GB'      Evaluate    ${value} * 1024 * 1024 * 1024
    ...    ELSE IF    '${unit}' == 'TB'      Evaluate    ${value} * 1024 * 1024 * 1024 * 1024
    ...    ELSE       Fail    Invalid size unit: ${unit}
    
    RETURN    ${bytes}

Verify Response Contains Key
    [Documentation]    Verify JSON response contains expected key
    [Arguments]    ${response}    ${key}
    ${data}=    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${data}    ${key}    Response missing key: ${key}

Verify Response Value
    [Documentation]    Verify JSON response key has expected value
    [Arguments]    ${response}    ${key}    ${expected_value}
    ${data}=    Set Variable    ${response.json()}
    ${actual_value}=    Get From Dictionary    ${data}    ${key}
    Should Be Equal    ${actual_value}    ${expected_value}
    ...    msg=Expected ${key}=${expected_value}, got ${actual_value}

Log Test Context
    [Documentation]    Log current test context for debugging
    Log    ========== TEST CONTEXT ==========    level=INFO
    Log    Test Name: ${TEST NAME}               level=INFO
    Log    Suite Name: ${SUITE NAME}             level=INFO
    Log    Build ID: ${BUILD_ID}                 level=INFO
    Log    Timestamp: ${TEST_START_TIME}         level=INFO
    Log    ==================================    level=INFO
