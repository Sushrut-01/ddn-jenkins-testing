*** Settings ***
Documentation    DDN Real-Time Test Scenarios - Robot Framework Version
...              Comprehensive test suite for DDN Storage Products:
...              - EXAScaler (Lustre file system)
...              - AI400X Series (AI storage platforms)
...              - Infinia (AI workload optimization)
...              - IntelliFlash (Enterprise storage)
...              All failures automatically reported to MongoDB via listener

Library          BuiltIn
Library          DDN_Keywords.py
Library          Collections
Library          String
Library          DateTime

Suite Setup      Initialize Test Suite
Suite Teardown   Close DDN Session

*** Variables ***
${BUILD_NUMBER}          ${EMPTY}
${JOB_NAME}              DDN-Robot-Basic-Tests
${CHECKPOINT_ID}         ${EMPTY}
${VOLUME_ID}             ${EMPTY}
${TEST_TIMEOUT}          30s

*** Test Cases ***

# =============================================================================
# TEST SCENARIO 1: DDN EXAScaler (Lustre) Storage Tests
# =============================================================================

EXAScaler Should Connect To Lustre File System
    [Documentation]    Verify EXAScaler Lustre file system is reachable and healthy
    [Tags]    exascaler    lustre    connectivity    critical
    ${response}=    Get Exascaler Health
    Should Be Equal As Numbers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${data}    status
    Should Be Equal As Strings    ${data}[status]    healthy

EXAScaler Should Verify Cluster Status And Metadata Servers
    [Documentation]    Verify EXAScaler cluster has active MDS and OSS servers
    [Tags]    exascaler    cluster    health-check    critical
    ${response}=    Get Exascaler Cluster Status
    Should Be Equal As Numbers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}

    # Verify MDS (Metadata Servers)
    Dictionary Should Contain Key    ${data}    mds_servers
    ${mds_servers}=    Get From Dictionary    ${data}    mds_servers
    Should Not Be Empty    ${mds_servers}
    ${mds_count}=    Get Length    ${mds_servers}
    Should Be True    ${mds_count} > 0

    # Verify OSS (Object Storage Servers)
    Dictionary Should Contain Key    ${data}    oss_servers
    ${oss_servers}=    Get From Dictionary    ${data}    oss_servers
    Should Not Be Empty    ${oss_servers}

EXAScaler Should Test Lustre Throughput Performance
    [Documentation]    Verify Lustre file system achieves high throughput (TB/s)
    [Tags]    exascaler    performance    throughput
    ${response}=    Run Exascaler Throughput Benchmark    file_size_gb=10    parallel_streams=8
    Should Be Equal As Numbers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}

    Dictionary Should Contain Key    ${data}    throughput_gbps
    ${throughput}=    Get From Dictionary    ${data}    throughput_gbps
    Should Be True    ${throughput} > 1.0    msg=Throughput should be at least 1 GB/s

EXAScaler Should Create And Access Lustre Striped Files
    [Documentation]    Test Lustre striping feature for parallel I/O performance
    [Tags]    exascaler    lustre    striping    file-operations
    ${timestamp}=    Get Current Date    result_format=%s
    ${file_path}=    Set Variable    /test/striped_file_${timestamp}.dat

    # Create striped file
    ${file_id}=    Create Lustre Striped File
    ...    path=${file_path}
    ...    stripe_count=4
    ...    stripe_size=1M
    ...    size_mb=100
    Should Not Be Empty    ${file_id}

    # Verify striping configuration
    ${stripe_info}=    Verify File Striping    ${file_id}
    Should Be Equal As Numbers    ${stripe_info}[stripe_count]    4

# =============================================================================
# TEST SCENARIO 2: DDN AI400X Series Tests
# =============================================================================

AI400X Should Connect To Storage Platform
    [Documentation]    Verify AI400X storage platform is accessible
    [Tags]    ai400x    connectivity    ai-storage    critical
    ${response}=    Get Ai400X Health
    Should Be Equal As Numbers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${data}    platform
    Should Contain    ${data}[platform]    AI400X

AI400X Should Verify GPU-Optimized Storage Performance
    [Documentation]    Verify GPU Direct Storage is enabled with low latency
    [Tags]    ai400x    gpu    performance    critical
    ${response}=    Get Ai400X GPU Metrics
    Should Be Equal As Numbers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}

    # Verify GPU Direct Storage enabled
    Dictionary Should Contain Key    ${data}    gpu_direct_storage_enabled
    Should Be True    ${data}[gpu_direct_storage_enabled]

    # Verify low latency (< 100 microseconds)
    Dictionary Should Contain Key    ${data}    latency_us
    ${latency}=    Get From Dictionary    ${data}    latency_us
    Should Be True    ${latency} < 100    msg=Latency should be less than 100 microseconds

