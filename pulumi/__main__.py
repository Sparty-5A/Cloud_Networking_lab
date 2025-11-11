"""
Solution 1A: Basic VPC for SaaS MVP Launch

Business Context:
- Target: Pre-revenue SaaS startups
- Budget: $8-15/month
- Traffic: < 10K requests/day
- Uptime: 95-99%

Architecture:
- Single region (us-east-1)
- Multi-AZ for resilience
- Public subnets for web tier
- Internet Gateway for connectivity

Cost Optimization:
- t3.micro instances (free tier eligible)
- No NAT Gateway (saves $32/month)
- No load balancer (saves $16/month)
- Minimal data transfer

Scaling Path:
- Solution 1B: Add ALB + auto-scaling (~$60/mo)
- Solution 1C: Add private subnets + RDS (~$250/mo)
"""

import pulumi
import pulumi_aws as aws
from typing import Dict, Any
from pathlib import Path
import yaml

# Import our modules
from vpc import create_vpc, enable_vpc_flow_logs
from networking import create_subnets, create_internet_gateway, create_route_tables
from vpn import create_vpn_gateway, create_customer_gateway, create_vpn_connection

# Configuration
config = pulumi.Config()
aws_config = pulumi.Config("aws")

# Get configuration values
vpc_cidr = config.get("vpc_cidr") or "10.0.0.0/16"
enable_vpn = config.get_bool("enable_vpn") or False
enable_flow_logs = config.get_bool("enable_flow_logs") or False
project_name = pulumi.get_project()
stack_name = pulumi.get_stack()

# Tags for all resources
common_tags = {
    "Project": project_name,
    "Stack": stack_name,
    "Environment": stack_name,
    "ManagedBy": "Pulumi",
    "Purpose": "CloudNetworkingLab"
}

# ==========================================
# VPC
# ==========================================

vpc = create_vpc(
    name=f"{project_name}-vpc",
    cidr_block=vpc_cidr,
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={**common_tags, "Name": f"{project_name}-vpc-{stack_name}"}
)

# ==========================================
# VPC Flow Logs (Optional)
# ==========================================

if enable_flow_logs:
    pulumi.log.info(f"Enabling VPC Flow Logs for {project_name}-vpc")

    flow_log = enable_vpc_flow_logs(
        name=f"{project_name}-flow-log",
        vpc_id=vpc.id,
        traffic_type="ALL",
        tags={**common_tags, "Name": f"{project_name}-flow-log-{stack_name}"}
    )

# ==========================================
# Internet Gateway
# ==========================================

igw = create_internet_gateway(
    name=f"{project_name}-igw",
    vpc_id=vpc.id,
    tags={**common_tags, "Name": f"{project_name}-igw-{stack_name}"}
)

# ==========================================
# Subnets (Multi-AZ)
# ==========================================

# Public subnet in AZ-A
public_subnet_a = aws.ec2.Subnet(
    f"{project_name}-public-a",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="us-east-1a",
    map_public_ip_on_launch=True,
    tags={**common_tags, "Name": f"{project_name}-public-a-{stack_name}"}
)

# Public subnet in AZ-B
public_subnet_b = aws.ec2.Subnet(
    f"{project_name}-public-b",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    availability_zone="us-east-1b",
    map_public_ip_on_launch=True,
    tags={**common_tags, "Name": f"{project_name}-public-b-{stack_name}"}
)

public_subnet_c = aws.ec2.Subnet(
    f"{project_name}-public-c",
    vpc_id=vpc.id,
    cidr_block="10.0.3.0/24",
    availability_zone="us-east-1c",
    map_public_ip_on_launch=True,
    tags={**common_tags, "Name": f"{project_name}-public-c-{stack_name}"}
)

# ==========================================
# Route Tables
# ==========================================

# Public route table
public_route_table = aws.ec2.RouteTable(
    f"{project_name}-public-rt",
    vpc_id=vpc.id,
    tags={**common_tags, "Name": f"{project_name}-public-rt-{stack_name}"}
)

# Route to Internet Gateway
public_route = aws.ec2.Route(
    f"{project_name}-public-route",
    route_table_id=public_route_table.id,
    destination_cidr_block="0.0.0.0/0",
    gateway_id=igw.id
)

# Associate route table with public subnets
public_rt_assoc_a = aws.ec2.RouteTableAssociation(
    f"{project_name}-public-rt-assoc-a",
    subnet_id=public_subnet_a.id,
    route_table_id=public_route_table.id
)

public_rt_assoc_b = aws.ec2.RouteTableAssociation(
    f"{project_name}-public-rt-assoc-b",
    subnet_id=public_subnet_b.id,
    route_table_id=public_route_table.id
)

