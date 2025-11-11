#!/bin/bash
# Deploy Cloud Networking Lab to LocalStack
#
# This script starts LocalStack and deploys your infrastructure locally
# for fast, free development and testing.

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐳 Cloud Networking Lab - LocalStack Deployment${NC}"
echo "=================================================="
echo ""

# Check if docker-compose is available
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}❌ Docker not found. Please install Docker first.${NC}"
    exit 1
fi

# Check if we're in the project root
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${YELLOW}❌ docker-compose.yml not found. Please run from project root.${NC}"
    exit 1
fi

# Start LocalStack
echo -e "${GREEN}🚀 Starting LocalStack...${NC}"
docker compose up -d

# Wait for LocalStack to be ready
echo -e "${BLUE}⏳ Waiting for LocalStack to be ready...${NC}"
sleep 5

# Check LocalStack health
echo -e "${BLUE}🔍 Checking LocalStack health...${NC}"
if curl -s http://localhost:4566/_localstack/health > /dev/null; then
    echo -e "${GREEN}✅ LocalStack is healthy${NC}"
else
    echo -e "${YELLOW}⚠️  LocalStack may not be fully ready yet...${NC}"
    echo -e "${BLUE}Waiting 10 more seconds...${NC}"
    sleep 10
fi

echo ""
echo -e "${GREEN}📦 Deploying to LocalStack...${NC}"
echo ""

# Navigate to pulumi directory
cd pulumi

# Select or create local stack
echo -e "${BLUE}Selecting 'local' stack...${NC}"
pulumi stack select local --create 2>/dev/null || pulumi stack select local

# Preview changes (optional - comment out if you want to skip)
echo ""
echo -e "${BLUE}📋 Preview of changes:${NC}"
pulumi preview

# Ask for confirmation
echo ""
read -p "Deploy these changes? (yes/no): " -r
echo
if [[ ! $REPLY =~ ^[Yy]es$ ]]; then
    echo -e "${YELLOW}Deployment cancelled.${NC}"
    cd ..
    exit 0
fi

# Deploy!
echo -e "${GREEN}🚀 Deploying...${NC}"
pulumi up --yes

# Show outputs
echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo -e "${BLUE}📊 Stack outputs:${NC}"
pulumi stack output

# Return to project root
cd ..

echo ""
echo -e "${GREEN}🎉 Success! Your infrastructure is running on LocalStack.${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  • View LocalStack logs: docker compose logs -f"
echo "  • Check AWS resources: awslocal ec2 describe-vpcs"
echo "  • Make changes and redeploy: ./scripts/deploy_local.sh"
echo "  • Destroy resources: cd pulumi && pulumi destroy"
echo "  • Stop LocalStack: docker compose down"
echo ""
