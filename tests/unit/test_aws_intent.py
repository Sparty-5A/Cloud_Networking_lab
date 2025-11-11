"""
Unit tests for AWS intent Pydantic models.

Tests validation logic, CIDR calculations, and intent creation.
"""

import pytest
from pydantic import ValidationError

from models.aws_intent import (
    AWSNetworkIntent,
    CustomerGatewayIntent,
    SubnetIntent,
    VPCIntent,
    VPNIntent,
)

# ==========================================
# SUBNET INTENT TESTS
# ==========================================

class TestSubnetIntent:
    """Test SubnetIntent model validation."""
    
    def test_valid_subnet_creation(self):
        """Test creating a valid subnet intent."""
        subnet = SubnetIntent(
            name="test-subnet",
            cidr_block="10.0.1.0/24",
            availability_zone="us-east-1a",
            public=True
        )
        
        assert subnet.name == "test-subnet"
        assert subnet.cidr_block == "10.0.1.0/24"
        assert subnet.availability_zone == "us-east-1a"
        assert subnet.public is True
    
    def test_invalid_cidr_block(self):
        """Test subnet with invalid CIDR block."""
        with pytest.raises(ValidationError) as exc_info:
            SubnetIntent(
                name="bad-subnet",
                cidr_block="256.0.0.0/24",
                availability_zone="us-east-1a"
            )
        
        assert "Invalid CIDR block" in str(exc_info.value)
    
    def test_invalid_availability_zone(self):
        """Test subnet with invalid AZ."""
        with pytest.raises(ValidationError) as exc_info:
            SubnetIntent(
                name="bad-az",
                cidr_block="10.0.1.0/24",
                availability_zone="bad"
            )
        
        assert "Invalid availability zone" in str(exc_info.value)
    
    def test_default_public_false(self):
        """Test subnet defaults to private."""
        subnet = SubnetIntent(
            name="private-subnet",
            cidr_block="10.0.2.0/24",
            availability_zone="us-east-1a"
        )
        
        assert subnet.public is False


# ==========================================
# VPC INTENT TESTS
# ==========================================

class TestVPCIntent:
    """Test VPCIntent model validation."""
    
    def test_valid_vpc_creation(self):
        """Test creating a valid VPC intent."""
        vpc = VPCIntent(
            cidr_block="10.0.0.0/16",
            enable_dns_hostnames=True,
            enable_dns_support=True
        )
        
        assert vpc.cidr_block == "10.0.0.0/16"
        assert vpc.enable_dns_hostnames is True
        assert vpc.enable_dns_support is True
        assert vpc.subnets == []
    
    @pytest.mark.parametrize("cidr,expected_valid", [
        ("10.0.0.0/16", True),   # Valid
        ("10.0.0.0/24", True),   # Valid
        ("10.0.0.0/28", True),   # Valid (min)
        ("10.0.0.0/15", False),  # Too large
        ("10.0.0.0/29", False),  # Too small
        ("invalid", False),      # Not a CIDR
    ])
    def test_vpc_cidr_validation(self, cidr, expected_valid):
        """Test VPC CIDR validation."""
        if expected_valid:
            vpc = VPCIntent(cidr_block=cidr)
            assert vpc.cidr_block == cidr
        else:
            with pytest.raises(ValidationError):
                VPCIntent(cidr_block=cidr)
    
    def test_vpc_with_subnets(self):
        """Test VPC with valid subnets."""
        vpc = VPCIntent(
            cidr_block="10.0.0.0/16",
            subnets=[
                SubnetIntent(
                    name="subnet-a",
                    cidr_block="10.0.1.0/24",
                    availability_zone="us-east-1a"
                ),
                SubnetIntent(
                    name="subnet-b",
                    cidr_block="10.0.2.0/24",
                    availability_zone="us-east-1b"
                )
            ]
        )
        
        assert len(vpc.subnets) == 2
        assert vpc.subnets[0].name == "subnet-a"
        assert vpc.subnets[1].name == "subnet-b"
    
    def test_subnet_outside_vpc_cidr(self):
        """Test subnet CIDR outside VPC CIDR fails."""
        with pytest.raises(ValidationError) as exc_info:
            VPCIntent(
                cidr_block="10.0.0.0/16",
                subnets=[
                    SubnetIntent(
                        name="bad-subnet",
                        cidr_block="192.168.1.0/24",
                        availability_zone="us-east-1a"
                    )
                ]
            )
        
        assert "not within VPC CIDR" in str(exc_info.value)
    
    def test_overlapping_subnets(self):
        """Test overlapping subnet CIDRs fail."""
        with pytest.raises(ValidationError) as exc_info:
            VPCIntent(
                cidr_block="10.0.0.0/16",
                subnets=[
                    SubnetIntent(
                        name="subnet-a",
                        cidr_block="10.0.1.0/24",
                        availability_zone="us-east-1a"
                    ),
                    SubnetIntent(
                        name="subnet-b",
                        cidr_block="10.0.1.128/25",  # Overlaps with subnet-a
                        availability_zone="us-east-1b"
                    )
                ]
            )
        
        assert "overlapping CIDR blocks" in str(exc_info.value)


