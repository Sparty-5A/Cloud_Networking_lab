"""
Pydantic models for AWS network intent.

Intent-based configuration for AWS networking infrastructure.
"""

import ipaddress
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator


class SubnetIntent(BaseModel):
    """Intent for a subnet configuration."""
    
    name: str = Field(..., description="Subnet name/identifier")
    cidr_block: str = Field(..., description="CIDR block for subnet")
    availability_zone: str = Field(..., description="AWS availability zone")
    public: bool = Field(default=False, description="Public subnet (with IGW route)")
    
    @field_validator('cidr_block')
    def validate_cidr(cls, v: str) -> str:
        """Validate CIDR block format."""
        try:
            ipaddress.ip_network(v, strict=False)
            return v
        except ValueError as err:
            raise ValueError(f"Invalid CIDR block: {v}") from err
    
    @field_validator('availability_zone')
    def validate_az(cls, v: str) -> str:
        """Validate availability zone format."""
        # Basic validation - should match pattern like us-east-1a
        if not v or len(v) < 10:
            raise ValueError(f"Invalid availability zone: {v}")
        return v


class VPCIntent(BaseModel):
    """Intent for VPC configuration."""
    
    cidr_block: str = Field(..., description="CIDR block for VPC")
    enable_dns_hostnames: bool = Field(default=True, description="Enable DNS hostnames")
    enable_dns_support: bool = Field(default=True, description="Enable DNS support")
    subnets: list[SubnetIntent] = Field(default_factory=list, description="List of subnets")
    
    @field_validator('cidr_block')
    def validate_cidr(cls, v: str) -> str:
        """Validate VPC CIDR block."""
        try:
            network = ipaddress.ip_network(v, strict=False)
            # VPC CIDR must be between /16 and /28
            if not (16 <= network.prefixlen <= 28):
                raise ValueError(f"VPC CIDR must be between /16 and /28, got /{network.prefixlen}")
            return v
        except ValueError as err:
            raise ValueError(f"Invalid VPC CIDR block: {v}") from err
    
    @field_validator('subnets')
    def validate_subnets(cls, v: list[SubnetIntent], info) -> list[SubnetIntent]:
        """Validate subnets are within VPC CIDR."""
        if not v:
            return v
        
        # Get VPC CIDR from the model
        vpc_cidr_str = info.data.get('cidr_block')
        if not vpc_cidr_str:
            return v
        
        vpc_network = ipaddress.ip_network(vpc_cidr_str, strict=False)
        
        # Check each subnet is within VPC CIDR
        for subnet in v:
            subnet_network = ipaddress.ip_network(subnet.cidr_block, strict=False)
            if not subnet_network.subnet_of(vpc_network):
                raise ValueError(
                    f"Subnet {subnet.name} ({subnet.cidr_block}) is not within "
                    f"VPC CIDR {vpc_cidr_str}"
                )
        
        # Check for overlapping subnets
        for i, subnet1 in enumerate(v):
            net1 = ipaddress.ip_network(subnet1.cidr_block, strict=False)
            for subnet2 in v[i+1:]:
                net2 = ipaddress.ip_network(subnet2.cidr_block, strict=False)
                if net1.overlaps(net2):
                    raise ValueError(
                        f"Subnets {subnet1.name} and {subnet2.name} have overlapping CIDR blocks"
                    )
        
        return v


class CustomerGatewayIntent(BaseModel):
    """Intent for Customer Gateway (on-prem side)."""
    
    ip_address: str = Field(..., description="Public IP of customer gateway")
    bgp_asn: int = Field(..., ge=1, le=4294967295, description="BGP AS number")
    device_name: Optional[str] = Field(None, description="Device name/identifier")
    
    @field_validator('ip_address')
    def validate_ip(cls, v: str) -> str:
        """Validate customer gateway IP address."""
        try:
            ipaddress.ip_address(v)
            return v
        except ValueError as err:
            raise ValueError(f"Invalid IP address: {v}") from err
    
    @field_validator('bgp_asn')
    def validate_asn(cls, v: int) -> int:
        """Validate BGP ASN."""
        # Common private ASN range: 64512-65534
        # AWS default: 64512
        if not (1 <= v <= 4294967295):
            raise ValueError(f"BGP ASN must be between 1 and 4294967295, got: {v}")
        return v