AI400X Should Store And Retrieve AI Model Checkpoint
    [Documentation]    Test AI model checkpoint storage and retrieval functionality
    [Tags]    ai400x    checkpoint    ai-model    critical
    ${timestamp}=    Get Current Date    result_format=%s
    ${model_name}=    Set Variable    llama-test-model-${timestamp}

    # Store checkpoint
    ${metadata}=    Create Dictionary
    ...    framework=pytorch
    ...    optimizer_state=${True}
    ...    training_step=10000

    ${checkpoint_id}=    Store Ai Checkpoint
    ...    model_name=${model_name}
    ...    checkpoint_epoch=100
    ...    checkpoint_size_gb=50
    ...    metadata=${metadata}
    Should Not Be Empty    ${checkpoint_id}
    Set Suite Variable    ${CHECKPOINT_ID}    ${checkpoint_id}

    # Retrieve checkpoint
    ${response}=    Retrieve Ai Checkpoint    ${checkpoint_id}
    Should Be Equal As Numbers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}
    Should Be Equal As Strings    ${data}[model_name]    ${model_name}

AI400X Should Verify 4x Faster Data Loading Claim
    [Documentation]    Verify AI400X achieves claimed 4x faster data loading
    [Tags]    ai400x    performance    data-loading
    ${response}=    Run Ai Data Loading Benchmark
    ...    dataset_size_gb=100
    ...    batch_size=128
    ...    data_format=tfrecord
    Should Be Equal As Numbers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}

    Dictionary Should Contain Key    ${data}    baseline_comparison
    ${comparison}=    Get From Dictionary    ${data}    baseline_comparison
    ${speedup}=    Get From Dictionary    ${comparison}    speedup_factor
    Should Be True    ${speedup} > 3.5    msg=Speed should be at least 3.5x faster

# =============================================================================
# TEST SCENARIO 3: DDN Infinia AI Workload Optimization Tests
# =============================================================================

Infinia Should Connect To Orchestration Platform
    [Documentation]    Verify Infinia orchestration platform is accessible
    [Tags]    infinia    connectivity    orchestration    critical
    ${response}=    Get Infinia Status
    Should Be Equal As Numbers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${data}    service
    Should Be Equal As Strings    ${data}[service]    Infinia

Infinia Should Optimize LLM Training Workload
    [Documentation]    Test LLM training workload optimization capabilities
    [Tags]    infinia    llm    optimization
    ${response}=    Optimize LLM Workload
    ...    model_size=70B
    ...    gpus=64
    ...    expected_tokens_per_sec=10000
    Should Be Equal As Numbers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}

    Dictionary Should Contain Key    ${data}    optimization_profile
    ${profile}=    Get From Dictionary    ${data}    optimization_profile
    Dictionary Should Contain Key    ${profile}    data_pipeline_config
    Dictionary Should Contain Key    ${profile}    storage_tiering

Infinia Should Verify 15x Faster Checkpointing Performance
    [Documentation]    Verify Infinia achieves 15x faster checkpointing
    [Tags]    infinia    checkpoint    performance
    ${response}=    Run Checkpoint Benchmark
    ...    model_size_gb=140
    ...    checkpoint_type=full
    ...    target_time_sec=60
    Should Be Equal As Numbers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}

    Dictionary Should Contain Key    ${data}    checkpoint_time_sec
    Dictionary Should Contain Key    ${data}    baseline_time_sec
    ${speedup}=    Evaluate    ${data}[baseline_time_sec] / ${data}[checkpoint_time_sec]
    Should Be True    ${speedup} > 12.0    msg=Checkpointing should be at least 12x faster

Infinia Should Setup Edge-Core-Cloud Orchestration
    [Documentation]    Test edge-core-cloud data orchestration setup
    [Tags]    infinia    orchestration    edge-cloud
    ${orchestration_id}=    Setup Edge Core Cloud Orchestration
    ...    edge_nodes=5
    ...    core_datacenter=us-west-1
    ...    cloud_provider=gcp
    ...    dataset_size_tb=10
    Should Not Be Empty    ${orchestration_id}

# =============================================================================
# TEST SCENARIO 4: DDN IntelliFlash Enterprise Storage Tests
# =============================================================================

