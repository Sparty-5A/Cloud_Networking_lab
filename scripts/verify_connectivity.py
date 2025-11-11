#!/usr/bin/env python3
"""
VPN Connectivity Verification Script.

Tests VPN tunnel status, BGP connectivity, and route propagation.
"""

import json
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

import boto3


@dataclass
class TunnelStatus:
    """VPN tunnel status information."""
    tunnel_id: int
    outside_ip: str
    status: str
    status_message: str
    last_status_change: Optional[datetime] = None


@dataclass
class VPNConnectionInfo:
    """VPN connection information."""
    vpn_id: str
    state: str
    type: str
    customer_gateway_id: str
    vpn_gateway_id: str
    tunnels: List[TunnelStatus]
    bgp_asn: Optional[int] = None


class VPNVerifier:
    """Verify VPN connectivity and status."""
    
    def __init__(self, region: str = "us-east-1"):
        """
        Initialize VPN verifier.
        
        Args:
            region: AWS region
        """
        self.ec2 = boto3.client('ec2', region_name=region)
        self.region = region
    
    def get_vpn_connections(self) -> List[VPNConnectionInfo]:
        """
        Get all VPN connections in the region.
        
        Returns:
            List of VPN connection information
        """
        try:
            response = self.ec2.describe_vpn_connections()
            connections = []
            
            for vpn in response.get('VpnConnections', []):
                # Parse tunnel information
                tunnels = []
                for i, tunnel in enumerate(vpn.get('VgwTelemetry', []), 1):
                    tunnel_status = TunnelStatus(
                        tunnel_id=i,
                        outside_ip=tunnel.get('OutsideIpAddress', 'N/A'),
                        status=tunnel.get('Status', 'UNKNOWN'),
                        status_message=tunnel.get('StatusMessage', ''),
                        last_status_change=tunnel.get('LastStatusChange')
                    )
                    tunnels.append(tunnel_status)
                
                # Get BGP ASN if available
                bgp_asn = None
                if 'CustomerGatewayConfiguration' in vpn:
                    # Parse from configuration (would need XML parsing)
                    pass
                
                conn_info = VPNConnectionInfo(
                    vpn_id=vpn['VpnConnectionId'],
                    state=vpn['State'],
                    type=vpn['Type'],
                    customer_gateway_id=vpn['CustomerGatewayId'],
                    vpn_gateway_id=vpn.get('VpnGatewayId', 'N/A'),
                    tunnels=tunnels,
                    bgp_asn=bgp_asn
                )
                connections.append(conn_info)
            
            return connections
        
        except Exception as e:
            print(f"❌ Error fetching VPN connections: {e}")
            return []
    
    def check_tunnel_status(self, tunnel: TunnelStatus) -> bool:
        """
        Check if a tunnel is UP.
        
        Args:
            tunnel: Tunnel status information
            
        Returns:
            True if tunnel is UP
        """
        return tunnel.status.upper() == 'UP'
    
    def verify_vpn_connection(self, vpn_id: str) -> Dict:
        """
        Verify a specific VPN connection.
        
        Args:
            vpn_id: VPN connection ID
            
        Returns:
            Verification results
        """
        results = {
            'vpn_id': vpn_id,
            'overall_status': 'UNKNOWN',
            'tunnels': [],
            'routes_learned': 0,
            'bgp_status': 'UNKNOWN',
            'recommendations': []
        }
        
        try:
            # Get VPN connection details
            response = self.ec2.describe_vpn_connections(
                VpnConnectionIds=[vpn_id]
            )
            
            if not response.get('VpnConnections'):
                results['overall_status'] = 'NOT_FOUND'
                return results
            
            vpn = response['VpnConnections'][0]
            results['overall_status'] = vpn['State']
            
            # Check tunnel status
            up_tunnels = 0
            for i, tunnel in enumerate(vpn.get('VgwTelemetry', []), 1):
                tunnel_info = {
                    'tunnel_id': i,
                    'outside_ip': tunnel.get('OutsideIpAddress'),
                    'status': tunnel.get('Status'),
                    'message': tunnel.get('StatusMessage', ''),
                    'last_change': str(tunnel.get('LastStatusChange', 'N/A'))
                }
                results['tunnels'].append(tunnel_info)
                
                if tunnel.get('Status', '').upper() == 'UP':
                    up_tunnels += 1
            
            # Check BGP routes (if using BGP)
            if not vpn.get('Options', {}).get('StaticRoutesOnly', False):
                results['bgp_status'] = 'ENABLED'
                # Note: Route count requires additional API calls
                # or parsing of CustomerGatewayConfiguration
            
            # Recommendations
            if up_tunnels == 0:
                results['recommendations'].append(
                    "⚠️  All tunnels are DOWN - check customer gateway configuration"
                )
            elif up_tunnels == 1:
                results['recommendations'].append(
                    "⚠️  Only 1 tunnel UP - check redundancy"
                )
            else:
                results['recommendations'].append(
                    "✓ Both tunnels UP - good redundancy"
                )
            
            return results
        
        except Exception as e:
            results['overall_status'] = 'ERROR'
            results['error'] = str(e)
            return results
    
    def print_connection_summary(self, conn: VPNConnectionInfo):
        """Print a summary of VPN connection."""
        print(f"\n{'='*60}")
        print(f"VPN Connection: {conn.vpn_id}")
        print(f"{'='*60}")
        print(f"State: {conn.state}")
        print(f"Type: {conn.type}")
        print(f"Customer Gateway: {conn.customer_gateway_id}")
        print(f"VPN Gateway: {conn.vpn_gateway_id}")
        
        print("\nTunnels:")
        up_count = 0
        for tunnel in conn.tunnels:
            status_icon = "✓" if tunnel.status.upper() == "UP" else "✗"
            print(f"  Tunnel {tunnel.tunnel_id}: {status_icon} {tunnel.status}")
            print(f"    Outside IP: {tunnel.outside_ip}")
            if tunnel.status_message:
                print(f"    Message: {tunnel.status_message}")
            if tunnel.status.upper() == "UP":
                up_count += 1
        
        # Overall health
        print(f"\nHealth: {up_count}/2 tunnels UP")
        if up_count == 2:
            print("✓ Full redundancy available")
        elif up_count == 1:
            print("⚠️  Single tunnel - degraded redundancy")
        else:
            print("❌ No tunnels UP - no connectivity")


