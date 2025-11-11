#!/bin/bash
# Destroy LocalStack infrastructure
#
# Clean up all resources in LocalStack

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🧹 Destroying LocalStack infrastructure...${NC}"
echo ""

cd pulumi

pulumi stack select local

echo -e "${BLUE}Destroying resources...${NC}"
pulumi destroy --yes

cd ..

echo ""
echo -e "${GREEN}✅ Resources destroyed${NC}"
echo ""
echo "LocalStack is still running. To stop it:"
echo "  docker compose down"
echo ""
echo "To remove all data:"
echo "  docker compose down -v"
echo "  rm -rf localstack-data"
echo ""
