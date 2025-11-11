# Quick Reference Card - Cloud Networking Lab

**Keep this handy for quick command reference!**

---

## ⚡ **Daily Workflow**

```bash
# 1. Navigate and activate venv (ALWAYS DO THIS FIRST!)
cd ~/Cloud_Networking_Lab
source .venv/bin/activate

# 2. Run tests (verify everything works)
pytest -v

# 3. Deploy infrastructure
cd pulumi
pulumi preview  # Check what will change
pulumi up       # Deploy changes

# 4. View results
pulumi stack output
```

---

## 🔑 **Essential Commands**

### **Project Setup (one-time)**
```bash
cd ~/Cloud_Networking_Lab
uv sync --extra dev  # Install dependencies
```

### **Testing**
```bash
pytest -v                              # All tests
pytest tests/unit/test_aws_intent.py   # Specific test
pytest --cov                           # With coverage
```

### **Pulumi Deployment**
```bash
cd pulumi

pulumi preview                    # Dry-run (see what will change)
pulumi up                         # Deploy/update
pulumi up --yes                   # Auto-approve
pulumi destroy                    # Delete everything
pulumi stack output               # View outputs
pulumi stack output vpc_id        # Specific output
```

### **Pulumi State**
```bash
pulumi stack                      # Current stack info
pulumi stack ls                   # List all stacks
pulumi stack history              # Deployment history
pulumi refresh                    # Sync state with AWS
```

### **Configuration**
```bash
pulumi config set aws:region us-east-1
pulumi config set vpc_cidr 10.0.0.0/16
pulumi config set enable_vpn false
pulumi config                     # View all config
```

---

## 🌐 **AWS Console Links**

**VPC Dashboard:**  
https://console.aws.amazon.com/vpc/home?region=us-east-1

**Specific Resources:**
- VPCs: https://console.aws.amazon.com/vpc/#vpcs
- Subnets: https://console.aws.amazon.com/vpc/#subnets
- Internet Gateways: https://console.aws.amazon.com/vpc/#igws
- Route Tables: https://console.aws.amazon.com/vpc/#RouteTables
- Security Groups: https://console.aws.amazon.com/vpc/#securityGroups

---

## 💰 **Cost Management**

```bash
# Current setup (VPN disabled)
Cost: $0/month ✅

# If you enable VPN
VPN Gateway: ~$36/month ⚠️

# ALWAYS destroy when done testing:
pulumi destroy
```

---

## 🔧 **Troubleshooting**

### **"No module named 'pulumi'"**
```bash
# Make sure venv is activated!
source .venv/bin/activate
cd pulumi
pulumi up
```

### **Passphrase prompts every time**
```bash
# Set environment variable
export PULUMI_CONFIG_PASSPHRASE="your-passphrase"

# Or add to ~/.bashrc:
echo 'export PULUMI_CONFIG_PASSPHRASE="your-passphrase"' >> ~/.bashrc
```

### **AWS credential errors**
```bash
# Check credentials configured
aws sts get-caller-identity

# If not, configure:
aws configure
```

### **"Resource already exists"**
```bash
# Refresh state from AWS
pulumi refresh

# Or import existing resource
pulumi import aws:ec2/vpc:Vpc my-vpc vpc-xxxxx
```

---

## 📚 **Documentation Locations**

```
docs/GETTING_STARTED.md    # First deployment guide
docs/setup_guide.md        # Installation & setup
docs/pulumi_guide.md       # How Pulumi works (detailed!)
PROJECT_COMPLETE.md        # What we built summary
README.md                  # Project overview
```

---

## 🎯 **Your Current Deployment**

```
Stack:      dev
Region:     us-east-1
VPC ID:     vpc-06f243cd89e27f2de
VPC CIDR:   10.0.0.0/16
Subnets:    2 (us-east-1a, us-east-1b)
VPN:        Disabled
Cost:       $0/month
```

---

## 🚀 **What's Next**

**Before Next Session:**
1. [ ] Push project to GitHub
2. [ ] Decide: Ubuntu VM or Nokia SROS for on-prem?
3. [ ] Get your public IP for VPN config
4. [ ] (Optional) Destroy AWS resources to save costs

**Phase 2 (Next Session):**
- Configure on-prem router (Ubuntu/SROS)
- Enable VPN Gateway in AWS
- Establish IPSec tunnels
- Configure BGP peering
- Test end-to-end connectivity

---

## 📞 **Quick Help**

**Pulumi Docs:** https://www.pulumi.com/docs/  
**AWS VPC Docs:** https://docs.aws.amazon.com/vpc/  
**Your Documentation:** `docs/` folder in project

---

## 💡 **Pro Tips**

1. **Always activate .venv first!**
   ```bash
   source .venv/bin/activate
   ```

2. **Preview before deploying**
   ```bash
   pulumi preview  # Check first
   pulumi up       # Then deploy
   ```

3. **Destroy when done testing**
   ```bash
   pulumi destroy  # Save money!
   ```

4. **Check AWS Console to verify**
   - See your resources visually
   - Verify everything created correctly

---

**Save this file for quick reference!**

Generated: October 30, 2025
