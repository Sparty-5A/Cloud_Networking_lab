# Troubleshooting Guide

Common issues and solutions for the Cloud Networking Lab project, covering Pulumi, AWS, Python, and networking problems.

---

## 📋 **Quick Troubleshooting Checklist**

Before diving into specific issues, check these common culprits:

```
✓ Virtual environment activated? (source .venv/bin/activate)
✓ AWS credentials configured? (aws sts get-caller-identity)
✓ Pulumi stack selected? (pulumi stack select dev)
✓ Configuration set? (pulumi config)
✓ Dependencies installed? (uv sync --extra dev)
```

---

## 🔧 **Pulumi Issues**

### **Issue: "No module named 'pulumi'"**

**Symptoms:**
```bash
$ pulumi up
ModuleNotFoundError: No module named 'pulumi'
```

**Cause:** Virtual environment not activated or Pulumi not installed

**Solution:**
```bash
cd ~/Cloud_Networking_Lab
source .venv/bin/activate  # Activate venv FIRST!
cd pulumi
pulumi up
```

**Verify:**
```bash
which python  # Should show: ~/Cloud_Networking_Lab/.venv/bin/python
pip list | grep pulumi  # Should show pulumi packages
```

---

### **Issue: "error: no Pulumi.yaml project file found"**

**Symptoms:**
```bash
$ pulumi up
error: no Pulumi.yaml project file found
```

**Cause:** Running `pulumi` command from wrong directory

**Solution:**
```bash
cd ~/Cloud_Networking_Lab/pulumi  # Must be IN the pulumi/ directory!
pulumi up
```

**Project structure:**
```
Cloud_Networking_Lab/
├── pyproject.toml        ← Root
└── pulumi/
    ├── Pulumi.yaml       ← Pulumi project file (must be here!)
    ├── __main__.py
    └── ...
```

---

### **Issue: "passphrase required to unlock secret"**

**Symptoms:**
```bash
$ pulumi up
Enter your passphrase to unlock config/secrets:
```

**Cause:** Pulumi state is encrypted with passphrase

**Solution 1:** Enter passphrase each time

**Solution 2:** Set environment variable
```bash
export PULUMI_CONFIG_PASSPHRASE="your-passphrase"
# Or add to ~/.bashrc:
echo 'export PULUMI_CONFIG_PASSPHRASE="your-passphrase"' >> ~/.bashrc
source ~/.bashrc
```

**Security Note:** Only use environment variable on personal/dev machines

---

### **Issue: "error: resource already exists"**

**Symptoms:**
```bash
$ pulumi up
error: resource 'aws:ec2/vpc:Vpc' already exists
```

**Cause:** AWS resource exists but Pulumi doesn't know about it

**Solutions:**

**Option 1:** Import existing resource
```bash
pulumi import aws:ec2/vpc:Vpc my-vpc vpc-abc123
```

**Option 2:** Delete AWS resource manually and redeploy
```bash
# Delete from AWS Console first
pulumi refresh  # Sync state
pulumi up       # Redeploy
```

**Option 3:** Start fresh (if safe)
```bash
# Manually delete all AWS resources
pulumi refresh
pulumi stack rm dev
pulumi stack init dev
pulumi up
```

---

### **Issue: "unable to find stack 'dev'"**

**Symptoms:**
```bash
$ pulumi up
error: unable to find stack 'dev'
```

**Cause:** Stack doesn't exist or was deleted

**Solution:**
```bash
# List existing stacks
pulumi stack ls

# If none exist, create one
pulumi stack init dev

# Configure it
pulumi config set aws:region us-east-1
pulumi config set vpc_cidr 10.0.0.0/16
pulumi config set enable_vpn false

# Deploy
pulumi up
```

---

### **Issue: "conflict: Another update is currently in progress"**

**Symptoms:**
```bash
$ pulumi up
error: [409] Conflict: Another update is currently in progress.
```

**Cause:** Previous update didn't complete or crashed

**Solution:**
```bash
# Cancel the stuck update
pulumi cancel

# Verify it's gone
pulumi stack

# Try again
pulumi up
```

**If that doesn't work:**
```bash
# Nuclear option: force unlock
rm -rf ~/.pulumi/stacks/dev.json.lock
pulumi refresh
```

---

## ☁️ **AWS Issues**

### **Issue: "InvalidClientTokenId: The security token included in the request is invalid"**

