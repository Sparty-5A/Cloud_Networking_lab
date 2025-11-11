# Getting Started - Cloud Networking Lab

**Welcome!** This guide will walk you through your first deployment.

---

## 🎯 **What You'll Build**

In this guide, you'll create:
- ✅ AWS VPC with CIDR 10.0.0.0/16
- ✅ Two public subnets across different availability zones
- ✅ Internet Gateway for public internet access
- ✅ Route tables configured for internet routing
- ✅ Security groups for network access control

**Time to complete:** ~15 minutes

**Estimated cost:** Free tier eligible (~$0/month)

---

## 📋 **Prerequisites Checklist**

Before starting, ensure you have:

- [ ] Python 3.13+ installed
- [ ] AWS account created
- [ ] AWS credentials configured
- [ ] Pulumi CLI installed
- [ ] Git installed (optional, for cloning)

Need help? See [Setup Guide](setup_guide.md) for detailed installation instructions.

---

## 🚀 **Step 1: Install Dependencies**

```bash
# Clone or navigate to project
cd Cloud_Networking_Lab

# Install dependencies with uv
uv sync

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

**Verify installation:**
```bash
pulumi version
python --version
uv --version
```

---

## 🔐 **Step 2: Configure AWS**

### **Option A: AWS CLI (Recommended)**

```bash
aws configure
```

Enter:
- AWS Access Key ID
- AWS Secret Access Key
- Default region: `us-east-1`
- Default output format: `json`

### **Option B: Environment Variables**

```bash
export AWS_ACCESS_KEY_ID="your-key-id"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"
```

**Verify:**
```bash
aws sts get-caller-identity
```

---

## 🎨 **Step 3: Choose Your Deployment Method**

### **Method 1: Pulumi CLI (Recommended for Beginners)**

Simple and interactive - perfect for learning!

### **Method 2: Intent-Based (Advanced)**

Use YAML configuration files - more scalable!

---

## 📦 **Method 1: Pulumi CLI Deployment**

### **1. Initialize Stack**

```bash
cd pulumi
pulumi login  # Use Pulumi Cloud (free) or --local
pulumi stack init dev
```

### **2. Configure Settings**

```bash
# Set AWS region
pulumi config set aws:region us-east-1

# Set VPC CIDR
pulumi config set vpc_cidr 10.0.0.0/16

# Disable VPN (we'll add it later)
pulumi config set enable_vpn false
```

### **3. Preview Changes**

```bash
pulumi preview
```

You'll see:
```
Previewing update (dev)

     Type                      Name                    Plan
 +   pulumi:pulumi:Stack       cloud-lab-dev           create
 +   ├─ aws:ec2:Vpc            cloud-lab-vpc           create
 +   ├─ aws:ec2:Subnet         cloud-lab-public-a      create
 +   ├─ aws:ec2:Subnet         cloud-lab-public-b      create
 +   ├─ aws:ec2:InternetGateway cloud-lab-igw          create
 +   ├─ aws:ec2:RouteTable     cloud-lab-public-rt     create
 +   └─ aws:ec2:SecurityGroup  cloud-lab-default-sg    create

Resources:
    + 7 to create
```

### **4. Deploy!**

```bash
pulumi up
```

Type `yes` when prompted.

**Wait 1-2 minutes for deployment...**

### **5. View Results**

```bash
pulumi stack output
```

Output:
```
Current stack outputs (8):
    OUTPUT                     VALUE
    deployment_message         ✓ VPC deployed successfully in dev...
    internet_gateway_id        igw-0abcdef1234567890
    public_subnet_a_az         us-east-1a
    public_subnet_a_cidr       10.0.1.0/24
    public_subnet_a_id         subnet-0abcdef1234567890
    public_subnet_b_az         us-east-1b
    public_subnet_b_cidr       10.0.2.0/24
    vpc_cidr                   10.0.0.0/16
    vpc_id                     vpc-0abcdef1234567890
```

**🎉 Success! Your VPC is live!**

---

## 📝 **Method 2: Intent-Based Deployment**

### **1. Create Intent File**

```bash
cp examples/basic_vpc.yaml my-network.yaml
```

Edit `my-network.yaml`:
```yaml
network:
  project_name: "my-first-lab"
  environment: "dev"
  region: "us-east-1"
  
  vpc:
    cidr_block: "10.0.0.0/16"
    subnets:
      - name: "public-a"
        cidr_block: "10.0.1.0/24"
        availability_zone: "us-east-1a"
        public: true
```

### **2. Validate Intent**

```bash
python -c "
from models.aws_intent import AWSNetworkIntent
import yaml