class VPNIntent(BaseModel):
    """Intent for VPN connection."""
    
    enabled: bool = Field(default=False, description="Enable VPN")
    customer_gateway: Optional[CustomerGatewayIntent] = Field(
        None, description="Customer gateway configuration"
    )
    static_routes_only: bool = Field(
        default=False, description="Use static routes (False = BGP)"
    )
    static_routes: list[str] = Field(
        default_factory=list, description="Static routes (if not using BGP)"
    )
    amazon_side_asn: Optional[int] = Field(
        None, description="Amazon side BGP ASN (default: 64512)"
    )
    
    @field_validator('static_routes')
    def validate_static_routes(cls, v: list[str]) -> list[str]:
        """Validate static route CIDR blocks."""
        for route in v:
            try:
                ipaddress.ip_network(route, strict=False)
            except ValueError as err:
                raise ValueError(f"Invalid static route CIDR: {route}") from err
        return v
    
    @field_validator('amazon_side_asn')
    def validate_amazon_asn(cls, v: Optional[int]) -> Optional[int]:
        """Validate Amazon side ASN."""
        if v is not None and not (1 <= v <= 4294967295):
            raise ValueError(f"Amazon side ASN must be between 1 and 4294967295, got: {v}")
        return v


class AWSNetworkIntent(BaseModel):
    """
    Complete AWS network intent.
    
    Declarative configuration for AWS VPC, subnets, and VPN.
    Similar to TriHaulIntent pattern from SROS automation.
    """
    
    # AWS configuration
    region: str = Field(default="us-east-1", description="AWS region")
    environment: Literal["dev", "staging", "prod"] = Field(
        default="dev", description="Environment name"
    )
    project_name: str = Field(default="cloud-lab", description="Project name")
    
    # VPC configuration
    vpc: VPCIntent = Field(..., description="VPC configuration")
    
    # VPN configuration (optional)
    vpn: Optional[VPNIntent] = Field(None, description="VPN configuration")
    
    # Features
    enable_nat_gateway: bool = Field(
        default=False, description="Enable NAT gateway for private subnets"
    )
    enable_flow_logs: bool = Field(
        default=False, description="Enable VPC flow logs"
    )
    
    @field_validator('region')
    def validate_region(cls, v: str) -> str:
        """Validate AWS region format."""
        # Basic validation - should match pattern like us-east-1
        if not v or len(v) < 9:
            raise ValueError(f"Invalid AWS region: {v}")
        return v
    
    @field_validator('vpn')
    def validate_vpn_config(cls, v: Optional[VPNIntent]) -> Optional[VPNIntent]:
        """Validate VPN configuration."""
        if v and v.enabled:
            if not v.customer_gateway:
                raise ValueError("VPN enabled but customer_gateway not configured")
            if v.static_routes_only and not v.static_routes:
                raise ValueError("static_routes_only enabled but no static_routes provided")
        return v
    
    def to_pulumi_config(self) -> dict:
        """
        Convert intent to Pulumi configuration format.
        
        Returns:
            dict: Pulumi configuration
        """
        config = {
            "vpc_cidr": self.vpc.cidr_block,
            "enable_vpn": self.vpn.enabled if self.vpn else False,
            "enable_nat_gateway": self.enable_nat_gateway,
            "enable_flow_logs": self.enable_flow_logs
        }
        
        if self.vpn and self.vpn.enabled and self.vpn.customer_gateway:
            config["customer_gateway_ip"] = self.vpn.customer_gateway.ip_address
            config["customer_bgp_asn"] = self.vpn.customer_gateway.bgp_asn
        
        return config


# Example usage patterns
def create_basic_vpc_intent() -> AWSNetworkIntent:
    """Create a basic VPC intent (no VPN)."""
    return AWSNetworkIntent(
        project_name="basic-lab",
        environment="dev",
        vpc=VPCIntent(
            cidr_block="10.0.0.0/16",
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


def create_vpc_with_vpn_intent(customer_ip: str) -> AWSNetworkIntent:
    """Create VPC with VPN intent."""
    return AWSNetworkIntent(
        project_name="hybrid-lab",
        environment="dev",
        vpc=VPCIntent(
            cidr_block="10.0.0.0/16",
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
        ),
        vpn=VPNIntent(
            enabled=True,
            customer_gateway=CustomerGatewayIntent(
                ip_address=customer_ip,
                bgp_asn=65000,
                device_name="lab-router"
            ),
            static_routes_only=False  # Use BGP
        )
    )
