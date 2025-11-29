/**
 * MongoDB Failure Reporter
 *
 * Automatically reports test failures to MongoDB database
 * No Jenkins or GitHub configuration needed - works out of the box
 */

// Load environment variables from .env file
require('dotenv').config();

const { MongoClient } = require('mongodb');

class MongoDBReporter {
    constructor() {
        // Require an explicit MongoDB connection string via environment variable.
        // The project uses MongoDB Atlas in production. Example:
        // mongodb+srv://<user>:<pass>@cluster0.xxxxx.mongodb.net/ddn_tests?retryWrites=true&w=majority
        this.mongodbUri = process.env.MONGODB_URI;
        if (!this.mongodbUri) {
            throw new Error('MONGODB_URI is required. Set it to your MongoDB Atlas connection string.');
        }
        this.database = process.env.MONGODB_DATABASE || 'ddn_tests';
        this.collection = process.env.MONGODB_COLLECTION_FAILURES || 'test_failures';
        this.client = null;
    }

    /**
     * Connect to MongoDB
     */
    async connect() {
        if (!this.client) {
            this.client = new MongoClient(this.mongodbUri);
            await this.client.connect();
            console.log('✓ MongoDB Reporter: Connected to database');
        }
        return this.client.db(this.database);
    }

    /**
     * Report test failure to MongoDB
     * @param {Object} failureData - Test failure information
     */
    async reportFailure(failureData) {
        try {
            const db = await this.connect();
            const collection = db.collection(this.collection);

            // Build complete failure document
            const document = {
                // Test Information
                test_name: failureData.test_name,
                test_category: failureData.test_category,
                product: failureData.product || 'DDN Storage',
                error_message: failureData.error_message,
                stack_trace: failureData.stack_trace,

                // Suite metadata (Bug #1 fix)
                suite_name: failureData.suite_name || failureData.test_category || 'Unknown Suite',
                pass_count: failureData.pass_count || 0,
                fail_count: failureData.fail_count || 1,
                total_count: failureData.total_count || 1,

                // Build Information (from Jenkins environment variables)
                // Bug #3 fix: Standardized build_id format: JobName-BuildNumber
                build_id: process.env.JOB_NAME && process.env.BUILD_NUMBER 
                    ? `${process.env.JOB_NAME}-${process.env.BUILD_NUMBER}`
                    : (process.env.BUILD_ID || process.env.BUILD_NUMBER || 'local'),
                job_name: process.env.JOB_NAME || 'manual-run',
                build_url: process.env.BUILD_URL || 'local',

                // Git Information
                git_commit: process.env.GIT_COMMIT || 'unknown',
                git_branch: process.env.GIT_BRANCH || 'main',
                repository: 'https://github.com/Sushrut-01/ddn-ai-test-analysis',

                // Status and Analysis
                status: 'FAILURE',
                analyzed: false,  // AI will set this to true after analysis
                analysis_required: true,

                // Timestamps
                timestamp: new Date(),
                created_at: new Date(),

                // Additional context
                environment: process.env.NODE_ENV || 'test',
                system: 'DDN Storage Tests',
                ...failureData  // Include any additional fields
            };

            const result = await collection.insertOne(document);
            console.log(`✓ Failure saved to MongoDB (ID: ${result.insertedId})`);
            return result.insertedId;
        } catch (error) {
            console.error('✗ MongoDB Reporter Error:', error.message);
            // Don't throw - we don't want MongoDB errors to break tests
            return null;
        }
    }

    /**
     * Report successful test to MongoDB (for tracking)
     */
    async reportSuccess(testData) {
        try {
            const db = await this.connect();
            const collection = db.collection('test_results');

            const document = {
                test_name: testData.test_name,
                test_category: testData.test_category,
                product: testData.product,
                status: 'SUCCESS',
                duration_ms: testData.duration_ms,
                build_id: process.env.BUILD_ID || 'local',
                job_name: process.env.JOB_NAME || 'manual-run',
                timestamp: new Date(),
                created_at: new Date()
            };

            await collection.insertOne(document);
            console.log(`✓ Success recorded in MongoDB`);
        } catch (error) {
            console.error('✗ MongoDB Reporter Error:', error.message);
        }
    }

    /**
     * Close MongoDB connection
     */
    async close() {
        if (this.client) {
            await this.client.close();
            this.client = null;
            console.log('✓ MongoDB Reporter: Connection closed');
        }
    }
}

// Export singleton instance
module.exports = new MongoDBReporter();
