#!/bin/bash
# Destroy AWS infrastructure
#
# Clean up all resources in real AWS to avoid costs

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${RED}🗑️  Cloud Networking Lab - AWS Cleanup${NC}"
echo "=================================================="
echo ""

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}❌ AWS credentials not configured.${NC}"
    exit 1
fi

echo -e "${BLUE}🔐 AWS Account:${NC}"
aws sts get-caller-identity
echo ""

echo -e "${YELLOW}⚠️  This will DESTROY all resources in AWS!${NC}"
echo ""
echo "Resources to be deleted:"
echo "  • VPC and all subnets"
echo "  • Internet Gateway"
echo "  • Route tables"
echo "  • Security groups"
echo "  • EC2 instances (if any)"
echo "  • VPN Gateway (if enabled)"
echo ""

read -p "Are you sure you want to destroy everything? (yes/no): " -r
echo
if [[ ! $REPLY =~ ^[Yy]es$ ]]; then
    echo -e "${YELLOW}Destruction cancelled.${NC}"
    exit 0
fi

cd pulumi

pulumi stack select dev

echo ""
echo -e "${BLUE}📋 Preview of what will be destroyed:${NC}"
pulumi destroy

cd ..

echo ""
echo -e "${GREEN}✅ All AWS resources destroyed${NC}"
echo -e "${GREEN}💰 Your AWS bill is now back to $0${NC}"
echo ""