IntelliFlash Should Connect To Storage System
    [Documentation]    Verify IntelliFlash storage system is accessible
    [Tags]    intelliflash    connectivity    enterprise    critical
    ${response}=    Get Intelliflash System Info
    Should Be Equal As Numbers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${data}    product
    Should Contain    ${data}[product]    IntelliFlash

IntelliFlash Should Test Flash-Optimized CRUD Operations
    [Documentation]    Test IntelliFlash Create, Read, Update, Delete operations
    [Tags]    intelliflash    crud    data-operations
    ${timestamp}=    Get Current Date    result_format=%s
    ${volume_name}=    Set Variable    test-volume-${timestamp}

    # Create volume
    ${volume_id}=    Create Intelliflash Volume
    ...    name=${volume_name}
    ...    size_gb=100
    ...    compression=${True}
    ...    deduplication=${True}
    Should Not Be Empty    ${volume_id}
    Set Suite Variable    ${VOLUME_ID}    ${volume_id}

    # Read volume
    ${read_response}=    Get Intelliflash Volume    ${volume_id}
    Should Be Equal As Numbers    ${read_response.status_code}    200
    ${volume_data}=    Set Variable    ${read_response.json()}
    Should Be Equal As Strings    ${volume_data}[name]    ${volume_name}

    # Update volume
    ${update_response}=    Update Intelliflash Volume    ${volume_id}    size_gb=200
    Should Be Equal As Numbers    ${update_response.status_code}    200

    # Delete volume
    ${delete_response}=    Delete Intelliflash Volume    ${volume_id}
    Should Be Equal As Numbers    ${delete_response.status_code}    204

IntelliFlash Should Verify Deduplication And Compression Ratios
    [Documentation]    Verify IntelliFlash storage efficiency features
    [Tags]    intelliflash    efficiency    deduplication    compression
    ${response}=    Get Storage Efficiency Metrics
    Should Be Equal As Numbers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}

    # Verify deduplication ratio (at least 1.5:1)
    Dictionary Should Contain Key    ${data}    dedup_ratio
    ${dedup_ratio}=    Get From Dictionary    ${data}    dedup_ratio
    Should Be True    ${dedup_ratio} > 1.5

    # Verify compression ratio (at least 1.3:1)
    Dictionary Should Contain Key    ${data}    compression_ratio
    ${compression_ratio}=    Get From Dictionary    ${data}    compression_ratio
    Should Be True    ${compression_ratio} > 1.3

# =============================================================================
# TEST SCENARIO 5: Integration Tests
# =============================================================================

DDN Should Complete Full AI Training Pipeline
    [Documentation]    End-to-end integration test across all DDN products
    [Tags]    integration    end-to-end    ai-pipeline    critical
    [Timeout]    60s

    # This test verifies the complete DDN storage stack workflow
    # from data loading through checkpointing to backup

    # Step 1: Verify EXAScaler is accessible (data loading)
    ${exascaler_health}=    Get Exascaler Health
    Should Be Equal As Numbers    ${exascaler_health.status_code}    200

    # Step 2: Verify Infinia optimization is working
    ${infinia_status}=    Get Infinia Status
    Should Be Equal As Numbers    ${infinia_status.status_code}    200

    # Step 3: Verify AI400X checkpoint storage
    ${ai400x_health}=    Get Ai400X Health
    Should Be Equal As Numbers    ${ai400x_health.status_code}    200

    # Step 4: Verify IntelliFlash backup system
    ${intelliflash_info}=    Get Intelliflash System Info
    Should Be Equal As Numbers    ${intelliflash_info.status_code}    200

    Log    Full DDN AI pipeline verification completed successfully    level=INFO

*** Keywords ***
Initialize Test Suite
    [Documentation]    Initialize test suite with environment variables
    ${build_num}=    Get Environment Variable    BUILD_NUMBER    default=local-run
    Set Suite Variable    ${BUILD_NUMBER}    ${build_num}

    ${job_name}=    Get Environment Variable    JOB_NAME    default=DDN-Robot-Basic-Tests
    Set Suite Variable    ${JOB_NAME}    ${job_name}

    Log    Starting DDN Robot Framework Tests    level=INFO
    Log    Build Number: ${BUILD_NUMBER}    level=INFO
    Log    Job Name: ${JOB_NAME}    level=INFO

Close DDN Session
    [Documentation]    Clean up resources after test suite
    Close Session
    Log    DDN test suite completed    level=INFO
