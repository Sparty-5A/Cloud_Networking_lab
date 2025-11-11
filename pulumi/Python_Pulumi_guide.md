# Python-Only Deployment Guide

**Pure Python + Pulumi approach - No shell scripts!**

---

## 🐍 **Philosophy**

Keep everything in Python:
- ✅ Infrastructure: Python + Pulumi
- ✅ Deployment: Python scripts
- ✅ Configuration: Pulumi config (YAML)
- ✅ No bash/shell scripts needed

---

## 📋 **File Structure**

```
Cloud_Networking_Lab/
├── deploy.py                 # Main deployment script (Python!)
├── docker-compose.yml        # LocalStack config
│
├── pulumi/
│   ├── __main__.py          # Infrastructure code
│   ├── vpc.py
│   ├── vpn.py
│   ├── networking.py
│   ├── Pulumi.yaml          # Project config
│   ├── Pulumi.local.yaml    # LocalStack stack
│   └── Pulumi.dev.yaml      # AWS stack
│
└── models/
    └── aws_intent.py         # Pydantic models
```

---

## 🚀 **Usage**

### **Deploy to LocalStack**

```bash
# Start LocalStack and deploy
python deploy.py deploy --stack local --start-localstack

# Or if LocalStack is already running
python deploy.py deploy --stack local

# Auto-approve (no prompts)
python deploy.py deploy --stack local --yes
```

### **Deploy to AWS**

```bash
# Deploy to real AWS
python deploy.py deploy --stack dev

# Auto-approve
python deploy.py deploy --stack dev --yes
```

### **Destroy Resources**

```bash
# Destroy LocalStack resources
python deploy.py destroy --stack local

# Destroy AWS resources (IMPORTANT!)
python deploy.py destroy --stack dev

# Auto-approve
python deploy.py destroy --stack local --yes
```

### **Check Status**

```bash
# Check LocalStack stack
python deploy.py status --stack local

# Check AWS stack
python deploy.py status --stack dev
```

---

## 🎯 **Direct Pulumi Commands**

You can also use Pulumi directly (pure Python workflow):

### **Deploy**

```bash
cd pulumi

# Select stack
pulumi stack select local   # or: dev

# Preview changes
pulumi preview

# Deploy
pulumi up

# Auto-approve
pulumi up --yes
```

### **Manage Stacks**

```bash
cd pulumi

# List stacks
pulumi stack ls

# Switch stacks
pulumi stack select local
pulumi stack select dev

# View outputs
pulumi stack output

# View specific output
pulumi stack output vpc_id
```

### **Destroy**

```bash
cd pulumi

# Select stack
pulumi stack select local

# Destroy resources
pulumi destroy

# Auto-approve
pulumi destroy --yes
```

---

## ⚙️ **Configuration Management**

### **View Configuration**

```bash
cd pulumi

# Show all config
pulumi config

# Show specific value
pulumi config get vpc_cidr
```

### **Update Configuration**

```bash
cd pulumi

# Set values
pulumi config set vpc_cidr 10.10.0.0/16
pulumi config set enable_web_server true
pulumi config set enable_vpn false

# Set secret (encrypted)
pulumi config set --secret api_key mysecretkey
```

### **Different Config per Stack**

LocalStack stack (`Pulumi.local.yaml`):
```yaml
config:
  aws:region: us-east-1
  aws:endpoints:
    - ec2: http://localhost:4566
  cloud-networking-lab:vpc_cidr: 10.0.0.0/16
  cloud-networking-lab:enable_vpn: "false"
```

AWS stack (`Pulumi.dev.yaml`):
```yaml
config:
  aws:region: us-east-1
  cloud-networking-lab:vpc_cidr: 10.0.0.0/16
  cloud-networking-lab:enable_vpn: "false"
```

---

## 🐳 **LocalStack Management**

### **Start/Stop LocalStack**

```bash
# Start
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f localstack

# Stop
docker compose down

# Stop and remove volumes
docker compose down -v
```

### **Check Health**

Python one-liner:
```python
python -c "import urllib.request, json; print(json.loads(urllib.request.urlopen('http://localhost:4566/_localstack/health').read()))"
```

Or using curl:
```bash
curl http://localhost:4566/_localstack/health
```

---

## 🔍 **Verification**