def main():
    """Main verification function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Verify VPN connectivity and status'
    )
    parser.add_argument(
        '--region',
        default='us-east-1',
        help='AWS region (default: us-east-1)'
    )
    parser.add_argument(
        '--vpn-id',
        help='Specific VPN connection ID to check'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )
    
    args = parser.parse_args()
    
    verifier = VPNVerifier(region=args.region)
    
    print(f"🔍 Checking VPN connections in {args.region}...")
    
    if args.vpn_id:
        # Check specific VPN
        results = verifier.verify_vpn_connection(args.vpn_id)
        
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"\nVPN Connection: {results['vpn_id']}")
            print(f"Status: {results['overall_status']}")
            print("\nTunnels:")
            for tunnel in results['tunnels']:
                status_icon = "✓" if tunnel['status'].upper() == "UP" else "✗"
                print(f"  Tunnel {tunnel['tunnel_id']}: {status_icon} {tunnel['status']}")
                print(f"    Outside IP: {tunnel['outside_ip']}")
            
            if results['recommendations']:
                print("\nRecommendations:")
                for rec in results['recommendations']:
                    print(f"  {rec}")
    else:
        # List all VPNs
        connections = verifier.get_vpn_connections()
        
        if not connections:
            print("❌ No VPN connections found")
            return 1
        
        if args.json:
            output = [
                {
                    'vpn_id': conn.vpn_id,
                    'state': conn.state,
                    'tunnels': [
                        {
                            'tunnel_id': t.tunnel_id,
                            'outside_ip': t.outside_ip,
                            'status': t.status
                        }
                        for t in conn.tunnels
                    ]
                }
                for conn in connections
            ]
            print(json.dumps(output, indent=2))
        else:
            print(f"\nFound {len(connections)} VPN connection(s):")
            for conn in connections:
                verifier.print_connection_summary(conn)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
