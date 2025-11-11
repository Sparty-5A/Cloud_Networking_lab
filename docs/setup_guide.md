# Setup Guide - Cloud Networking Lab

Complete setup instructions for the AWS Cloud Networking Lab project.

---

## 📋 **Prerequisites**

### **Required**
- Python 3.13+ ([Download](https://www.python.org/downloads/))
- uv package manager ([Install](https://docs.astral.sh/uv/))
- AWS Account ([Sign up](https://aws.amazon.com/))
- Pulumi CLI ([Install](https://www.pulumi.com/docs/get-started/install/))
- Git

### **Optional**
- Docker (for LocalStack testing)
- AWS CLI (for manual verification)

---

## 🚀 **Installation**

### **1. Clone the Repository**

```bash
git clone https://github.com/yourusername/Cloud_Networking_Lab.git
cd Cloud_Networking_Lab
```

### **2. Create Virtual Environment**

```bash
# Create venv
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### **3. Install Dependencies**

```bash
# Install dependencies with uv
uv sync

# Or install with dev dependencies
uv sync --all-extras
```

### **4. Configure AWS Credentials**

```bash
# Option A: AWS CLI
aws configure

# Option B: Environment variables
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"
```

### **5. Login to Pulumi**

```bash
# Option A: Pulumi Cloud (free)
pulumi login

# Option B: Local backend
pulumi login --local
```

---

## 🎯 **Quick Start**

### **Deploy Basic VPC**

```bash
cd pulumi

# Initialize stack
pulumi stack init dev

# Set configuration
pulumi config set aws:region us-east-1
pulumi config set vpc_cidr 10.0.0.0/16

# Preview changes
pulumi preview

# Deploy infrastructure
pulumi up

# View outputs
pulumi stack output
```

### **Deploy VPC with VPN**

```bash
# Enable VPN
pulumi config set enable_vpn true

# Configure customer gateway
pulumi config set customer_gateway_ip YOUR_PUBLIC_IP
pulumi config set customer_bgp_asn 65000

# Deploy
pulumi up
```

---

## 🧪 **Running Tests**

### **All Tests**

```bash
cd tests
pytest -v
```

### **Unit Tests Only**

```bash
pytest tests/unit/ -v
```

### **With Coverage**

```bash
pytest --cov=models --cov=pulumi --cov-report=html
open htmlcov/index.html  # View coverage report
```

---

## ✅ **Verify Deployment**

### **Check VPN Status**

```bash
cd scripts
python verify_connectivity.py
```

### **Test from Pulumi**

```bash
cd pulumi
pulumi stack output
```

Expected outputs:
```
vpc_id                  vpc-12345678
vpc_cidr                10.0.0.0/16
public_subnet_a_id      subnet-12345678
internet_gateway_id     igw-12345678
```

---

## 🔧 **Configuration**

### **Using Intent Files (Recommended)**

Create `network-intent.yaml`:

```yaml
network:
  project_name: "my-lab"
  environment: "dev"
  region: "us-east-1"
  
  vpc:
    cidr_block: "10.0.0.0/16"
    enable_dns_hostnames: true
    enable_dns_support: true
    
    subnets:
      - name: "public-a"
        cidr_block: "10.0.1.0/24"
        availability_zone: "us-east-1a"
        public: true
        
      - name: "public-b"
        cidr_block: "10.0.2.0/24"
        availability_zone: "us-east-1b"
        public: true
  
  vpn:
    enabled: true
    customer_gateway:
      ip_address: "203.0.113.1"
      bgp_asn: 65000
      device_name: "lab-router"
    static_routes_only: false
```

Deploy from intent:

```python
from models.aws_intent import AWSNetworkIntent
import yaml

# Load intent
with open("network-intent.yaml") as f:
    config = yaml.safe_load(f)

intent = AWSNetworkIntent(**config['network'])

# Deploy with Pulumi
# (integrate with __main__.py)
```

---

## 📊 **Monitoring**

### **AWS Console**

1. Navigate to VPC Dashboard
2. Check VPN connections
3. View Flow Logs (if enabled)

### **Command Line**

```bash
# VPN status
aws ec2 describe-vpn-connections

# VPC details
aws ec2 describe-vpcs

# Subnet information
aws ec2 describe-subnets
```

---

## 🧹 **Cleanup**

### **Destroy Infrastructure**

```bash
cd pulumi
pulumi destroy

# Confirm with 'yes'
```

### **Remove Stack**

```bash
pulumi stack rm dev
```

---

## 🐛 **Troubleshooting**

### **Pulumi Login Issues**

```bash
# Reset Pulumi credentials
rm -rf ~/.pulumi

# Login again
pulumi login
```

### **AWS Credentials**

```bash
# Verify credentials
aws sts get-caller-identity

# Check region
aws configure get region
```

### **VPN Tunnel DOWN**

1. Check customer gateway public IP
2. Verify BGP ASN configuration
3. Check on-prem firewall rules (UDP 500, 4500)
4. Review VPN logs in AWS console

### **Subnet CIDR Conflicts**

- Ensure subnets don't overlap
- Verify all subnets within VPC CIDR
- Use CIDR calculator: https://www.subnet-calculator.com/

---

## 🔐 **Security Best Practices**

1. **Never commit credentials**
   - Use environment variables
   - Use AWS IAM roles
   - Use Pulumi secrets

2. **Limit security group rules**
   - Restrict SSH to your IP
   - Use least privilege
   - Document all rules

3. **Enable logging**
   - VPC Flow Logs
   - CloudTrail
   - CloudWatch

4. **Use MFA**
   - Enable MFA on AWS account
   - Use temporary credentials

---

## 📚 **Next Steps**

1. ✅ Deploy basic VPC
2. ✅ Run tests
3. ✅ Verify connectivity
4. 🚀 Add on-prem configuration
5. 🚀 Establish VPN tunnels
6. 🚀 Configure BGP
7. 🚀 Test end-to-end connectivity

---

## 💡 **Tips**

- Start with `dev` stack
- Use `pulumi preview` before `pulumi up`
- Tag all resources
- Document changes
- Version control everything

---

## 🆘 **Getting Help**

- **Pulumi Docs**: https://www.pulumi.com/docs/
- **AWS VPC Docs**: https://docs.aws.amazon.com/vpc/
- **Project Issues**: https://github.com/yourusername/Cloud_Networking_Lab/issues
- **Pulumi Community**: https://slack.pulumi.com/

---

**Happy Cloud Networking!** ☁️🚀
