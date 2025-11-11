# LocalStack Setup Guide

Complete guide for using LocalStack with your Cloud Networking Lab.

---

## 🎯 What is LocalStack?

**LocalStack** is a cloud service emulator that runs AWS services locally on your computer.

**Think of it as:**
> "AWS running on your laptop - free, fast, and offline"

**Benefits:**
- ✅ $0 cost (unlimited usage)
- ✅ 10-20x faster than real AWS
- ✅ No fear of surprise bills
- ✅ Works offline
- ✅ Instant reset/cleanup
- ✅ Perfect for learning

---

## 📋 Prerequisites

Before starting, ensure you have:

- [x] Docker installed (you have 28.1.1 ✅)
- [x] Docker Compose available
- [x] Pulumi CLI installed
- [x] Python virtual environment activated

**Verify Docker Compose:**
```bash
docker compose version
# Should show: Docker Compose version v2.x.x
```

---

## 🚀 Quick Start

### **Step 1: Copy Files to Your Project**

```bash
cd ~/Cloud_Networking_Lab

# Copy LocalStack configuration files
cp /path/to/docker-compose.yml ./
cp /path/to/Pulumi.local.yaml ./pulumi/

# Copy deployment scripts
cp /path/to/deploy_local.sh ./scripts/
cp /path/to/deploy_aws.sh ./scripts/
cp /path/to/destroy_local.sh ./scripts/
cp /path/to/destroy_aws.sh ./scripts/

# Make scripts executable
chmod +x scripts/*.sh
```

### **Step 2: Start LocalStack**

```bash
# Start LocalStack in background
docker compose up -d

# Check status
docker compose ps

# Should see:
# NAME                              STATUS
# cloud-networking-lab-localstack   Up (healthy)
```

### **Step 3: Verify LocalStack is Running**

```bash
# Check health endpoint
curl http://localhost:4566/_localstack/health

# Should return JSON with service statuses
```

### **Step 4: Deploy to LocalStack**

```bash
# Option A: Use script (recommended)
./scripts/deploy_local.sh

# Option B: Manual deployment
cd pulumi
pulumi stack select local --create
pulumi up
```

### **Step 5: View Your Infrastructure**

```bash
# In pulumi directory
pulumi stack output

# Example output:
# vpc_id: vpc-12345678
# vpc_cidr: 10.0.0.0/16
# public_subnet_a_id: subnet-abcdef01
# internet_gateway_id: igw-98765432
```

---

## 🔍 Verifying Deployment

### **Check VPC in LocalStack:**

```bash
# Install awslocal (if not installed)
pip install awscli-local

# List VPCs
awslocal ec2 describe-vpcs

# List subnets
awslocal ec2 describe-subnets

# List security groups
awslocal ec2 describe-security-groups
```

### **View LocalStack Logs:**

```bash
# Follow logs in real-time
docker compose logs -f localstack

# View recent logs
docker compose logs --tail=100 localstack
```

---

## 📊 LocalStack vs AWS: When to Use Each

### **Use LocalStack For:**

**Daily Development:**
```bash
✅ Making code changes
✅ Testing new features
✅ Debugging issues
✅ Learning AWS services
✅ Experimenting with configurations
✅ Running tests

Cost: $0
Speed: Instant (5-10 seconds)
Risk: None
```

**Example workflow:**
```bash
# Morning: Start LocalStack
docker compose up -d

# Deploy
./scripts/deploy_local.sh

# Make changes to pulumi/__main__.py
vim pulumi/__main__.py

# Redeploy (takes 5 seconds!)
cd pulumi && pulumi up

# Test, iterate, repeat...
# Cost: $0, unlimited iterations
```

### **Use Real AWS For:**

**Validation & Portfolio:**
```bash
✅ Final validation before portfolio
✅ Taking screenshots
✅ Recording demos
✅ Testing public internet access
✅ Verifying everything works in real AWS

Cost: $0 (free tier if brief)
Speed: 2-3 minutes
Risk: Low (destroy immediately after)
```