# ==========================================
# VPN Gateway (Optional)
# ==========================================

vpn_gateway = None
customer_gateway = None
vpn_connection = None

if enable_vpn:
    pulumi.log.info(f"Enabling VPN Gateway for {project_name}-vpc")

    # VPN Gateway
    vpn_gateway = create_vpn_gateway(
        name=f"{project_name}-vgw",
        vpc_id=vpc.id,
        tags={**common_tags, "Name": f"{project_name}-vgw-{stack_name}"}
    )

    # Customer Gateway (on-prem side)
    # Note: Replace with your actual public IP
    customer_public_ip = config.get("customer_gateway_ip") or "1.2.3.4"  # Placeholder
    customer_bgp_asn = config.get_int("customer_bgp_asn") or 65000

    customer_gateway = create_customer_gateway(
        name=f"{project_name}-cgw",
        ip_address=customer_public_ip,
        bgp_asn=customer_bgp_asn,
        tags={**common_tags, "Name": f"{project_name}-cgw-{stack_name}"}
    )

    # VPN Connection
    vpn_connection = create_vpn_connection(
        name=f"{project_name}-vpn",
        vpn_gateway_id=vpn_gateway.id,
        customer_gateway_id=customer_gateway.id,
        type="ipsec.1",
        static_routes_only=False,  # Use BGP
        tags={**common_tags, "Name": f"{project_name}-vpn-{stack_name}"}
    )

    # Enable route propagation for VPN
    vpn_route_propagation = aws.ec2.VpnGatewayRoutePropagation(
        f"{project_name}-vpn-route-propagation",
        vpn_gateway_id=vpn_gateway.id,
        route_table_id=public_route_table.id
    )

# ==========================================
# Security Groups
# ==========================================

# Default security group for resources in this VPC
default_sg = aws.ec2.SecurityGroup(
    f"{project_name}-default-sg",
    vpc_id=vpc.id,
    description="Default security group for Cloud Networking Lab",
    ingress=[
        # Allow ICMP (ping) from VPC
        aws.ec2.SecurityGroupIngressArgs(
            protocol="icmp",
            from_port=-1,
            to_port=-1,
            cidr_blocks=[vpc_cidr]
        ),
        # Allow SSH from anywhere (restrict in production!)
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"]
        ),
        # Allow HTTP from anywhere (for web server)
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=80,
            to_port=80,
            cidr_blocks=["0.0.0.0/0"]
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=8080,
            to_port=8080,
            cidr_blocks=["0.0.0.0/0"],
            description="Test port"
        ),
        # Allow HTTPS from anywhere (for future use)
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=443,
            to_port=443,
            cidr_blocks=["0.0.0.0/0"]
        ),
        # Allow all traffic within VPC
        aws.ec2.SecurityGroupIngressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=[vpc_cidr]
        )
    ],
    egress=[
        # Allow all outbound traffic
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"]
        )
    ],
    tags={**common_tags, "Name": f"{project_name}-default-sg-{stack_name}"}
)

# ==========================================
# EC2 Web Server (Optional)
# ==========================================

# Get latest Amazon Linux 2023 AMI
ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["amazon"],
    filters=[
        aws.ec2.GetAmiFilterArgs(name="name", values=["al2023-ami-*-x86_64"]),
        aws.ec2.GetAmiFilterArgs(name="state", values=["available"]),
    ]
)

# Launch web server if enabled
enable_web_server = config.get_bool("enable_web_server") or False

web_server = None  # Initialize

