#!/usr/bin/env python3
"""
AWS Architecture Diagram Generator

Generates visual diagrams of your Pulumi infrastructure.
Reads Pulumi state and creates beautiful architecture diagrams.
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import (
    VPC,
    InternetGateway,
    PublicSubnet,
    RouteTable,
    NATGateway,
    ELB
)
from diagrams.aws.database import RDS
import json
import subprocess
from pathlib import Path


def get_stack_outputs():
    """Get Pulumi stack outputs."""
    try:
        # Find pulumi directory
        pulumi_dir = Path('pulumi')
        if not pulumi_dir.exists():
            pulumi_dir = Path('..')

        result = subprocess.run(
            ['pulumi', 'stack', 'output', '--json'],
            capture_output=True,
            text=True,
            check=True,
            cwd=str(pulumi_dir)
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Warning: Could not get Pulumi outputs: {e}")
        print(f"  stderr: {e.stderr}")
        print("  Tip: Make sure you're in Cloud_Networking_Lab directory")
        print("       and have run 'pulumi up' successfully")
        return {}
    except Exception as e:
        print(f"Error getting outputs: {e}")
        return {}


def generate_current_architecture():
    """Generate diagram of current deployed infrastructure."""

    print("📊 Generating architecture diagram...")

    # Get outputs
    outputs = get_stack_outputs()

    # Create diagram
    graph_attr = {
        "fontsize": "16",
        "bgcolor": "white",
        "pad": "0.5",
        "splines": "ortho"
    }

    with Diagram(
            "Cloud Networking Lab - Current Architecture",
            show=False,
            direction="TB",
            filename="diagrams/current_architecture",
            graph_attr=graph_attr
    ):

        with Cluster("Internet"):
            internet = InternetGateway("Internet Gateway")

        with Cluster(f"AWS Cloud (LocalStack)\nVPC: {outputs.get('vpc_cidr', '10.0.0.0/16')}"):

            igw = InternetGateway("IGW")
            rt = RouteTable("Route Table")

            # Connect internet to IGW
            internet >> Edge(color="darkgreen", style="bold") >> igw
            igw >> Edge(label="0.0.0.0/0") >> rt

            with Cluster("Availability Zone: us-east-1a"):
                subnet_a = PublicSubnet(
                    f"Public Subnet A\n{outputs.get('public_subnet_a_cidr', '10.0.1.0/24')}"
                )

                if 'web_server_id' in outputs:
                    web_a = EC2(
                        f"Web Server\n{outputs.get('web_server_private_ip', 'N/A')}"
                    )
                    rt >> subnet_a >> web_a
                else:
                    rt >> subnet_a

            with Cluster("Availability Zone: us-east-1b"):
                subnet_b = PublicSubnet(
                    f"Public Subnet B\n{outputs.get('public_subnet_b_cidr', '10.0.2.0/24')}"
                )
                rt >> subnet_b

            # Check for subnet C
            if 'public_subnet_c_cidr' in outputs:
                with Cluster("Availability Zone: us-east-1c"):
                    subnet_c = PublicSubnet(
                        f"Public Subnet C\n{outputs.get('public_subnet_c_cidr', '10.0.3.0/24')}"
                    )
                    rt >> subnet_c

    print("✅ Diagram generated: diagrams/current_architecture.png")


def generate_basic_vpc_diagram():
    """Generate diagram showing basic VPC architecture."""

    print("📊 Generating basic VPC diagram...")

    with Diagram(
            "Solution 1: Basic VPC Architecture",
            show=False,
            direction="TB",
            filename="diagrams/solution_01_basic_vpc",
            graph_attr={"fontsize": "16", "bgcolor": "white", "splines": "ortho"}
    ):
        with Cluster("Internet"):
            internet = InternetGateway("Internet")

        with Cluster("AWS Cloud\nVPC: 10.0.0.0/16"):
            igw = InternetGateway("Internet Gateway")

            with Cluster("Public Subnet: 10.0.1.0/24\nAvailability Zone: us-east-1a"):
                web = EC2("Web Server\nt3.micro\nNginx")

            internet >> igw >> web

    print("✅ Diagram generated: diagrams/solution_01_basic_vpc.png")


def generate_ha_web_diagram():
    """Generate HA web application with load balancer."""

    print("📊 Generating HA web application diagram...")

    with Diagram(
            "Solution 2: High Availability Web Application",
            show=False,
            direction="TB",
            filename="diagrams/solution_02_ha_web",
            graph_attr={"fontsize": "16", "bgcolor": "white", "splines": "ortho"}
    ):
        with Cluster("Internet"):
            internet = InternetGateway("Internet")

        with Cluster("AWS Cloud\nVPC: 10.0.0.0/16"):
            igw = InternetGateway("Internet Gateway")
            alb = ELB("Application\nLoad Balancer")

            with Cluster("Availability Zone: us-east-1a"):
                with Cluster("Public Subnet: 10.0.1.0/24"):
                    web1 = EC2("Web Server 1\nt3.micro")

            with Cluster("Availability Zone: us-east-1b"):
                with Cluster("Public Subnet: 10.0.2.0/24"):
                    web2 = EC2("Web Server 2\nt3.micro")

            internet >> igw >> alb
            alb >> Edge(label="health checks") >> [web1, web2]

    print("✅ Diagram generated: diagrams/solution_02_ha_web.png")


def generate_multi_tier_diagram():
    """Generate multi-tier architecture diagram."""

    print("📊 Generating multi-tier architecture diagram...")

    with Diagram(
            "Solution 3: Multi-Tier Architecture",
            show=False,
            direction="TB",
            filename="diagrams/solution_03_multi_tier",
            graph_attr={"fontsize": "16", "bgcolor": "white", "splines": "ortho"}
    ):
        with Cluster("Internet"):
            internet = InternetGateway("Internet")

        with Cluster("AWS Cloud\nVPC: 10.0.0.0/16"):
            igw = InternetGateway("Internet Gateway")
            nat = NATGateway("NAT Gateway")
            alb = ELB("Application\nLoad Balancer")

            with Cluster("Public Tier (DMZ)"):
                with Cluster("AZ-A: 10.0.1.0/24"):
                    web1 = EC2("Web 1")

                with Cluster("AZ-B: 10.0.2.0/24"):
                    web2 = EC2("Web 2")

            with Cluster("Private Application Tier"):
                with Cluster("AZ-A: 10.0.11.0/24"):
                    app1 = EC2("App 1")

                with Cluster("AZ-B: 10.0.12.0/24"):
                    app2 = EC2("App 2")

            with Cluster("Private Data Tier"):
                db = RDS("RDS Database\nMulti-AZ\nPostgreSQL")

            # Connections
            internet >> igw >> alb
            alb >> [web1, web2]
            web1 >> [app1, app2]
            web2 >> [app1, app2]
            [app1, app2] >> db
            [app1, app2] >> nat >> igw

    print("✅ Diagram generated: diagrams/solution_03_multi_tier.png")


def generate_all_diagrams():
    """Generate all architecture diagrams."""

    # Create diagrams directory
    Path("diagrams").mkdir(exist_ok=True)

    print("\n🎨 AWS Architecture Diagram Generator")
    print("=" * 50)

    # Generate current architecture
    try:
        generate_current_architecture()
    except Exception as e:
        print(f"⚠️  Could not generate current architecture: {e}")
        print("    (Make sure you've run 'pulumi up' first)")

    # Generate solution templates
    generate_basic_vpc_diagram()
    generate_ha_web_diagram()
    generate_multi_tier_diagram()

    print("\n✅ All diagrams generated successfully!")
    print("\n📂 Diagrams saved to: ./diagrams/")
    print("\nGenerated diagrams:")
    print("  • current_architecture.png - Your deployed infrastructure")
    print("  • solution_01_basic_vpc.png - Basic VPC pattern")
    print("  • solution_02_ha_web.png - HA web application")
    print("  • solution_03_multi_tier.png - Multi-tier architecture")

    print("\n💡 Open diagrams with:")
    print("  xdg-open diagrams/current_architecture.png")
    print("  # or")
    print("  nautilus diagrams/")


def main():
    """Main entry point."""
    import sys

    try:
        generate_all_diagrams()
    except ImportError as e:
        print("\n❌ Error: 'diagrams' library not installed")
        print("\nInstall with:")
        print("  uv add diagrams")
        print("  # or")
        print("  pip install diagrams")
        print("\nAlso install Graphviz:")
        print("  sudo apt-get install graphviz")
        print("\nThen run this script again.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()