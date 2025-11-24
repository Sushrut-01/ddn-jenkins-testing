"""
Robot Framework Listener for MongoDB Integration
Automatically sends test failures to MongoDB Atlas during test execution
Phase 4: Now includes PII redaction before storage
"""

import os
import sys
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import traceback

# Phase 4: Add security module to path
security_dir = os.path.join(os.path.dirname(__file__), 'security')
sys.path.insert(0, security_dir)

# Phase 4: Import PII redaction
try:
    from pii_redaction import get_pii_redactor
    PII_REDACTION_AVAILABLE = True
except ImportError:
    PII_REDACTION_AVAILABLE = False
    print("[MongoDB Listener] WARNING: PII redaction not available")

# Load environment variables
load_dotenv()

class MongoDBListener:
    """
    Robot Framework listener that sends test failures to MongoDB
    """

    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        """Initialize MongoDB connection"""
        try:
            self.mongodb_uri = os.getenv('MONGODB_URI')
            self.mongodb_db = os.getenv('MONGODB_DB', 'ddn_tests')

            if not self.mongodb_uri:
                print("[MongoDB Listener] ERROR: MONGODB_URI not configured")
                self.client = None
                return

            self.client = MongoClient(self.mongodb_uri)
            self.db = self.client[self.mongodb_db]
            self.collection = self.db['test_failures']

            # Test connection
            self.client.server_info()
            print(f"[MongoDB Listener] Connected to MongoDB: {self.mongodb_db}")

            # Store current suite and test context
            self.current_suite = None
            self.current_suite_stats = None  # BUG FIX: Track suite statistics
            self.current_test = None
            self.build_number = os.getenv('BUILD_NUMBER', 'local')
            self.job_name = os.getenv('JOB_NAME', 'robot-framework-tests')

            # Phase 4: Initialize PII redactor
            self.pii_redactor = None
            pii_enabled = os.getenv('PII_REDACTION_ENABLED', 'false').lower() == 'true'

            if not pii_enabled:
                print("[MongoDB Listener] ℹ️  PII redaction DISABLED (client approval pending)")
                print("[MongoDB Listener] ℹ️  Storing actual data for dashboard navigation")
            elif PII_REDACTION_AVAILABLE:
                try:
                    self.pii_redactor = get_pii_redactor()
                    print("[MongoDB Listener] ✓ PII redaction ENABLED")
                except Exception as e:
                    print(f"[MongoDB Listener] WARNING: PII redaction failed to initialize: {e}")
            else:
                print("[MongoDB Listener] WARNING: PII redaction disabled - install presidio packages")

        except Exception as e:
            print(f"[MongoDB Listener] Connection error: {str(e)}")
            self.client = None

    def start_suite(self, data, result):
        """Called when a test suite starts"""
        self.current_suite = result.name
        # BUG FIX: Initialize suite stats tracking
        self.current_suite_stats = {
            'suite_name': result.name,
            'pass_count': 0,
            'fail_count': 0,
            'total_count': 0
        }
        print(f"[MongoDB Listener] Suite started: {result.name}")

    def start_test(self, data, result):
        """Called when a test case starts"""
        self.current_test = {
            'name': result.name,
            'suite': self.current_suite,
            'start_time': datetime.utcnow(),
            'tags': list(data.tags) if hasattr(data, 'tags') else []
        }
        print(f"[MongoDB Listener] Test started: {result.name}")

    def end_test(self, data, result):
        """Called when a test case ends"""
        if not self.client:
            return

        # Only report failures
        if result.status == 'FAIL':
            try:
                # Calculate duration
                end_time = datetime.utcnow()
                start_time = self.current_test.get('start_time', end_time)
                duration_ms = int((end_time - start_time).total_seconds() * 1000)

                # Extract error message and stack trace
                error_message = result.message if result.message else "Test failed without error message"

                # Get more details from the result
                stack_trace = ""
                if hasattr(result, 'body'):
                    # Try to get detailed failure information from keywords
                    for item in result.body:
                        if hasattr(item, 'status') and item.status == 'FAIL':
                            if hasattr(item, 'message'):
                                stack_trace += f"{item.name}: {item.message}\n"

                if not stack_trace:
                    stack_trace = error_message

                # BUG FIX #1: Include suite statistics in failure document
                failure_doc = {
                    'timestamp': end_time,
                    'test_name': result.name,
                    'test_suite': self.current_suite,
                    'suite_name': self.current_suite_stats.get('suite_name') if self.current_suite_stats else self.current_suite,
                    'error_message': error_message,
                    'stack_trace': stack_trace,
                    'build_number': self.build_number,
                    'build_id': f"{self.job_name}-{self.build_number}",  # Standardized build ID
                    'job_name': self.job_name,
                    'duration_ms': duration_ms,
                    'status': 'failed',
                    'test_type': 'robot_framework',
                    'tags': self.current_test.get('tags', []),
                    'robot_result': {
                        'status': result.status,
                        'start_time': result.starttime,
                        'end_time': result.endtime,
                        'elapsed_time': result.elapsedtime,
                        'critical': getattr(result, 'critical', 'yes')
                    }
                }

                # Phase 4: Redact PII before storing
                if self.pii_redactor:
                    try:
                        redacted_doc, redaction_metadata = self.pii_redactor.redact_failure_data(failure_doc)
                        failure_doc = redacted_doc
                        if redaction_metadata['total_redactions'] > 0:
                            print(f"[MongoDB Listener] ✓ Redacted {redaction_metadata['total_redactions']} PII entities")
                    except Exception as e:
                        print(f"[MongoDB Listener] WARNING: PII redaction failed: {e}")
                        # Continue with unredacted data (better to store data than lose it)

                # BUG FIX #1: Update suite statistics before storing
                if self.current_suite_stats:
                    self.current_suite_stats['fail_count'] += 1
                    self.current_suite_stats['total_count'] += 1

                # Store in MongoDB
                insert_result = self.collection.insert_one(failure_doc)
                print(f"[MongoDB Listener] ✓ Failure stored: {result.name} (ID: {insert_result.inserted_id})")

            except Exception as e:
                print(f"[MongoDB Listener] ERROR storing failure: {str(e)}")
                print(traceback.format_exc())
        else:
            # BUG FIX #1: Track passed tests in suite statistics
            if self.current_suite_stats:
                self.current_suite_stats['pass_count'] += 1
                self.current_suite_stats['total_count'] += 1
            print(f"[MongoDB Listener] ✓ Test passed: {result.name}")

    def end_suite(self, data, result):
        """Called when a test suite ends - BUG FIX #1: Update all failures with final suite stats"""
        if self.current_suite_stats and self.client:
            try:
                # Update all failures from this suite with final statistics
                update_result = self.collection.update_many(
                    {
                        'test_suite': self.current_suite,
                        'build_number': self.build_number,
                        'job_name': self.job_name
                    },
                    {
                        '$set': {
                            'suite_name': self.current_suite_stats['suite_name'],
                            'pass_count': self.current_suite_stats['pass_count'],
                            'fail_count': self.current_suite_stats['fail_count'],
                            'total_count': self.current_suite_stats['total_count']
                        }
                    }
                )
                print(f"[MongoDB Listener] ✓ Suite ended: {result.name} - "
                      f"Pass: {self.current_suite_stats['pass_count']}, "
                      f"Fail: {self.current_suite_stats['fail_count']}, "
                      f"Total: {self.current_suite_stats['total_count']} "
                      f"({update_result.modified_count} records updated)")
            except Exception as e:
                print(f"[MongoDB Listener] WARNING: Failed to update suite statistics: {e}")
        else:
            print(f"[MongoDB Listener] Suite ended: {result.name} - Status: {result.status}")

    def close(self):
        """Called when all tests are completed"""
        if self.client:
            print("[MongoDB Listener] Closing MongoDB connection")
            self.client.close()

# This allows the listener to be used directly from command line
if __name__ == '__main__':
    print("MongoDB Robot Framework Listener")
    print("This file should be used as a listener with Robot Framework:")
    print("  robot --listener mongodb_robot_listener.py tests/")
