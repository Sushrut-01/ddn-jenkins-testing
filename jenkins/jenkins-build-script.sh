#!/bin/bash
echo "========================================="
echo "DDN Robot Framework Tests - Build $BUILD_NUMBER"
echo "Job: $JOB_NAME"
echo "Workspace: $WORKSPACE"
echo "========================================="

# Install Robot Framework and dependencies
echo "Installing dependencies..."
python3 -m pip install --quiet --upgrade pip --break-system-packages
python3 -m pip install --quiet --break-system-packages robotframework pymongo python-dotenv boto3 requests

# Set MongoDB reporter environment variables
export MONGODB_URI='mongodb+srv://sushrutnistane097_db_user:Sharu%40051220@ddn-cluster.wudcfln.mongodb.net/ddn_tests?retryWrites=true&w=majority'
export JOB_NAME="$JOB_NAME"
export BUILD_NUMBER="$BUILD_NUMBER"
export BUILD_URL="$BUILD_URL"
export GIT_COMMIT="$GIT_COMMIT"
export GIT_BRANCH="$GIT_BRANCH"

# Create output directory
mkdir -p robot-results

echo "Running Robot Framework tests..."
echo "Git Branch: $GIT_BRANCH"
echo "Git Commit: $GIT_COMMIT"
python3 -m robot --outputdir robot-results --listener implementation.mongodb_robot_listener.MongoDBListener robot-tests/

echo "========================================="
echo "Robot Framework Tests completed!"
echo "Build URL: $BUILD_URL"
echo "========================================="