**Symptoms:**
```bash
$ pulumi up
error: InvalidClientTokenId: The security token included in the request is invalid
```

**Cause:** AWS credentials not configured or expired

**Solution:**
```bash
# Configure AWS credentials
aws configure
# Enter:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Region: us-east-1
# - Output: json

# Verify
aws sts get-caller-identity
```

**Expected output:**
```json
{
    "UserId": "AIDAI...",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/myuser"
}
```

---

### **Issue: "UnauthorizedOperation: You are not authorized to perform this operation"**

**Symptoms:**
```bash
$ pulumi up
error: UnauthorizedOperation: You are not authorized to perform this operation
```

**Cause:** IAM user lacks required permissions

**Solution:**

**Check current permissions:**
```bash
aws iam get-user
aws iam list-attached-user-policies --user-name YOUR_USERNAME
```

**Required policies for this project:**
- `AmazonVPCFullAccess`
- `AmazonEC2FullAccess`
- `IAMReadOnlyAccess` (for flow logs)
- `CloudWatchLogsFullAccess` (for flow logs)

**Add policy (if you're admin):**
```bash
aws iam attach-user-policy \
  --user-name YOUR_USERNAME \
  --policy-arn arn:aws:iam::aws:policy/AmazonVPCFullAccess
```

**If not admin:** Ask your AWS administrator to grant permissions

---

### **Issue: "InvalidParameterValue: Value (10.0.0.0/15) for parameter cidrBlock is invalid"**

**Symptoms:**
```bash
$ pulumi up
error: InvalidParameterValue: Value (10.0.0.0/15) for parameter cidrBlock is invalid. 
VPC CIDR block must be between /16 and /28
```

**Cause:** Invalid CIDR block for VPC

**Solution:**
```bash
# VPC must be /16 to /28
pulumi config set vpc_cidr 10.0.0.0/16  # ✅ Valid
# Not /15, /8, etc.

pulumi up
```

**Valid CIDR ranges:**
```
10.0.0.0/16   ✅ 65,536 IPs
10.0.0.0/17   ✅ 32,768 IPs
10.0.0.0/24   ✅ 256 IPs
10.0.0.0/28   ✅ 16 IPs (minimum)
10.0.0.0/15   ❌ Too large!
```

---

### **Issue: "The maximum number of VPCs has been reached"**

**Symptoms:**
```bash
$ pulumi up
error: VpcLimitExceeded: The maximum number of VPCs has been reached
```

**Cause:** AWS has a default limit of 5 VPCs per region

**Solution:**

**Option 1:** Delete unused VPCs
```bash
# List VPCs
aws ec2 describe-vpcs --query 'Vpcs[*].[VpcId,CidrBlock,Tags]'

# Delete via AWS Console or:
aws ec2 delete-vpc --vpc-id vpc-xxxxx
```

**Option 2:** Request limit increase
- Go to AWS Service Quotas console
- Request increase for "VPCs per Region"
- Usually approved quickly

---

### **Issue: "Resource has a dependent object"**

**Symptoms:**
```bash
$ pulumi destroy
error: DependencyViolation: The vpc 'vpc-xxx' has dependencies and cannot be deleted
```

**Cause:** VPC has resources attached (subnets, IGW, etc.)

**Solution:**

**Manual cleanup order:**
```bash
1. Delete EC2 instances
2. Delete NAT Gateways (wait 5 min)
3. Delete subnets
4. Detach & delete Internet Gateway
5. Delete route tables (except main)
6. Delete security groups (except default)
7. Delete VPC
```

**Or use Pulumi:**
```bash
# This should handle dependencies automatically
pulumi destroy --yes

# If it fails, try:
pulumi refresh
pulumi destroy --yes
```

---

## 🐍 **Python Issues**

### **Issue: "ImportError: cannot import name 'X' from 'models'"**

**Symptoms:**
```bash
$ pulumi up
ImportError: cannot import name 'VPCIntent' from 'models'
```

**Cause:** Incorrect import path or missing `__init__.py`

**Solution:**

**Check file structure:**
```
models/
├── __init__.py         ← Must exist!
└── aws_intent.py       ← Contains VPCIntent
```

**Correct import in `__main__.py`:**
```python
# If running from pulumi/ directory:
import sys
sys.path.insert(0, '..')  # Add parent directory

from models.aws_intent import VPCIntent  # ✅ Correct
```

**Verify:**
```bash
cd ~/Cloud_Networking_Lab
source .venv/bin/activate
python -c "from models.aws_intent import VPCIntent; print('OK')"
```

---

### **Issue: "ModuleNotFoundError: No module named 'pydantic'"**

**Symptoms:**
```bash
$ pytest
ModuleNotFoundError: No module named 'pydantic'
```

**Cause:** Dependencies not installed

**Solution:**
```bash
cd ~/Cloud_Networking_Lab
source .venv/bin/activate
uv sync --extra dev  # Install all dependencies

# Verify
pip list | grep pydantic
```

---

### **Issue: "TypeError: 'Output' object is not callable"**

**Symptoms:**
```bash
$ pulumi up
TypeError: 'Output' object is not callable
```

**Cause:** Trying to use Pulumi Output incorrectly

**Common mistakes:**

**❌ Wrong:**
```python
# Trying to call Output
vpc_id = vpc.id()  # ❌ Output is not callable

# Using Output in string directly
print(f"VPC ID: {vpc.id}")  # ❌ Shows <pulumi.Output object>
```

**✅ Correct:**
```python
# Export Output
pulumi.export("vpc_id", vpc.id)  # ✅

# Use .apply() for transformations
vpc.id.apply(lambda id: print(f"VPC ID: {id}"))  # ✅

# Combine multiple Outputs
pulumi.Output.all(vpc.id, subnet.id).apply(
    lambda args: {"vpc": args[0], "subnet": args[1]}
)  # ✅
```

---

## 🌐 **Networking Issues**

### **Issue: "Cannot connect to EC2 instance"**

**Symptoms:**
```bash
$ ssh ec2-user@54.123.45.67
ssh: connect to host 54.123.45.67 port 22: Connection timed out
```

**Debugging steps:**

**1. Check instance is running:**
```bash
aws ec2 describe-instances --instance-ids i-xxxxx \
  --query 'Reservations[0].Instances[0].State.Name'
# Should be "running"
```

**2. Check instance has public IP:**
```bash
aws ec2 describe-instances --instance-ids i-xxxxx \
  --query 'Reservations[0].Instances[0].PublicIpAddress'
# Should show an IP, not "null"
```

**3. Check security group allows SSH:**
```bash
aws ec2 describe-security-groups --group-ids sg-xxxxx \
  --query 'SecurityGroups[0].IpPermissions'

# Should have:
# {
#   "IpProtocol": "tcp",
#   "FromPort": 22,
#   "ToPort": 22,
#   "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
# }
```

**4. Check route table has IGW route:**
```bash
aws ec2 describe-route-tables --route-table-ids rtb-xxxxx \
  --query 'RouteTables[0].Routes'

# Should have:
# {
#   "DestinationCidrBlock": "0.0.0.0/0",
#   "GatewayId": "igw-xxxxx"
# }
```

**5. Check NACL allows traffic:**
```bash
# Usually NACLs are permissive by default
# Only check if you customized them
```

**Common fixes:**
```bash
# Fix: Add SSH rule to security group
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0

# Fix: Associate IGW route
aws ec2 create-route \
  --route-table-id rtb-xxxxx \
  --destination-cidr-block 0.0.0.0/0 \
  --gateway-id igw-xxxxx
```

---

### **Issue: "Instance can't reach internet"**

**Symptoms:**
```bash
# From inside instance:
$ ping 8.8.8.8
Network is unreachable
```

**Debugging steps:**

**1. Check subnet type:**
```bash
# Is instance in public or private subnet?
aws ec2 describe-subnets --subnet-ids subnet-xxxxx

# Public subnet needs:
# - Route to IGW (0.0.0.0/0 → igw-xxxxx)
# - Auto-assign public IP enabled
```

**2. Check route table:**
```bash
aws ec2 describe-route-tables \
  --filters "Name=association.subnet-id,Values=subnet-xxxxx"

# Must have IGW route:
# 0.0.0.0/0 → igw-xxxxx (for public subnet)
# OR
# 0.0.0.0/0 → nat-xxxxx (for private subnet)
```

**3. Check security group egress:**
```bash
aws ec2 describe-security-groups --group-ids sg-xxxxx \
  --query 'SecurityGroups[0].IpPermissionsEgress'

# Should allow all outbound:
# {
#   "IpProtocol": "-1",
#   "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
# }
```

**Common fix:**
```python
# In Pulumi code, ensure subnet has IGW route:
public_route = aws.ec2.Route(
    "public-route",
    route_table_id=route_table.id,
    destination_cidr_block="0.0.0.0/0",
    gateway_id=igw.id  # ← Must point to IGW!
)
```

---

### **Issue: "VPN tunnel won't establish"**

**Symptoms:**
```bash
# VPN tunnel shows "DOWN" in AWS Console
```

**Debugging steps:**

**1. Check customer gateway IP:**
```bash
# Your public IP must be correct
curl ifconfig.me  # Get your current public IP

# Update if changed:
pulumi config set customer_gateway_ip YOUR_PUBLIC_IP
pulumi up
```

**2. Check on-prem IPSec configuration:**
```bash
# For StrongSwan:
sudo ipsec status
sudo ipsec statusall

# Look for:
# - IKE SA established
# - IPSec SA installed
```

**3. Check AWS VPN configuration:**
```bash
# Download VPN config from AWS Console
# Compare with your on-prem settings:
# - Pre-shared keys match?
# - Phase 1/2 parameters match?
# - Inside tunnel IPs correct?
```

**4. Check routing:**
```bash
# On-prem should have route to AWS CIDR
ip route | grep 10.0.0.0

# AWS should have VPN route propagation enabled
aws ec2 describe-route-tables --route-table-ids rtb-xxxxx
# Look for routes learned via VPN
```

**Common issues:**
```
❌ NAT in front of customer gateway
   → Use public IP before NAT

❌ Firewall blocking UDP 500/4500
   → Allow IPSec traffic

❌ PSK mismatch
   → Re-download config, verify PSK

❌ MTU issues
   → Set MSS clamping: iptables -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu
```

---

## 🧪 **Testing Issues**

### **Issue: "pytest: command not found"**

**Symptoms:**
```bash
$ pytest
bash: pytest: command not found
```

**Cause:** Virtual environment not activated or pytest not installed

**Solution:**
```bash
cd ~/Cloud_Networking_Lab
source .venv/bin/activate
uv sync --extra dev  # Install dev dependencies
pytest -v
```

---

### **Issue: "ModuleNotFoundError: No module named 'tests'"**

**Symptoms:**
```bash
$ pytest
ImportError: No module named 'tests'
```

**Cause:** Running pytest from wrong directory

**Solution:**
```bash
# Run from project root
cd ~/Cloud_Networking_Lab
source .venv/bin/activate
pytest -v

# NOT from pulumi/ directory!
```

---

### **Issue: "Fixture 'mock_aws_config' not found"**

**Symptoms:**
```bash
$ pytest
fixture 'mock_aws_config' not found
```

**Cause:** Missing or incorrect `conftest.py`

**Solution:**

**Check conftest.py exists:**
```bash
ls tests/conftest.py  # Should exist
```

**Check fixture is defined:**
```python
# In tests/conftest.py:
@pytest.fixture
def mock_aws_config():
    # ... fixture code
    return config
```

---

## 💰 **Cost Issues**

### **Issue: "Unexpected AWS charges"**

**Symptoms:**
- AWS bill higher than expected
- Resources not cleaned up

**Prevention:**
```bash
# Always destroy when done
pulumi destroy --yes

# Verify resources deleted
aws ec2 describe-vpcs
aws ec2 describe-vpn-gateways
aws ec2 describe-nat-gateways
```

**Cost culprits:**
```
💰 VPN Gateway:    ~$36/month  (always running)
💰 NAT Gateway:    ~$32/month  (always running)
💰 EC2 instances:  ~$8/month   (t2.micro outside free tier)
💰 Data transfer:  $0.09/GB    (outbound)

Free tier:
✅ VPC, subnets, IGW, route tables, security groups: $0
✅ t2.micro EC2:   750 hours/month free (first year)
```

**Clean up checklist:**
```bash
# 1. Destroy Pulumi stack
cd ~/Cloud_Networking_Lab/pulumi
pulumi destroy

# 2. Verify in AWS Console
# - EC2 → Instances: None
# - VPC → VPCs: None (or just default)
# - VPC → NAT Gateways: None
# - VPC → VPN Gateways: None

# 3. Check billing
# AWS Console → Billing → Cost Explorer
# Look for unexpected charges
```

---

## 🔍 **Debugging Techniques**

### **Enable Verbose Logging**

**Pulumi:**
```bash
# Show detailed logs
pulumi up --logtostderr -v=9

# Show only errors
pulumi up --suppress-outputs
```

**AWS CLI:**
```bash
# Enable debug mode
aws ec2 describe-vpcs --debug
```

### **Inspect Pulumi State**

```bash
# View current stack state
pulumi stack --show-urns

# Export state
pulumi stack export > state.json
cat state.json | jq .

# View specific resource
pulumi stack export | jq '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc")'
```

### **Check AWS Resources**

```bash
# List all VPCs
aws ec2 describe-vpcs --output table

# List all subnets in VPC
aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=vpc-xxxxx" \
  --output table

# List security groups
aws ec2 describe-security-groups \
  --filters "Name=vpc-id,Values=vpc-xxxxx" \
  --output table

# Check route tables
aws ec2 describe-route-tables \
  --filters "Name=vpc-id,Values=vpc-xxxxx" \
  --output table
```

### **Network Connectivity Testing**

**From your local machine:**
```bash
# Test public IP reachable
ping 54.123.45.67

# Test SSH port open
nc -zv 54.123.45.67 22
# Or:
telnet 54.123.45.67 22

# Trace route
traceroute 54.123.45.67
```

**From EC2 instance:**
```bash
# Test internet connectivity
ping 8.8.8.8

# Test DNS
nslookup google.com

# Test specific port
curl -I https://www.google.com

# Check routes
ip route show

# Check interfaces
ip addr show
```

---

## 🆘 **When You're Really Stuck**

### **Nuclear Options** (Use with caution!)

**1. Completely reset Pulumi state:**
```bash
cd ~/Cloud_Networking_Lab/pulumi
pulumi stack rm dev --yes --force
pulumi stack init dev
# Reconfigure from scratch
```

**2. Manually clean all AWS resources:**
```bash
# Delete VPC and all contents from AWS Console
# Then start fresh with Pulumi
```

**3. Recreate virtual environment:**
```bash
cd ~/Cloud_Networking_Lab
rm -rf .venv
uv venv
source .venv/bin/activate
uv sync --extra dev
```

### **Get Help**

**Resources:**
- **Pulumi Docs:** https://www.pulumi.com/docs/
- **AWS Support:** https://support.aws.amazon.com/
- **Pulumi Slack:** https://pulumi-community.slack.com/
- **Stack Overflow:** Tag with `pulumi` and `amazon-vpc`

**Information to include when asking for help:**
```
1. Exact error message (full traceback)
2. Output of: pulumi version
3. Output of: aws --version
4. Output of: python --version
5. What you were trying to do
6. What you've already tried
7. Relevant code snippets
```

---

## 📚 **Prevention Tips**

**Best practices to avoid issues:**

✅ **Always activate venv:**
```bash
cd ~/Cloud_Networking_Lab
source .venv/bin/activate  # First thing!
```

✅ **Use pulumi preview:**
```bash
pulumi preview  # Check changes before applying
```

✅ **Start small:**
```bash
# Deploy basic VPC first
# Add complexity incrementally
# Test after each change
```

✅ **Version control:**
```bash
git add .
git commit -m "Working state"
# Easy to revert if something breaks
```

✅ **Document config:**
```bash
# Keep a notes.md with your config values
# Especially: IPs, CIDRs, PSKs
```

✅ **Clean up regularly:**
```bash
pulumi destroy  # When done testing
# Avoid unexpected charges
```

---

## 🎓 **Common Error Patterns**

**Pattern 1: "It worked yesterday"**
```
Likely causes:
- AWS credentials expired
- Public IP changed (VPN)
- Free tier limits reached
- Configuration drift

Fix: Run pulumi refresh, check AWS Console
```

**Pattern 2: "Works in AWS Console but not in code"**
```
Likely causes:
- Pulumi state out of sync
- Resource manually modified
- Naming conflicts

Fix: Run pulumi refresh or pulumi import
```

**Pattern 3: "Tests pass but deployment fails"**
```
Likely causes:
- Mocking in tests doesn't match AWS reality
- AWS API validation stricter than model validation
- Resource dependencies not properly defined

Fix: Check AWS error, adjust code, re-test
```

---

**Last Updated:** October 30, 2025  
**Need more help?** Check `docs/` for other guides or open an issue on GitHub.