# ==========================================
# CUSTOMER GATEWAY INTENT TESTS
# ==========================================

class TestCustomerGatewayIntent:
    """Test CustomerGatewayIntent model validation."""
    
    def test_valid_customer_gateway(self):
        """Test creating a valid customer gateway."""
        cgw = CustomerGatewayIntent(
            ip_address="203.0.113.1",
            bgp_asn=65000,
            device_name="lab-router"
        )
        
        assert cgw.ip_address == "203.0.113.1"
        assert cgw.bgp_asn == 65000
        assert cgw.device_name == "lab-router"
    
    def test_invalid_ip_address(self):
        """Test customer gateway with invalid IP."""
        with pytest.raises(ValidationError) as exc_info:
            CustomerGatewayIntent(
                ip_address="256.0.0.1",
                bgp_asn=65000
            )
        
        assert "Invalid IP address" in str(exc_info.value)
    
    @pytest.mark.parametrize("asn,expected_valid", [
        (1, True),          # Min
        (65000, True),      # Private
        (64512, True),      # AWS default
        (4294967295, True), # Max
        (0, False),         # Too low
        (-1, False),        # Negative
    ])
    def test_bgp_asn_validation(self, asn, expected_valid):
        """Test BGP ASN validation."""
        if expected_valid:
            cgw = CustomerGatewayIntent(
                ip_address="203.0.113.1",
                bgp_asn=asn
            )
            assert cgw.bgp_asn == asn
        else:
            with pytest.raises(ValidationError):
                CustomerGatewayIntent(
                    ip_address="203.0.113.1",
                    bgp_asn=asn
                )


# ==========================================
# VPN INTENT TESTS
# ==========================================

class TestVPNIntent:
    """Test VPNIntent model validation."""
    
    def test_vpn_disabled_by_default(self):
        """Test VPN is disabled by default."""
        vpn = VPNIntent()
        
        assert vpn.enabled is False
        assert vpn.customer_gateway is None
        assert vpn.static_routes_only is False
        assert vpn.static_routes == []
    
    def test_vpn_with_bgp(self):
        """Test VPN with BGP configuration."""
        vpn = VPNIntent(
            enabled=True,
            customer_gateway=CustomerGatewayIntent(
                ip_address="203.0.113.1",
                bgp_asn=65000
            ),
            static_routes_only=False
        )
        
        assert vpn.enabled is True
        assert vpn.customer_gateway.bgp_asn == 65000
        assert vpn.static_routes_only is False
    
    def test_vpn_with_static_routes(self):
        """Test VPN with static routes."""
        vpn = VPNIntent(
            enabled=True,
            customer_gateway=CustomerGatewayIntent(
                ip_address="203.0.113.1",
                bgp_asn=65000
            ),
            static_routes_only=True,
            static_routes=["192.168.1.0/24", "192.168.2.0/24"]
        )
        
        assert vpn.static_routes_only is True
        assert len(vpn.static_routes) == 2
    
    def test_invalid_static_route_cidr(self):
        """Test VPN with invalid static route CIDR."""
        with pytest.raises(ValidationError) as exc_info:
            VPNIntent(
                enabled=True,
                customer_gateway=CustomerGatewayIntent(
                    ip_address="203.0.113.1",
                    bgp_asn=65000
                ),
                static_routes=["invalid_cidr"]
            )
        
        assert "Invalid static route CIDR" in str(exc_info.value)


# ==========================================
# AWS NETWORK INTENT TESTS
# ==========================================