**Example workflow:**
```bash
# Deploy to AWS
./scripts/deploy_aws.sh

# Test web server publicly
curl $(cd pulumi && pulumi stack output web_server_url)

# Take screenshots
# - AWS Console
# - Web browser
# - Pulumi outputs

# Destroy immediately
./scripts/destroy_aws.sh

# Total time: 1-2 hours
# Total cost: $0 (free tier)
```

---

## 🎓 Development Workflow

### **Recommended Daily Workflow:**

```bash
# 1. Start your day
cd ~/Cloud_Networking_Lab
docker compose up -d
source .venv/bin/activate

# 2. Deploy current state to LocalStack
./scripts/deploy_local.sh

# 3. Make changes (edit code)
vim pulumi/__main__.py

# 4. Test changes locally
cd pulumi
pulumi preview  # See what will change
pulumi up       # Deploy changes (5 seconds!)

# 5. Verify it works
pulumi stack output
awslocal ec2 describe-vpcs

# 6. Make more changes, repeat steps 3-5
# (Unlimited iterations, $0 cost!)

# 7. End of day
pulumi destroy  # Clean up LocalStack
docker compose down
```

### **Weekly AWS Validation:**

```bash
# Once per week (or before showing portfolio)

# 1. Deploy to AWS
./scripts/deploy_aws.sh

# 2. Test everything
curl http://$(cd pulumi && pulumi stack output web_server_url)

# 3. Take screenshots
# - AWS Console showing VPC
# - EC2 Console showing instance
# - Web browser showing your site
# - Terminal showing pulumi outputs

# 4. Destroy immediately
./scripts/destroy_aws.sh

# Total time: 1 hour
# Cost: $0
```

---

## 🛠️ Common Tasks

### **Start LocalStack:**
```bash
docker compose up -d
```

### **Stop LocalStack:**
```bash
docker compose down
```

### **Reset LocalStack (fresh start):**
```bash
docker compose down -v
rm -rf localstack-data
docker compose up -d
```

### **View LocalStack UI (optional):**
Visit: http://localhost:4566/_localstack/health

### **Deploy Infrastructure:**
```bash
./scripts/deploy_local.sh
```

### **Destroy Infrastructure:**
```bash
./scripts/destroy_local.sh
```

### **Check Resource Status:**
```bash
# VPCs
awslocal ec2 describe-vpcs

# Subnets
awslocal ec2 describe-subnets

# EC2 instances
awslocal ec2 describe-instances

# Security Groups
awslocal ec2 describe-security-groups
```

### **Switch Between LocalStack and AWS:**

```bash
# Deploy to LocalStack
cd pulumi
pulumi stack select local
pulumi up

# Deploy to AWS
pulumi stack select dev
pulumi up

# Switch back
pulumi stack select local
```

---

## 🐛 Troubleshooting

### **LocalStack won't start:**

**Problem:** `docker compose up` fails

**Solution:**
```bash
# Check Docker is running
docker ps

# Check port 4566 isn't in use
lsof -i :4566

# Try stopping and restarting
docker compose down
docker compose up -d
```

### **Can't connect to LocalStack:**

**Problem:** `Connection refused` when deploying

**Solution:**
```bash
# Check LocalStack health
curl http://localhost:4566/_localstack/health

# Check Docker logs
docker compose logs localstack

# Restart LocalStack
docker compose restart localstack
```

### **Pulumi deployment fails:**

**Problem:** Errors during `pulumi up`

**Solution:**
```bash
# Verify you're on local stack
pulumi stack ls
# Should show: local*

# Check LocalStack is running
docker compose ps

# Check Pulumi config
pulumi config
# Should show LocalStack endpoints

# Reset and try again
pulumi stack rm local --yes
pulumi stack init local
./scripts/deploy_local.sh
```

### **Resources not appearing in LocalStack:**

**Problem:** `awslocal` commands show no resources

**Solution:**
```bash
# Check deployment succeeded
cd pulumi
pulumi stack output

# Verify correct endpoint
awslocal --endpoint-url=http://localhost:4566 ec2 describe-vpcs

# Check LocalStack logs for errors
docker compose logs --tail=50 localstack
```

### **"Endpoint not available" errors:**

**Problem:** Service endpoint errors

**Solution:**
```bash
# Check which services LocalStack is running
curl http://localhost:4566/_localstack/health | jq

# Restart with specific services
docker compose down
# Edit docker-compose.yml SERVICES if needed
docker compose up -d
```

