#!/bin/bash
# Deploy Cloud Networking Lab to Real AWS
#
# This script deploys your infrastructure to actual AWS for validation,
# screenshots, and portfolio demonstrations.

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}☁️  Cloud Networking Lab - AWS Deployment${NC}"
echo "=================================================="
echo ""

# Check if AWS credentials are configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}❌ AWS credentials not configured.${NC}"
    echo ""
    echo "Please configure AWS credentials first:"
    echo "  aws configure"
    echo ""
    exit 1
fi

# Show AWS account info
echo -e "${BLUE}🔐 AWS Account:${NC}"
aws sts get-caller-identity
echo ""

# Warning about costs
echo -e "${YELLOW}⚠️  WARNING: This will deploy to REAL AWS${NC}"
echo ""
echo "Estimated costs:"
echo "  • VPC, Subnets, IGW: $0 (always free)"
echo "  • EC2 t3.micro: $0 (free tier: 750 hrs/month)"
echo "  • VPN Gateway: ~$36/month (if enabled)"
echo ""
echo -e "${YELLOW}💡 Remember to run 'pulumi destroy' when done!${NC}"
echo ""

# Confirm deployment
read -p "Continue with AWS deployment? (yes/no): " -r
echo
if [[ ! $REPLY =~ ^[Yy]es$ ]]; then
    echo -e "${YELLOW}Deployment cancelled.${NC}"
    exit 0
fi

# Navigate to pulumi directory
cd pulumi

# Select or create dev stack
echo -e "${BLUE}Selecting 'dev' stack...${NC}"
pulumi stack select dev --create 2>/dev/null || pulumi stack select dev

# Preview changes
echo ""
echo -e "${BLUE}📋 Preview of changes:${NC}"
pulumi preview

# Confirm again after seeing preview
echo ""
read -p "Deploy these changes to AWS? (yes/no): " -r
echo
if [[ ! $REPLY =~ ^[Yy]es$ ]]; then
    echo -e "${YELLOW}Deployment cancelled.${NC}"
    cd ..
    exit 0
fi

# Deploy!
echo -e "${GREEN}🚀 Deploying to AWS...${NC}"
pulumi up

# Show outputs
echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo -e "${BLUE}📊 Stack outputs:${NC}"
pulumi stack output

# Check if web server is enabled
if pulumi stack output web_server_url &> /dev/null; then
    WEB_URL=$(pulumi stack output web_server_url)
    echo ""
    echo -e "${GREEN}🌐 Web Server URL:${NC}"
    echo "  $WEB_URL"
    echo ""
    echo -e "${BLUE}💡 Test it:${NC}"
    echo "  curl $WEB_URL"
    echo "  # Or open in browser"
fi

# Return to project root
cd ..

echo ""
echo -e "${GREEN}🎉 Success! Your infrastructure is running on AWS.${NC}"
echo ""
echo -e "${YELLOW}💰 Cost reminder:${NC}"
echo "  • Don't forget to destroy when done: ./scripts/destroy_aws.sh"
echo "  • Or manually: cd pulumi && pulumi destroy"
echo ""
echo -e "${BLUE}📸 Portfolio tips:${NC}"
echo "  • Take screenshots of AWS Console"
echo "  • Screenshot the web server in browser"
echo "  • Run 'pulumi stack output' and screenshot"
echo "  • Test from different device/network"
echo ""
