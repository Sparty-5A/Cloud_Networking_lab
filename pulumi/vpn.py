"""
VPN module for AWS Cloud Networking Lab.

Provides functions to create site-to-site VPN connections with BGP support.
"""

from typing import Optional

import pulumi_aws as aws

import pulumi


def create_vpn_gateway(
    name: str,
    vpc_id: pulumi.Input[str],
    amazon_side_asn: Optional[int] = None,
    tags: Optional[dict] = None
) -> aws.ec2.VpnGateway:
    """
    Create a VPN Gateway attached to a VPC.
    
    Args:
        name: Resource name
        vpc_id: VPC ID to attach to
        amazon_side_asn: Amazon side BGP ASN (default: 64512)
        tags: Additional tags
        
    Returns:
        aws.ec2.VpnGateway: The VPN gateway
    """
    if tags is None:
        tags = {}
    
    vgw_args = {
        "vpc_id": vpc_id,
        "tags": {"Name": name, **tags}
    }
    
    if amazon_side_asn:
        vgw_args["amazon_side_asn"] = amazon_side_asn
    
    vpn_gateway = aws.ec2.VpnGateway(name, **vgw_args)
    
    pulumi.log.info(f"Creating VPN Gateway: {name}")
    
    return vpn_gateway


def create_customer_gateway(
    name: str,
    ip_address: str,
    bgp_asn: int,
    device_name: Optional[str] = None,
    tags: Optional[dict] = None
) -> aws.ec2.CustomerGateway:
    """
    Create a Customer Gateway (on-prem side).
    
    Args:
        name: Resource name
        ip_address: Public IP of customer gateway
        bgp_asn: BGP ASN for customer side
        device_name: Optional device name
        tags: Additional tags
        
    Returns:
        aws.ec2.CustomerGateway: The customer gateway
    """
    if tags is None:
        tags = {}
    
    cgw_args = {
        "bgp_asn": bgp_asn,
        "ip_address": ip_address,
        "type": "ipsec.1",
        "tags": {"Name": name, **tags}
    }
    
    if device_name:
        cgw_args["device_name"] = device_name
    
    customer_gateway = aws.ec2.CustomerGateway(name, **cgw_args)
    
    pulumi.log.info(f"Creating Customer Gateway: {name} at {ip_address}")
    
    return customer_gateway


def create_vpn_connection(
    name: str,
    vpn_gateway_id: pulumi.Input[str],
    customer_gateway_id: pulumi.Input[str],
    type: str = "ipsec.1",
    static_routes_only: bool = False,
    tunnel1_inside_cidr: Optional[str] = None,
    tunnel2_inside_cidr: Optional[str] = None,
    tunnel1_preshared_key: Optional[str] = None,
    tunnel2_preshared_key: Optional[str] = None,
    tags: Optional[dict] = None
) -> aws.ec2.VpnConnection:
    """
    Create a VPN connection between VGW and CGW.
    
    Args:
        name: Resource name
        vpn_gateway_id: VPN gateway ID
        customer_gateway_id: Customer gateway ID
        type: Connection type (always "ipsec.1")
        static_routes_only: Use static routes (False = BGP)
        tunnel1_inside_cidr: Inside CIDR for tunnel 1
        tunnel2_inside_cidr: Inside CIDR for tunnel 2
        tunnel1_preshared_key: Pre-shared key for tunnel 1
        tunnel2_preshared_key: Pre-shared key for tunnel 2
        tags: Additional tags
        
    Returns:
        aws.ec2.VpnConnection: The VPN connection
    """
    if tags is None:
        tags = {}
    
    vpn_args = {
        "vpn_gateway_id": vpn_gateway_id,
        "customer_gateway_id": customer_gateway_id,
        "type": type,
        "static_routes_only": static_routes_only,
        "tags": {"Name": name, **tags}
    }
    
    # Optional tunnel configuration
    if tunnel1_inside_cidr:
        vpn_args["tunnel1_inside_cidr"] = tunnel1_inside_cidr
    if tunnel2_inside_cidr:
        vpn_args["tunnel2_inside_cidr"] = tunnel2_inside_cidr
    if tunnel1_preshared_key:
        vpn_args["tunnel1_preshared_key"] = tunnel1_preshared_key
    if tunnel2_preshared_key:
        vpn_args["tunnel2_preshared_key"] = tunnel2_preshared_key
    
    vpn_connection = aws.ec2.VpnConnection(name, **vpn_args)
    
    pulumi.log.info(f"Creating VPN Connection: {name} (BGP: {not static_routes_only})")
    
    return vpn_connection


def create_vpn_connection_route(
    name: str,
    vpn_connection_id: pulumi.Input[str],
    destination_cidr_block: str
) -> aws.ec2.VpnConnectionRoute:
    """
    Create a static route for VPN connection.
    
    Only used when static_routes_only=True on VPN connection.
    
    Args:
        name: Resource name
        vpn_connection_id: VPN connection ID
        destination_cidr_block: Destination CIDR for route
        
    Returns:
        aws.ec2.VpnConnectionRoute: The VPN route
    """
    vpn_route = aws.ec2.VpnConnectionRoute(
        name,
        vpn_connection_id=vpn_connection_id,
        destination_cidr_block=destination_cidr_block
    )
    
    return vpn_route
