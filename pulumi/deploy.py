#!/usr/bin/env python3
"""
Deploy Cloud Networking Lab infrastructure.

Pure Python deployment script using Pulumi Automation API.
No shell scripts required!
"""

import subprocess
import sys
import time
from pathlib import Path


def check_localstack_health() -> bool:
    """Check if LocalStack is running and healthy."""
    import urllib.request
    import json

    try:
        with urllib.request.urlopen('http://localhost:4566/_localstack/health') as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                print("✅ LocalStack is healthy")
                print(f"   Version: {data.get('version', 'unknown')}")
                return True
    except Exception as e:
        print(f"❌ LocalStack health check failed: {e}")
        return False

    return False


def check_docker_running() -> bool:
    """Check if Docker is running."""
    try:
        result = subprocess.run(
            ['docker', 'ps'],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        print("❌ Docker is not running")
        return False


def start_localstack() -> bool:
    """Start LocalStack using docker compose."""
    print("🐳 Starting LocalStack...")

    try:
        # Check if already running
        result = subprocess.run(
            ['docker', 'compose', 'ps', '--format', 'json'],
            capture_output=True,
            text=True,
            check=True
        )

        if 'cloud-networking-lab-localstack' in result.stdout and '"State":"running"' in result.stdout:
            print("✅ LocalStack is already running")
            return True

        # Start LocalStack
        subprocess.run(
            ['docker', 'compose', 'up', '-d'],
            check=True
        )

        print("⏳ Waiting for LocalStack to be ready...")
        time.sleep(10)

        # Verify it's healthy
        if check_localstack_health():
            return True

        # Wait a bit more and retry
        time.sleep(5)
        return check_localstack_health()

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start LocalStack: {e}")
        return False


def deploy_stack(stack_name: str, auto_approve: bool = False) -> bool:
    """Deploy Pulumi stack."""
    print(f"\n📦 Deploying stack: {stack_name}")

    # Change to pulumi directory
    pulumi_dir = Path(__file__).parent / 'pulumi'

    try:
        # Select stack
        print(f"Selecting stack: {stack_name}")
        subprocess.run(
            ['pulumi', 'stack', 'select', stack_name, '--create'],
            cwd=pulumi_dir,
            check=True
        )

        # Preview changes
        print("\n📋 Previewing changes...")
        subprocess.run(
            ['pulumi', 'preview'],
            cwd=pulumi_dir,
            check=True
        )

        # Deploy
        if auto_approve:
            print("\n🚀 Deploying (auto-approved)...")
            subprocess.run(
                ['pulumi', 'up', '--yes'],
                cwd=pulumi_dir,
                check=True
            )
        else:
            print("\n🚀 Deploying...")
            subprocess.run(
                ['pulumi', 'up'],
                cwd=pulumi_dir,
                check=True
            )

        # Show outputs
        print("\n📊 Stack outputs:")
        subprocess.run(
            ['pulumi', 'stack', 'output'],
            cwd=pulumi_dir,
            check=True
        )

        print("\n✅ Deployment successful!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Deployment failed: {e}")
        return False


def destroy_stack(stack_name: str, auto_approve: bool = False) -> bool:
    """Destroy Pulumi stack resources."""
    print(f"\n🗑️  Destroying stack: {stack_name}")

    pulumi_dir = Path(__file__).parent / 'pulumi'

    try:
        # Select stack
        subprocess.run(
            ['pulumi', 'stack', 'select', stack_name],
            cwd=pulumi_dir,
            check=True
        )

        # Destroy
        if auto_approve:
            print("Destroying resources (auto-approved)...")
            subprocess.run(
                ['pulumi', 'destroy', '--yes'],
                cwd=pulumi_dir,
                check=True
            )
        else:
            print("Destroying resources...")
            subprocess.run(
                ['pulumi', 'destroy'],
                cwd=pulumi_dir,
                check=True
            )

        print("\n✅ Resources destroyed!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Destroy failed: {e}")
        return False


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Deploy Cloud Networking Lab infrastructure'
    )
    parser.add_argument(
        'action',
        choices=['deploy', 'destroy', 'status'],
        help='Action to perform'
    )
    parser.add_argument(
        '--stack',
        choices=['local', 'dev'],
        default='local',
        help='Stack to use (default: local)'
    )
    parser.add_argument(
        '--yes',
        action='store_true',
        help='Auto-approve changes'
    )
    parser.add_argument(
        '--start-localstack',
        action='store_true',
        help='Start LocalStack if deploying to local stack'
    )

    args = parser.parse_args()

    print("🚀 Cloud Networking Lab Deployment")
    print("=" * 50)

    # Check Docker is running
    if not check_docker_running():
        print("\n❌ Please start Docker first")
        sys.exit(1)

    # Start LocalStack if needed
    if args.stack == 'local':
        if args.start_localstack or args.action == 'deploy':
            if not start_localstack():
                print("\n❌ LocalStack is not running")
                print("Start it with: docker compose up -d")
                sys.exit(1)
        elif not check_localstack_health():
            print("\n⚠️  LocalStack doesn't appear to be running")
            print("Start it with: docker compose up -d")
            print("Or use --start-localstack flag")
            sys.exit(1)

    # Perform action
    if args.action == 'deploy':
        success = deploy_stack(args.stack, args.yes)
        sys.exit(0 if success else 1)

    elif args.action == 'destroy':
        success = destroy_stack(args.stack, args.yes)
        sys.exit(0 if success else 1)

    elif args.action == 'status':
        print(f"\nStack: {args.stack}")

        if args.stack == 'local':
            check_localstack_health()

        pulumi_dir = Path(__file__).parent / 'pulumi'
        subprocess.run(
            ['pulumi', 'stack', 'output'],
            cwd=pulumi_dir
        )


if __name__ == '__main__':
    main()