"""
Pytest fixtures for AWS Cloud Networking Lab tests.

Provides reusable test setup and mock infrastructure.
"""

import pytest

from models.aws_intent import (
    AWSNetworkIntent,
    CustomerGatewayIntent,
    SubnetIntent,
    VPCIntent,
    VPNIntent,
)

# ==========================================
# SAMPLE INTENT FIXTURES
# ==========================================

@pytest.fixture
def basic_vpc_intent():
    """Basic VPC intent without VPN."""
    return AWSNetworkIntent(
        project_name="test-project",
        environment="dev",
        region="us-east-1",
        vpc=VPCIntent(
            cidr_block="10.0.0.0/16",
            enable_dns_hostnames=True,
            enable_dns_support=True,
            subnets=[
                SubnetIntent(
                    name="public-a",
                    cidr_block="10.0.1.0/24",
                    availability_zone="us-east-1a",
                    public=True
                ),
                SubnetIntent(
                    name="public-b",
                    cidr_block="10.0.2.0/24",
                    availability_zone="us-east-1b",
                    public=True
                )
            ]
        )
    )


@pytest.fixture
def vpc_with_vpn_intent():
    """VPC intent with VPN configuration."""
    return AWSNetworkIntent(
        project_name="hybrid-lab",
        environment="dev",
        region="us-east-1",
        vpc=VPCIntent(
            cidr_block="10.0.0.0/16",
            subnets=[
                SubnetIntent(
                    name="public-a",
                    cidr_block="10.0.1.0/24",
                    availability_zone="us-east-1a",
                    public=True
                )
            ]
        ),
        vpn=VPNIntent(
            enabled=True,
            customer_gateway=CustomerGatewayIntent(
                ip_address="203.0.113.1",
                bgp_asn=65000,
                device_name="lab-router"
            ),
            static_routes_only=False
        )
    )


@pytest.fixture
def multi_az_intent():
    """Multi-AZ VPC with public and private subnets."""
    return AWSNetworkIntent(
        project_name="multi-az-lab",
        environment="prod",
        region="us-east-1",
        vpc=VPCIntent(
            cidr_block="10.0.0.0/16",
            subnets=[
                # Public subnets
                SubnetIntent(
                    name="public-a",
                    cidr_block="10.0.1.0/24",
                    availability_zone="us-east-1a",
                    public=True
                ),
                SubnetIntent(
                    name="public-b",
                    cidr_block="10.0.2.0/24",
                    availability_zone="us-east-1b",
                    public=True
                ),
                # Private subnets
                SubnetIntent(
                    name="private-a",
                    cidr_block="10.0.11.0/24",
                    availability_zone="us-east-1a",
                    public=False
                ),
                SubnetIntent(
                    name="private-b",
                    cidr_block="10.0.12.0/24",
                    availability_zone="us-east-1b",
                    public=False
                )
            ]
        ),
        enable_nat_gateway=True,
        enable_flow_logs=True
    )


# ==========================================
# INVALID INTENT FIXTURES (for negative tests)
# ==========================================

@pytest.fixture
def invalid_vpc_cidr_cases():
    """Test cases for invalid VPC CIDR blocks."""
    return [
        ("10.0.0.0/15", "too large - /15"),
        ("10.0.0.0/29", "too small - /29"),
        ("256.0.0.0/16", "invalid IP"),
        ("10.0.0.0", "missing prefix"),
        ("invalid", "not a CIDR"),
    ]


@pytest.fixture
def invalid_subnet_cases():
    """Test cases for invalid subnet configurations."""
    return [
        # Subnet outside VPC CIDR
        {
            "vpc_cidr": "10.0.0.0/16",
            "subnet_cidr": "192.168.1.0/24",
            "reason": "outside VPC CIDR"
        },
        # Overlapping subnets
        {
            "vpc_cidr": "10.0.0.0/16",
            "subnets": [
                {"name": "subnet-a", "cidr": "10.0.1.0/24", "az": "us-east-1a"},
                {"name": "subnet-b", "cidr": "10.0.1.128/25", "az": "us-east-1b"}
            ],
            "reason": "overlapping CIDRs"
        }
    ]


# ==========================================
# MOCK AWS RESOURCES
# ==========================================

@pytest.fixture
def mock_vpc_response():
    """Mock AWS VPC response."""
    return {
        "VpcId": "vpc-12345678",
        "CidrBlock": "10.0.0.0/16",
        "State": "available",
        "EnableDnsHostnames": True,
        "EnableDnsSupport": True,
        "Tags": [
            {"Key": "Name", "Value": "test-vpc"},
            {"Key": "Environment", "Value": "dev"}
        ]
    }


@pytest.fixture
def mock_subnet_response():
    """Mock AWS Subnet response."""
    return {
        "SubnetId": "subnet-12345678",
        "VpcId": "vpc-12345678",
        "CidrBlock": "10.0.1.0/24",
        "AvailabilityZone": "us-east-1a",
        "State": "available",
        "MapPublicIpOnLaunch": True
    }


@pytest.fixture
def mock_vpn_connection_response():
    """Mock AWS VPN Connection response."""
    return {
        "VpnConnectionId": "vpn-12345678",
        "State": "available",
        "Type": "ipsec.1",
        "VpnGatewayId": "vgw-12345678",
        "CustomerGatewayId": "cgw-12345678",
        "Options": {
            "StaticRoutesOnly": False,
            "TunnelOptions": [
                {
                    "OutsideIpAddress": "203.0.113.10",
                    "TunnelInsideCidr": "169.254.10.0/30",
                    "PreSharedKey": "test-key-1"
                },
                {
                    "OutsideIpAddress": "203.0.113.11",
                    "TunnelInsideCidr": "169.254.10.4/30",
                    "PreSharedKey": "test-key-2"
                }
            ]
        }
    }


# ==========================================
# PARAMETRIZE HELPERS
# ==========================================

# Valid AWS regions
VALID_REGIONS = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
    "eu-west-1",
    "ap-southeast-1"
]

# Valid BGP ASN ranges
VALID_BGP_ASNS = [
    64512,  # Common private ASN
    65000,  # Private ASN
    65534,  # Max private ASN
    100,    # Public ASN
    4200000000  # 4-byte ASN
]

# Invalid BGP ASNs
INVALID_BGP_ASNS = [
    0,
    -1,
    4294967296  # Over max
]


# ==========================================
# PYTEST CONFIGURATION
# ==========================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests (fast, isolated)"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests (may require AWS/mocks)"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take > 1 second"
    )
    config.addinivalue_line(
        "markers", "aws: Tests that require AWS credentials"
    )
