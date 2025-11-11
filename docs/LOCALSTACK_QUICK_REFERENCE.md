# LocalStack Quick Reference

**One-page cheat sheet for LocalStack with Cloud Networking Lab**

---

## 🚀 Quick Start

```bash
# 1. Start LocalStack
docker compose up -d

# 2. Deploy infrastructure
./scripts/deploy_local.sh

# 3. Make changes, redeploy
cd pulumi && pulumi up

# 4. Clean up
./scripts/destroy_local.sh
docker compose down
```

---

## 📝 Common Commands

### **LocalStack Management**

```bash
# Start
docker compose up -d

# Stop
docker compose down

# Restart
docker compose restart

# View logs
docker compose logs -f localstack

# Check health
curl http://localhost:4566/_localstack/health

# Reset everything
docker compose down -v && rm -rf localstack-data
```

### **Pulumi Operations**

```bash
# Deploy to LocalStack
cd pulumi
pulumi stack select local
pulumi up

# Deploy to AWS
pulumi stack select dev
pulumi up

# Preview changes
pulumi preview

# View outputs
pulumi stack output

# Destroy resources
pulumi destroy
```

### **AWS CLI (LocalStack)**

```bash
# Install awslocal
pip install awscli-local

# List VPCs
awslocal ec2 describe-vpcs

# List subnets
awslocal ec2 describe-subnets

# List security groups
awslocal ec2 describe-security-groups

# List EC2 instances
awslocal ec2 describe-instances
```

---

## 🎯 When to Use Each

| Task | Use |
|------|-----|
| Daily development | LocalStack ✅ |
| Testing changes | LocalStack ✅ |
| Learning/experimenting | LocalStack ✅ |
| Debugging | LocalStack ✅ |
| Portfolio screenshots | AWS 📸 |
| Final validation | AWS ✅ |
| Public demos | AWS 🌐 |

---

## 📊 Deployment Scripts

```bash
# LocalStack
./scripts/deploy_local.sh    # Deploy
./scripts/destroy_local.sh   # Destroy

# AWS
./scripts/deploy_aws.sh      # Deploy
./scripts/destroy_aws.sh     # Destroy (IMPORTANT!)
```

---

## 🐛 Quick Troubleshooting

**LocalStack won't start?**
```bash
docker ps                    # Check Docker
lsof -i :4566               # Check port
docker compose logs         # Check logs
```

**Can't deploy?**
```bash
pulumi stack ls             # Verify stack
docker compose ps           # Check LocalStack
curl localhost:4566/_localstack/health
```

**Resources missing?**
```bash
pulumi stack output         # Check deployment
awslocal ec2 describe-vpcs  # Verify resources
docker compose logs --tail=50
```

---

## 💡 Pro Tips

```bash
# ✅ Always develop on LocalStack first
# ✅ Destroy AWS resources immediately after testing
# ✅ Use awslocal for LocalStack commands
# ✅ Check logs when things don't work
# ❌ Don't leave AWS resources running
# ❌ Don't deploy every change to AWS
```

---

## 📁 File Locations

```
Cloud_Networking_Lab/
├── docker-compose.yml              # LocalStack config
├── localstack-data/                # LocalStack data
├── pulumi/
│   ├── Pulumi.local.yaml          # LocalStack stack
│   └── Pulumi.dev.yaml            # AWS stack
└── scripts/
    ├── deploy_local.sh            # LocalStack deploy
    ├── deploy_aws.sh              # AWS deploy
    ├── destroy_local.sh           # LocalStack cleanup
    └── destroy_aws.sh             # AWS cleanup
```

---

## 🎓 Workflow Examples

**Making a change:**
```bash
docker compose up -d
vim pulumi/__main__.py
cd pulumi && pulumi up
# Test locally (5 seconds, $0)
```

**Adding security rule:**
```bash
vim pulumi/__main__.py  # Add rule
pulumi preview          # Check
pulumi up               # Deploy (instant!)
awslocal ec2 describe-security-groups  # Verify
```

**Portfolio validation:**
```bash
./scripts/deploy_aws.sh         # Deploy to AWS
# Take screenshots
./scripts/destroy_aws.sh        # Clean up
# Total: 1 hour, $0
```

---

## 💰 Cost Summary

| Environment | Cost | Speed | Use For |
|-------------|------|-------|---------|
| **LocalStack** | $0 | 5 sec | 95% of development |
| **AWS** | $0* | 2 min | 5% validation |

*Free tier + immediate destroy

---

**Keep this handy!** Print or bookmark for quick reference.