---

## 💡 Tips & Best Practices

### **Development Best Practices:**

**1. Always start with LocalStack**
```bash
# ✅ Good: Develop locally first
docker compose up -d
./scripts/deploy_local.sh
# ... make changes ...

# ❌ Bad: Deploy every change to AWS
./scripts/deploy_aws.sh  # Don't do this for every change!
```

**2. Use meaningful stack names**
```bash
local  → LocalStack development
dev    → Real AWS development/testing
prod   → Real AWS production (if you deploy)
```

**3. Always destroy when done**
```bash
# LocalStack
pulumi destroy  # Clean up

# Real AWS - CRITICAL!
./scripts/destroy_aws.sh  # Avoid charges!
```

**4. Keep LocalStack data separate**
```bash
# Add to .gitignore
localstack-data/
```

### **Cost Optimization:**

**Use LocalStack for:**
- ✅ All development (90%+ of time)
- ✅ All testing
- ✅ All experimentation
- ✅ All learning

**Use Real AWS only for:**
- ✅ Final validation (1-2 hours)
- ✅ Screenshots (30 minutes)
- ✅ Demos (30 minutes)
- ✅ Then destroy immediately!

**Result:** 95%+ of work at $0 cost ✅

---

## 📊 Feature Compatibility

### **What Works 100% on LocalStack:**

Your Phase 1 features:
- ✅ VPC creation
- ✅ Subnets (public/private)
- ✅ Internet Gateway
- ✅ Route Tables
- ✅ Routes
- ✅ Security Groups (all rules)
- ✅ EC2 Instances
- ✅ Elastic IPs

**Confidence Level:** Can develop entirely on LocalStack ✅

### **What Has Limitations:**

Phase 2 features:
- ⚠️ VPN Gateway - Basic support
- ⚠️ VPN Connection - No actual IPSec tunnels
- ⚠️ VPC Flow Logs - Simulated
- ⚠️ CloudWatch - Basic metrics

**Recommendation:** Use LocalStack for Phase 1, Real AWS for Phase 2 VPN

---

## 🎯 Next Steps

### **You're Ready When:**

- [x] LocalStack starts successfully
- [x] `docker compose ps` shows healthy
- [x] `./scripts/deploy_local.sh` works
- [x] `pulumi stack output` shows resources
- [x] `awslocal ec2 describe-vpcs` returns your VPC

### **Try These:**

**1. Deploy to LocalStack:**
```bash
./scripts/deploy_local.sh
```

**2. Make a change:**
```bash
# Edit security group to add port 8080
vim pulumi/__main__.py
# Add new ingress rule
```

**3. Redeploy (instant!):**
```bash
cd pulumi && pulumi up
```

**4. Verify:**
```bash
awslocal ec2 describe-security-groups
```

**5. Experiment:**
- Add/remove subnets
- Change CIDR blocks
- Modify security rules
- Break things and fix them!
- Cost: $0, unlimited tries ✅

---

## 📚 Additional Resources

### **LocalStack:**
- Docs: https://docs.localstack.cloud
- Coverage: https://docs.localstack.cloud/references/coverage/
- Slack: https://localstack.cloud/slack

### **AWS Local CLI:**
- GitHub: https://github.com/localstack/awscli-local
- Install: `pip install awscli-local`
- Usage: `awslocal` instead of `aws`

### **Your Project:**
- Main docs: `docs/GETTING_STARTED.md`
- Architecture: `docs/architecture.md`
- Troubleshooting: `docs/troubleshooting.md`

---

## 🎉 You're All Set!

**LocalStack is now integrated with your Cloud Networking Lab!**

**What this gives you:**
- ⚡ Instant deployments (5 seconds vs 2 minutes)
- 💰 $0 cost (unlimited iterations)
- 🧪 Safe experimentation (no fear of breaking things)
- 🎓 Better learning (try things without worry)
- 💼 Professional workflow (modern DevOps practice)

**Start developing:**
```bash
docker compose up -d
./scripts/deploy_local.sh
# Start coding! 🚀
```

---

**Happy Local Cloud Development!** ☁️✨