### **Check Resources (LocalStack)**

```bash
# VPCs
awslocal ec2 describe-vpcs

# Subnets
awslocal ec2 describe-subnets

# Security Groups
awslocal ec2 describe-security-groups

# EC2 Instances
awslocal ec2 describe-instances
```

### **Check Resources (AWS)**

```bash
# Same commands, just use 'aws' instead of 'awslocal'
aws ec2 describe-vpcs
aws ec2 describe-subnets
# etc.
```

---

## 📊 **Workflow Examples**

### **Daily Development (LocalStack)**

```bash
# Morning - start LocalStack
docker compose up -d

# Deploy
cd pulumi
pulumi stack select local
pulumi up

# Make changes to code
vim __main__.py

# Redeploy (fast!)
pulumi up --yes

# Check outputs
pulumi stack output

# End of day - cleanup
pulumi destroy --yes
docker compose down
```

### **Weekly Validation (AWS)**

```bash
# Deploy to AWS
cd pulumi
pulumi stack select dev
pulumi up

# Test, take screenshots, etc.

# IMPORTANT: Destroy immediately!
pulumi destroy --yes
```

---

## 🎓 **Python-Only Philosophy**

### **Why Python-Only?**

✅ **Consistency:** Everything in one language  
✅ **Type Safety:** Python type hints throughout  
✅ **IDE Support:** Full autocomplete and linting  
✅ **Testing:** Can write Python tests for everything  
✅ **Debugging:** Use Python debugger everywhere  
✅ **Portability:** Works same on all platforms  

### **What We Avoid:**

❌ Bash scripts (platform-specific)  
❌ Shell commands (hard to debug)  
❌ Mixed languages (context switching)  
❌ Platform dependencies (Linux vs Windows)  

### **What We Use:**

✅ Python scripts (`deploy.py`)  
✅ Pulumi (Python SDK)  
✅ Pydantic (Python validation)  
✅ pytest (Python testing)  
✅ Docker Compose (YAML config, not scripts)  

---

## 🛠️ **Advanced: Pulumi Automation API**

For even more Python control, use the Automation API:

```python
# Example: Programmatic deployment
from pulumi import automation as auto

# Create or select stack
stack = auto.create_or_select_stack(
    stack_name="local",
    project_name="cloud-networking-lab",
    program=lambda: __import__('__main__')
)

# Set config programmatically
stack.set_config("vpc_cidr", auto.ConfigValue(value="10.0.0.0/16"))
stack.set_config("enable_web_server", auto.ConfigValue(value="true"))

# Deploy
up_result = stack.up()
print(f"Update succeeded: {up_result.summary.result}")

# Get outputs
outputs = stack.outputs()
print(f"VPC ID: {outputs['vpc_id'].value}")
```

This gives you **complete programmatic control** in Python!

---

## 📝 **Quick Reference**

### **Common Commands**

| Task | Command |
|------|---------|
| Deploy to LocalStack | `python deploy.py deploy --stack local` |
| Deploy to AWS | `python deploy.py deploy --stack dev` |
| Destroy LocalStack | `python deploy.py destroy --stack local` |
| Destroy AWS | `python deploy.py destroy --stack dev` |
| Check status | `python deploy.py status --stack local` |
| Start LocalStack | `docker compose up -d` |
| Stop LocalStack | `docker compose down` |

### **Pulumi Direct**

| Task | Command |
|------|---------|
| Select stack | `pulumi stack select local` |
| Deploy | `pulumi up` |
| Destroy | `pulumi destroy` |
| View outputs | `pulumi stack output` |
| Set config | `pulumi config set key value` |

---

## ✅ **Pure Python Stack**

```
Infrastructure:     Python + Pulumi
Configuration:      Pydantic models
Deployment:         Python scripts
Testing:            pytest
Validation:         Python
Everything:         Python! 🐍
```

**No shell scripts needed!** 🎉

---

## 🚀 **Get Started**

```bash
# 1. Start LocalStack
docker compose up -d

# 2. Deploy with Python
python deploy.py deploy --stack local --yes

# 3. Make changes
vim pulumi/__main__.py

# 4. Redeploy
cd pulumi && pulumi up --yes

# Done! All Python! 🐍
```

---

**Pure Python Infrastructure as Code!** ✨