with open('my-network.yaml') as f:
    config = yaml.safe_load(f)

intent = AWSNetworkIntent(**config['network'])
print('✓ Intent valid!')
print(f'  VPC CIDR: {intent.vpc.cidr_block}')
print(f'  Subnets: {len(intent.vpc.subnets)}')
"
```

### **3. Deploy**

```bash
cd pulumi
pulumi up --config-file ../my-network.yaml
```

---

## ✅ **Step 4: Verify Deployment**

### **Check AWS Console**

1. Go to https://console.aws.amazon.com/vpc/
2. Select your region (us-east-1)
3. Click "Your VPCs" - you should see your new VPC!
4. Click "Subnets" - you should see 2 subnets
5. Click "Internet Gateways" - you should see your IGW

### **Run Tests**

```bash
cd ../tests
pytest unit/test_aws_intent.py -v
```

Should see:
```
✓ 20+ tests passed
```

### **Verify Connectivity Script**

```bash
cd ../scripts
python verify_connectivity.py
```

Output:
```
🔍 Checking VPN connections in us-east-1...
❌ No VPN connections found (expected - VPN not enabled)

✓ VPC infrastructure verified
```

---

## 🎓 **What You Learned**

Congratulations! You just:

✅ Deployed infrastructure as code with Pulumi  
✅ Created a production-ready VPC  
✅ Configured multi-AZ subnets  
✅ Set up internet connectivity  
✅ Used intent-based configuration  
✅ Validated with tests  

---

## 🚀 **Next Steps**

### **Easy Next Steps:**

1. **Add another subnet**
   ```bash
   pulumi config set subnet_count 4
   pulumi up
   ```

2. **Enable VPC Flow Logs**
   ```bash
   pulumi config set enable_flow_logs true
   pulumi up
   ```

3. **Run all tests**
   ```bash
   cd tests
   pytest -v --cov
   ```

### **Advanced Next Steps:**

4. **Add VPN Connection**
   - Edit `examples/vpc_with_vpn.yaml`
   - Replace `ip_address` with your public IP
   - Deploy: `pulumi up`

5. **Configure On-Prem Side**
   - Set up Ubuntu VM or router
   - Configure IPSec
   - Establish BGP peering

6. **Monitor with CloudWatch**
   - Enable Flow Logs
   - Create dashboards
   - Set up alarms

---

## 🧹 **Cleanup**

When you're done experimenting:

```bash
cd pulumi
pulumi destroy
```

Type `yes` to confirm.

**This will delete:**
- VPC
- Subnets
- Internet Gateway
- Route tables
- Security groups

**Note:** This operation is irreversible!

---

## 💰 **Cost Management**

### **Current Setup Costs:**

| Resource | Cost |
|----------|------|
| VPC | Free |
| Subnets | Free |
| Internet Gateway | Free |
| Route Tables | Free |

**Total: $0/month** 🎉

### **If You Add:**

| Resource | Estimated Cost |
|----------|---------------|
| VPN Gateway | ~$36/month |
| NAT Gateway | ~$32/month + data |
| EC2 instance | ~$8/month (t2.micro) |

**💡 Tip:** Always run `pulumi destroy` when not using resources!

---

## 🐛 **Troubleshooting**

### **"Insufficient permissions"**

Your AWS user needs these permissions:
- `AmazonVPCFullAccess`
- `AmazonEC2FullAccess`

**Fix:**
1. Go to AWS IAM Console
2. Find your user
3. Attach policies above

### **"Stack already exists"**

```bash
pulumi stack select dev
# or
pulumi stack rm dev  # Delete and start over
```

### **"Resource already exists"**

```bash
# Import existing resource
pulumi import aws:ec2/vpc:Vpc my-vpc vpc-12345678
```

---

## 📚 **Learn More**

- **[Setup Guide](setup_guide.md)** - Detailed installation
- **[Architecture Overview](architecture.md)** - System design
- **[Networking Concepts](networking_concepts.md)** - AWS fundamentals
- **[Pulumi Docs](https://www.pulumi.com/docs/)** - Pulumi reference

---

## 🆘 **Need Help?**

- 💬 **Slack:** [Pulumi Community](https://slack.pulumi.com/)
- 📖 **Docs:** [AWS VPC Guide](https://docs.aws.amazon.com/vpc/)
- 🐛 **Issues:** [GitHub Issues](https://github.com/yourusername/Cloud_Networking_Lab/issues)

---

**Ready for more? Let's add a VPN connection next!** 🚀

See: [VPN Setup Guide](vpn_setup.md) *(coming soon)*
