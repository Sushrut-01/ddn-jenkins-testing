"""
DDN Storage Test Keywords Library for Robot Framework
Provides Python-based keywords for testing DDN storage products
"""

import os
import requests
import boto3
from botocore.client import Config
from datetime import datetime
import json
from dotenv import load_dotenv

load_dotenv()

class DDN_Keywords:
    """
    Robot Framework keyword library for DDN Storage testing
    """

    ROBOT_LIBRARY_SCOPE = 'SUITE'

    def __init__(self):
        """Initialize DDN test configuration"""
        # DDN Storage Endpoints
        self.exascaler_endpoint = os.getenv('DDN_EXASCALER_ENDPOINT', 'http://exascaler.ddn.local')
        self.ai400x_endpoint = os.getenv('DDN_AI400X_ENDPOINT', 'http://ai400x.ddn.local')
        self.infinia_endpoint = os.getenv('DDN_INFINIA_ENDPOINT', 'http://infinia.ddn.local')
        self.intelliflash_endpoint = os.getenv('DDN_INTELLIFLASH_ENDPOINT', 'http://intelliflash.ddn.local')
        self.emf_endpoint = os.getenv('DDN_EMF_ENDPOINT', 'http://emf.ddn.local')
        self.s3_endpoint = os.getenv('DDN_S3_ENDPOINT', 'http://s3.exascaler.ddn.local')

        # API Credentials
        self.api_key = os.getenv('DDN_API_KEY', '')
        self.api_secret = os.getenv('DDN_API_SECRET', '')
        self.s3_access_key = os.getenv('DDN_S3_ACCESS_KEY', '')
        self.s3_secret_key = os.getenv('DDN_S3_SECRET_KEY', '')

        # Session for HTTP requests
        self.session = requests.Session()
        self.session.headers.update(self._get_auth_headers())

        # S3 clients
        self.s3_clients = {}

        # Test context
        self.current_test = {}

    def _get_auth_headers(self):
        """Get authentication headers for DDN API"""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'X-API-Secret': self.api_secret,
            'Content-Type': 'application/json',
            'User-Agent': 'DDN-Robot-Framework-Tests/1.0'
        }

    def get_exascaler_health(self):
        """
        Get EXAScaler health status
        Returns response object
        """
        url = f"{self.exascaler_endpoint}/api/v1/health"
        response = self.session.get(url)
        return response

    def get_exascaler_cluster_status(self):
        """
        Get EXAScaler cluster status including MDS and OSS servers
        Returns response object
        """
        url = f"{self.exascaler_endpoint}/api/v1/cluster/status"
        response = self.session.get(url)
        return response

    def run_exascaler_throughput_benchmark(self, file_size_gb=10, parallel_streams=8):
        """
        Run EXAScaler throughput benchmark

        Arguments:
        - file_size_gb: Size of test file in GB
        - parallel_streams: Number of parallel streams

        Returns response object
        """
        url = f"{self.exascaler_endpoint}/api/v1/performance/benchmark"
        data = {
            'operation': 'benchmark',
            'test_type': 'throughput',
            'file_size_gb': int(file_size_gb),
            'parallel_streams': int(parallel_streams)
        }
        response = self.session.post(url, json=data)
        return response

    def create_lustre_striped_file(self, path, stripe_count=4, stripe_size='1M', size_mb=100):
        """
        Create a Lustre striped file

        Arguments:
        - path: File path
        - stripe_count: Number of stripes
        - stripe_size: Size of each stripe
        - size_mb: Total file size in MB

        Returns file ID
        """
        url = f"{self.exascaler_endpoint}/api/v1/files/create"
        data = {
            'path': path,
            'stripe_count': int(stripe_count),
            'stripe_size': stripe_size,
            'size_mb': int(size_mb)
        }
        response = self.session.post(url, json=data)
        if response.status_code == 201:
            return response.json().get('file_id')
        else:
            raise Exception(f"Failed to create file: {response.status_code} - {response.text}")

    def verify_file_striping(self, file_id):
        """
        Verify Lustre file striping configuration

        Arguments:
        - file_id: File ID to verify

        Returns stripe configuration dict
        """
        url = f"{self.exascaler_endpoint}/api/v1/files/{file_id}/stripe-info"
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to verify striping: {response.status_code}")

    def get_ai400x_health(self):
        """Get AI400X storage platform health status"""
        url = f"{self.ai400x_endpoint}/api/v1/health"
        response = self.session.get(url)
        return response

    def get_ai400x_gpu_metrics(self):
        """Get AI400X GPU-optimized storage metrics"""
        url = f"{self.ai400x_endpoint}/api/v1/gpu/storage-metrics"
        response = self.session.get(url)
        return response

    def store_ai_checkpoint(self, model_name, checkpoint_epoch, checkpoint_size_gb, metadata=None):
        """
        Store AI model checkpoint on AI400X

        Arguments:
        - model_name: Name of the AI model
        - checkpoint_epoch: Training epoch number
        - checkpoint_size_gb: Checkpoint size in GB
        - metadata: Additional metadata dict

        Returns checkpoint ID
        """
        url = f"{self.ai400x_endpoint}/api/v1/checkpoints/store"
        data = {
            'model_name': model_name,
            'checkpoint_epoch': int(checkpoint_epoch),
            'checkpoint_size_gb': int(checkpoint_size_gb),
            'metadata': metadata or {}
        }
        response = self.session.post(url, json=data)
        if response.status_code == 201:
            return response.json().get('checkpoint_id')
        else:
            raise Exception(f"Failed to store checkpoint: {response.status_code}")

    def retrieve_ai_checkpoint(self, checkpoint_id):
        """Retrieve AI model checkpoint"""
        url = f"{self.ai400x_endpoint}/api/v1/checkpoints/{checkpoint_id}"
        response = self.session.get(url)
        return response

    def run_ai_data_loading_benchmark(self, dataset_size_gb, batch_size, data_format='tfrecord'):
        """
        Run AI data loading performance benchmark

        Arguments:
        - dataset_size_gb: Dataset size in GB
        - batch_size: Batch size for loading
        - data_format: Data format (tfrecord, etc.)

        Returns benchmark results
        """
        url = f"{self.ai400x_endpoint}/api/v1/benchmark/data-loading"
        data = {
            'dataset_size_gb': int(dataset_size_gb),
            'batch_size': int(batch_size),
            'data_format': data_format,
            'test_duration_sec': 60
        }
        response = self.session.post(url, json=data)
        return response

    def get_infinia_status(self):
        """Get Infinia orchestration platform status"""
        url = f"{self.infinia_endpoint}/api/v1/status"
        response = self.session.get(url)
        return response

    def optimize_llm_workload(self, model_size, gpus, expected_tokens_per_sec):
        """
        Optimize LLM training workload with Infinia

        Arguments:
        - model_size: Model size (e.g., '70B')
        - gpus: Number of GPUs
        - expected_tokens_per_sec: Expected throughput

        Returns optimization profile
        """
        url = f"{self.infinia_endpoint}/api/v1/workload/optimize"
        data = {
            'workload_type': 'llm_training',
            'model_size': model_size,
            'gpus': int(gpus),
            'expected_tokens_per_sec': int(expected_tokens_per_sec)
        }
        response = self.session.post(url, json=data)
        return response

    def run_checkpoint_benchmark(self, model_size_gb, checkpoint_type='full', target_time_sec=60):
        """
        Benchmark checkpointing performance

        Arguments:
        - model_size_gb: Model size in GB
        - checkpoint_type: Type of checkpoint
        - target_time_sec: Target completion time

        Returns benchmark results
        """
        url = f"{self.infinia_endpoint}/api/v1/benchmark/checkpoint"
        data = {
            'model_size_gb': int(model_size_gb),
            'checkpoint_type': checkpoint_type,
            'target_time_sec': int(target_time_sec)
        }
        response = self.session.post(url, json=data)
        return response

    def setup_edge_core_cloud_orchestration(self, edge_nodes, core_datacenter, cloud_provider, dataset_size_tb):
        """
        Setup edge-core-cloud data orchestration

        Arguments:
        - edge_nodes: Number of edge nodes
        - core_datacenter: Core datacenter location
        - cloud_provider: Cloud provider name
        - dataset_size_tb: Dataset size in TB

        Returns orchestration ID
        """
        url = f"{self.infinia_endpoint}/api/v1/orchestration/setup"
        data = {
            'edge_nodes': int(edge_nodes),
            'core_datacenter': core_datacenter,
            'cloud_provider': cloud_provider,
            'data_flow': 'bidirectional',
            'dataset_size_tb': int(dataset_size_tb)
        }
        response = self.session.post(url, json=data)
        if response.status_code == 201:
            return response.json().get('orchestration_id')
        else:
            raise Exception(f"Failed to setup orchestration: {response.status_code}")

    def get_intelliflash_system_info(self):
        """Get IntelliFlash system information"""
        url = f"{self.intelliflash_endpoint}/api/v1/system/info"
        response = self.session.get(url)
        return response

    def create_intelliflash_volume(self, name, size_gb, compression=True, deduplication=True):
        """
        Create IntelliFlash volume

        Arguments:
        - name: Volume name
        - size_gb: Volume size in GB
        - compression: Enable compression
        - deduplication: Enable deduplication

        Returns volume ID
        """
        url = f"{self.intelliflash_endpoint}/api/v1/volumes/create"
        data = {
            'name': name,
            'size_gb': int(size_gb),
            'compression': compression,
            'deduplication': deduplication
        }
        response = self.session.post(url, json=data)
        if response.status_code == 201:
            return response.json().get('volume_id')
        else:
            raise Exception(f"Failed to create volume: {response.status_code}")

    def get_intelliflash_volume(self, volume_id):
        """Get IntelliFlash volume details"""
        url = f"{self.intelliflash_endpoint}/api/v1/volumes/{volume_id}"
        response = self.session.get(url)
        return response

    def update_intelliflash_volume(self, volume_id, size_gb):
        """Update IntelliFlash volume size"""
        url = f"{self.intelliflash_endpoint}/api/v1/volumes/{volume_id}"
        data = {'size_gb': int(size_gb)}
        response = self.session.patch(url, json=data)
        return response

    def delete_intelliflash_volume(self, volume_id):
        """Delete IntelliFlash volume"""
        url = f"{self.intelliflash_endpoint}/api/v1/volumes/{volume_id}"
        response = self.session.delete(url)
        return response

    def get_storage_efficiency_metrics(self):
        """Get IntelliFlash storage efficiency (dedup/compression) metrics"""
        url = f"{self.intelliflash_endpoint}/api/v1/storage/efficiency"
        response = self.session.get(url)
        return response

    def create_domain(self, domain_name, vlan_id, network_segment, isolation_level='strict'):
        """
        Create domain for tenant isolation

        Arguments:
        - domain_name: Domain name
        - vlan_id: VLAN ID
        - network_segment: Network segment (e.g., '10.100.0.0/24')
        - isolation_level: Isolation level (strict, moderate, none)

        Returns domain ID
        """
        url = f"{self.emf_endpoint}/api/v1/domains/create"
        data = {
            'domain_name': domain_name,
            'vlan_id': int(vlan_id),
            'isolation_level': isolation_level,
            'network_segment': network_segment
        }
        response = self.session.post(url, json=data)
        if response.status_code == 201:
            return response.json().get('domain_id')
        else:
            raise Exception(f"Failed to create domain: {response.status_code}")

    def create_namespace(self, namespace_name, root_path, owner_domain, mount_type='subdirectory'):
        """
        Create isolated namespace for tenant

        Arguments:
        - namespace_name: Namespace name
        - root_path: Root path for namespace
        - owner_domain: Owning domain
        - mount_type: Mount type (subdirectory, etc.)

        Returns namespace ID
        """
        url = f"{self.exascaler_endpoint}/api/v1/namespaces/create"
        data = {
            'namespace_name': namespace_name,
            'root_path': root_path,
            'mount_type': mount_type,
            'owner_domain': owner_domain
        }
        response = self.session.post(url, json=data)
        if response.status_code == 201:
            return response.json().get('namespace_id')
        else:
            raise Exception(f"Failed to create namespace: {response.status_code}")

    def set_storage_quota(self, namespace, soft_limit_gb, hard_limit_gb, grace_period_hours=24):
        """
        Set storage quota for namespace

        Arguments:
        - namespace: Namespace name
        - soft_limit_gb: Soft limit in GB
        - hard_limit_gb: Hard limit in GB
        - grace_period_hours: Grace period in hours

        Returns quota ID
        """
        url = f"{self.exascaler_endpoint}/api/v1/quotas/set"
        data = {
            'namespace': namespace,
            'quota_type': 'storage',
            'soft_limit_gb': float(soft_limit_gb),
            'hard_limit_gb': float(hard_limit_gb),
            'grace_period_hours': int(grace_period_hours)
        }
        response = self.session.post(url, json=data)
        if response.status_code == 201:
            return response.json().get('quota_id')
        else:
            raise Exception(f"Failed to set quota: {response.status_code}")

    def create_s3_client(self, tenant_name, access_key=None, secret_key=None):
        """
        Create S3 client for tenant

        Arguments:
        - tenant_name: Tenant identifier
        - access_key: S3 access key (optional)
        - secret_key: S3 secret key (optional)

        Returns S3 client
        """
        access = access_key or self.s3_access_key
        secret = secret_key or self.s3_secret_key

        s3_client = boto3.client(
            's3',
            endpoint_url=self.s3_endpoint,
            aws_access_key_id=access,
            aws_secret_access_key=secret,
            config=Config(signature_version='s4', s3={'addressing_style': 'path'})
        )

        self.s3_clients[tenant_name] = s3_client
        return s3_client

    def create_s3_bucket(self, tenant_name, bucket_name, location_constraint=None):
        """
        Create S3 bucket for tenant

        Arguments:
        - tenant_name: Tenant identifier
        - bucket_name: Bucket name
        - location_constraint: Location constraint

        Returns bucket location
        """
        if tenant_name not in self.s3_clients:
            self.create_s3_client(tenant_name)

        s3_client = self.s3_clients[tenant_name]

        config = {}
        if location_constraint:
            config['LocationConstraint'] = location_constraint

        if config:
            response = s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration=config
            )
        else:
            response = s3_client.create_bucket(Bucket=bucket_name)

        return response.get('Location')

    def list_s3_objects(self, tenant_name, bucket_name):
        """
        List objects in S3 bucket

        Arguments:
        - tenant_name: Tenant identifier
        - bucket_name: Bucket name

        Returns list of objects
        """
        if tenant_name not in self.s3_clients:
            raise Exception(f"S3 client not created for tenant: {tenant_name}")

        s3_client = self.s3_clients[tenant_name]
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        return response

    def get_quota_usage(self, namespace):
        """
        Get quota usage statistics for namespace

        Arguments:
        - namespace: Namespace name

        Returns quota usage dict
        """
        url = f"{self.exascaler_endpoint}/api/v1/quotas/{namespace}/usage"
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get quota usage: {response.status_code}")

    def get_audit_logs(self, tenant_domain, hours=24):
        """
        Get audit logs for tenant

        Arguments:
        - tenant_domain: Tenant domain
        - hours: Number of hours to retrieve

        Returns audit log entries
        """
        url = f"{self.emf_endpoint}/api/v1/audit/logs"
        start_time = datetime.utcnow() - timedelta(hours=hours)
        params = {
            'tenant_domain': tenant_domain,
            'start_time': start_time.isoformat() + 'Z',
            'end_time': datetime.utcnow().isoformat() + 'Z'
        }
        response = self.session.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('audit_entries', [])
        else:
            raise Exception(f"Failed to get audit logs: {response.status_code}")

    def close_session(self):
        """Close HTTP session"""
        self.session.close()