class TestAWSNetworkIntent:
    """Test complete AWSNetworkIntent model."""
    
    def test_basic_network_intent(self, basic_vpc_intent):
        """Test creating a basic network intent."""
        intent = basic_vpc_intent
        
        assert intent.project_name == "test-project"
        assert intent.environment == "dev"
        assert intent.region == "us-east-1"
        assert intent.vpc.cidr_block == "10.0.0.0/16"
        assert len(intent.vpc.subnets) == 2
        assert intent.vpn is None
    
    def test_network_intent_with_vpn(self, vpc_with_vpn_intent):
        """Test network intent with VPN."""
        intent = vpc_with_vpn_intent
        
        assert intent.vpn is not None
        assert intent.vpn.enabled is True
        assert intent.vpn.customer_gateway.ip_address == "203.0.113.1"
    
    def test_vpn_enabled_requires_customer_gateway(self):
        """Test VPN enabled without customer gateway fails."""
        with pytest.raises(ValidationError) as exc_info:
            AWSNetworkIntent(
                project_name="test",
                vpc=VPCIntent(cidr_block="10.0.0.0/16"),
                vpn=VPNIntent(enabled=True)  # No customer_gateway
            )
        
        assert "customer_gateway not configured" in str(exc_info.value)
    
    def test_static_routes_only_requires_routes(self):
        """Test static_routes_only without routes fails."""
        with pytest.raises(ValidationError) as exc_info:
            AWSNetworkIntent(
                project_name="test",
                vpc=VPCIntent(cidr_block="10.0.0.0/16"),
                vpn=VPNIntent(
                    enabled=True,
                    customer_gateway=CustomerGatewayIntent(
                        ip_address="203.0.113.1",
                        bgp_asn=65000
                    ),
                    static_routes_only=True,
                    static_routes=[]  # Empty!
                )
            )
        
        assert "no static_routes provided" in str(exc_info.value)
    
    def test_to_pulumi_config(self, basic_vpc_intent):
        """Test converting intent to Pulumi config."""
        config = basic_vpc_intent.to_pulumi_config()
        
        assert config["vpc_cidr"] == "10.0.0.0/16"
        assert config["enable_vpn"] is False
        assert config["enable_nat_gateway"] is False
    
    def test_to_pulumi_config_with_vpn(self, vpc_with_vpn_intent):
        """Test Pulumi config with VPN."""
        config = vpc_with_vpn_intent.to_pulumi_config()
        
        assert config["enable_vpn"] is True
        assert config["customer_gateway_ip"] == "203.0.113.1"
        assert config["customer_bgp_asn"] == 65000
    
    @pytest.mark.parametrize("environment", ["dev", "staging", "prod"])
    def test_valid_environments(self, environment):
        """Test valid environment names."""
        intent = AWSNetworkIntent(
            project_name="test",
            environment=environment,
            vpc=VPCIntent(cidr_block="10.0.0.0/16")
        )
        
        assert intent.environment == environment
    
    def test_invalid_environment(self):
        """Test invalid environment name fails."""
        with pytest.raises(ValidationError):
            AWSNetworkIntent(
                project_name="test",
                environment="invalid",
                vpc=VPCIntent(cidr_block="10.0.0.0/16")
            )


# ==========================================
# INTEGRATION TESTS
# ==========================================

@pytest.mark.integration
class TestIntentIntegration:
    """Test intent models working together."""
    
    def test_complete_hybrid_network_intent(self):
        """Test creating a complete hybrid network intent."""
        intent = AWSNetworkIntent(
            project_name="hybrid-cloud",
            environment="prod",
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
                    ),
                    SubnetIntent(
                        name="private-a",
                        cidr_block="10.0.11.0/24",
                        availability_zone="us-east-1a",
                        public=False
                    )
                ]
            ),
            vpn=VPNIntent(
                enabled=True,
                customer_gateway=CustomerGatewayIntent(
                    ip_address="203.0.113.50",
                    bgp_asn=65100,
                    device_name="datacenter-router"
                ),
                static_routes_only=False,
                amazon_side_asn=64512
            ),
            enable_nat_gateway=True,
            enable_flow_logs=True
        )
        
        # Validate all components
        assert intent.project_name == "hybrid-cloud"
        assert intent.environment == "prod"
        assert len(intent.vpc.subnets) == 3
        assert intent.vpn.enabled is True
        assert intent.vpn.customer_gateway.device_name == "datacenter-router"
        assert intent.enable_nat_gateway is True
        assert intent.enable_flow_logs is True
        
        # Test Pulumi config generation
        config = intent.to_pulumi_config()
        assert config["enable_vpn"] is True
        assert config["customer_bgp_asn"] == 65100