if enable_web_server:
    pulumi.log.info(f"Launching web server in {project_name}-vpc")

    # User data script to install and configure nginx
    user_data = """#!/bin/bash
# Update system
yum update -y

# Install nginx
yum install -y nginx

# Get instance metadata
HOSTNAME=$(hostname)
PRIVATE_IP=$(hostname -I | awk '{print $1}')
AZ=$(ec2-metadata --availability-zone | cut -d ' ' -f 2)
INSTANCE_ID=$(ec2-metadata --instance-id | cut -d ' ' -f 2)

# Create simple webpage
cat > /usr/share/nginx/html/index.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Cloud Networking Lab</title>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 30px;
            backdrop-filter: blur(10px);
        }
        h1 { margin-top: 0; }
        .info { background: rgba(0,0,0,0.2); padding: 15px; border-radius: 5px; margin: 10px 0; }
        .success { color: #00ff00; font-weight: bold; }
        .checkmark { color: #00ff00; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Cloud Networking Lab</h1>
        <p class="success"><span class="checkmark">&#10003;</span> Web server is running!</p>
        
        <div class="info">
            <h3>Server Information:</h3>
            <p><strong>Hostname:</strong> $HOSTNAME</p>
            <p><strong>Private IP:</strong> $PRIVATE_IP</p>
            <p><strong>Availability Zone:</strong> $AZ</p>
            <p><strong>Instance ID:</strong> $INSTANCE_ID</p>
        </div>
        
        <div class="info">
            <h3>What You Built:</h3>
            <ul>
                <li><span class="checkmark">&#10003;</span> VPC with multi-AZ subnets</li>
                <li><span class="checkmark">&#10003;</span> Internet Gateway for public access</li>
                <li><span class="checkmark">&#10003;</span> Route tables with proper routing</li>
                <li><span class="checkmark">&#10003;</span> Security groups protecting resources</li>
                <li><span class="checkmark">&#10003;</span> EC2 instance running nginx web server</li>
            </ul>
        </div>
        
        <div class="info">
            <h3>Deployed with:</h3>
            <p>&#9658; Pulumi (Infrastructure as Code)</p>
            <p>&#9658; Python (Real programming language)</p>
            <p>&#9658; Pydantic (Type-safe configuration)</p>
            <p>&#9658; AWS (Cloud infrastructure)</p>
        </div>
        
        <p style="text-align: center; margin-top: 30px; opacity: 0.7;">
            <small>Cloud Networking Lab - Phase 1 Complete</small>
        </p>
    </div>
</body>
</html>
EOF

# Start and enable nginx
systemctl start nginx
systemctl enable nginx

# Configure firewall
systemctl stop firewalld
systemctl disable firewalld
"""

    # Create EC2 instance
    web_server = aws.ec2.Instance(
        f"{project_name}-web-server",
        instance_type="t3.micro",  # New free tier (post July 2025) - uses credits!
        ami=ami.id,
        subnet_id=public_subnet_a.id,
        vpc_security_group_ids=[default_sg.id],
        user_data=user_data,
        associate_public_ip_address=True,
        tags={**common_tags, "Name": f"{project_name}-web-server-{stack_name}"}
    )

# ==========================================
# Exports (Pulumi Stack Outputs)
# ==========================================

# VPC information
pulumi.export("vpc_id", vpc.id)
pulumi.export("vpc_cidr", vpc.cidr_block)

# Subnet information
pulumi.export("public_subnet_a_id", public_subnet_a.id)
pulumi.export("public_subnet_a_cidr", public_subnet_a.cidr_block)
pulumi.export("public_subnet_a_az", public_subnet_a.availability_zone)

pulumi.export("public_subnet_b_id", public_subnet_b.id)
pulumi.export("public_subnet_b_cidr", public_subnet_b.cidr_block)
pulumi.export("public_subnet_b_az", public_subnet_b.availability_zone)

pulumi.export("public_subnet_c_id", public_subnet_c.id)
pulumi.export("public_subnet_c_cidr", public_subnet_c.cidr_block)
pulumi.export("public_subnet_c_az", public_subnet_c.availability_zone)

# Gateway information
pulumi.export("internet_gateway_id", igw.id)

# Route table information
pulumi.export("public_route_table_id", public_route_table.id)

# Security group information
pulumi.export("default_security_group_id", default_sg.id)

# Flow logs information (if enabled)
if enable_flow_logs:
    pulumi.export("flow_logs_enabled", True)
    pulumi.export("flow_log_id", flow_log.id)

# Web server information (if enabled)
if enable_web_server and web_server:
    pulumi.export("web_server_id", web_server.id)
    pulumi.export("web_server_public_ip", web_server.public_ip)
    pulumi.export("web_server_private_ip", web_server.private_ip)
    pulumi.export("web_server_url", web_server.public_ip.apply(lambda ip: f"http://{ip}"))

# VPN information (if enabled)
if enable_vpn and vpn_gateway:
    pulumi.export("vpn_gateway_id", vpn_gateway.id)

if enable_vpn and customer_gateway:
    pulumi.export("customer_gateway_id", customer_gateway.id)
    pulumi.export("customer_gateway_ip", customer_gateway.ip_address)

if enable_vpn and vpn_connection:
    pulumi.export("vpn_connection_id", vpn_connection.id)
    pulumi.export("vpn_connection_type", vpn_connection.type)
    # Note: VPN configuration details available via CLI: pulumi stack output --show-secrets

# Summary message
summary_parts = [
    f"✓ VPC deployed successfully in {stack_name} environment.",
    f"VPN {'enabled' if enable_vpn else 'disabled'}.",
    f"Flow logs {'enabled' if enable_flow_logs else 'disabled'}.",
    f"Web server {'enabled' if enable_web_server else 'disabled'}."
]

pulumi.export("deployment_message", " ".join(summary_parts))