# Pulumi Python Quick Reference

Complete guide for making infrastructure changes with Pulumi and AWS.

---

## 📚 **Documentation Links**

### **Main Resources:**
- **Pulumi AWS Registry:** https://www.pulumi.com/registry/packages/aws/
- **Pulumi Python Guide:** https://www.pulumi.com/docs/languages-sdks/python/
- **AWS Resource List:** https://www.pulumi.com/registry/packages/aws/api-docs/

### **Common Resources:**
| Resource | Documentation URL |
|----------|------------------|
| VPC | https://www.pulumi.com/registry/packages/aws/api-docs/ec2/vpc/ |
| Subnet | https://www.pulumi.com/registry/packages/aws/api-docs/ec2/subnet/ |
| Security Group | https://www.pulumi.com/registry/packages/aws/api-docs/ec2/securitygroup/ |
| Route Table | https://www.pulumi.com/registry/packages/aws/api-docs/ec2/routetable/ |
| Route | https://www.pulumi.com/registry/packages/aws/api-docs/ec2/route/ |
| EC2 Instance | https://www.pulumi.com/registry/packages/aws/api-docs/ec2/instance/ |
| Internet Gateway | https://www.pulumi.com/registry/packages/aws/api-docs/ec2/internetgateway/ |
| NAT Gateway | https://www.pulumi.com/registry/packages/aws/api-docs/ec2/natgateway/ |
| VPN Gateway | https://www.pulumi.com/registry/packages/aws/api-docs/ec2/vpngateway/ |
| Elastic IP | https://www.pulumi.com/registry/packages/aws/api-docs/ec2/eip/ |
| Load Balancer | https://www.pulumi.com/registry/packages/aws/api-docs/lb/loadbalancer/ |

---

## 🔍 **How to Find Documentation**

### **Method 1: Google Search**
```
Pattern: "pulumi aws [resource] python"

Examples:
- "pulumi aws security group python"
- "pulumi aws route table python"
- "pulumi aws nat gateway python"
```

### **Method 2: Navigate Registry**
```
1. Go to https://www.pulumi.com/registry/packages/aws/
2. Click "API Docs"
3. Use search box (e.g., "Security Group")
4. Click on the resource
5. Ensure "Python" tab is selected
```

### **Method 3: From AWS Console**
```
1. Find resource in AWS Console
2. Note the service (EC2, VPC, etc.)
3. Google: "pulumi aws [service-name] [resource-name] python"
```

---

## 📖 **Reading Documentation Pages**

Every resource page has these sections:

### **1. Example Usage**
Shows complete working code you can copy/modify

### **2. Create [Resource]**
Shows constructor signature and all parameters

### **3. Inputs**
Lists all properties you can set:
- **Required** properties (must provide)
- **Optional** properties (can omit)
- **Type** of each property

### **4. Outputs**
Lists properties you can read after creation:
- Usually includes `id`, `arn`
- Resource-specific outputs

### **5. Import**
Shows how to import existing resources (if needed)

---

## 🎯 **Common Patterns**

### **Basic Resource Creation**
```python
import pulumi_aws as aws

resource = aws.service.ResourceType("name",
    required_property="value",
    optional_property="value",
    tags={"Name": "my-resource"}
)
```

### **Referencing Other Resources**
```python
# Create VPC
vpc = aws.ec2.Vpc("my-vpc",
    cidr_block="10.0.0.0/16"
)

# Reference VPC in Subnet
subnet = aws.ec2.Subnet("my-subnet",
    vpc_id=vpc.id,  # ← References VPC's ID
    cidr_block="10.0.1.0/24"
)
```

### **Using Configuration**
```python
config = pulumi.Config()

# Get with default
vpc_cidr = config.get("vpc_cidr") or "10.0.0.0/16"

# Get required (fails if not set)
vpc_cidr = config.require("vpc_cidr")

# Get boolean
enable_feature = config.get_bool("enable_feature") or False

# Get integer
port = config.get_int("port") or 80
```

### **Conditional Resources**
```python
enable_vpn = config.get_bool("enable_vpn") or False

if enable_vpn:
    vpn_gateway = aws.ec2.VpnGateway("vpn-gw",
        vpc_id=vpc.id
    )
```

### **Lists of Sub-Resources**
```python
# Security group with multiple rules
sg = aws.ec2.SecurityGroup("my-sg",
    vpc_id=vpc.id,
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"]
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=80,
            to_port=80,
            cidr_blocks=["0.0.0.0/0"]
        ),
    ]
)
```

### **Exporting Outputs**
```python
# Export simple value
pulumi.export("vpc_id", vpc.id)

# Export with formatting
pulumi.export("web_url", instance.public_ip.apply(
    lambda ip: f"http://{ip}"
))

# Export multiple values
pulumi.export("config", {
    "vpc_id": vpc.id,
    "subnet_id": subnet.id
})
```

---

## 🔧 **Making Changes Workflow**

### **Step-by-Step:**

```bash
# 1. Find documentation for what you want to change
Google: "pulumi aws [resource] python"

# 2. Edit the code
cd ~/Cloud_Networking_Lab
vim pulumi/__main__.py
# Make your changes

# 3. Activate virtual environment
source .venv/bin/activate
cd pulumi

# 4. Preview changes (ALWAYS do this first!)
pulumi preview

# 5. Review preview output
# Check:
# - What will be created (+)
# - What will be updated (~)
# - What will be replaced (replace)
# - What will be deleted (-)

# 6. Apply if preview looks correct
pulumi up

# 7. Type "yes" to confirm

# 8. Verify changes
pulumi stack output
# or check AWS Console

# 9. Commit to git
git add pulumi/__main__.py
git commit -m "Description of change"
```

---

## 💡 **Common Changes**

### **1. Add Security Group Rule**

**File:** `pulumi/__main__.py`

**Find security group, add to ingress list:**
```python
aws.ec2.SecurityGroupIngressArgs(
    protocol="tcp",
    from_port=8080,
    to_port=8080,
    cidr_blocks=["10.0.0.0/16"],
    description="App server traffic"
),
```

**Deploy:**
```bash
pulumi up
```

---

### **2. Add New Subnet**

**File:** `pulumi/__main__.py`

**Add after existing subnets:**
```python
public_subnet_c = aws.ec2.Subnet(
    f"{project_name}-public-c",
    vpc_id=vpc.id,
    cidr_block="10.0.3.0/24",
    availability_zone=f"{aws_region}c",
    map_public_ip_on_launch=True,
    tags={**common_tags, "Name": f"{project_name}-public-c-{stack_name}"}
)

# Associate with route table
public_rt_assoc_c = aws.ec2.RouteTableAssociation(
    f"{project_name}-public-rt-assoc-c",
    subnet_id=public_subnet_c.id,
    route_table_id=public_route_table.id
)

# Export
pulumi.export("public_subnet_c_id", public_subnet_c.id)
```

---

### **3. Add Static Route**

**File:** `pulumi/__main__.py`

**Add after route table creation:**
```python
custom_route = aws.ec2.Route(
    "custom-route",
    route_table_id=route_table.id,
    destination_cidr_block="192.168.0.0/16",
    gateway_id=vpn_gateway.id  # or nat_gateway.id
)
```

---

### **4. Change Instance Type**

**File:** `pulumi/__main__.py`

**Find EC2 instance, change:**
```python
web_server = aws.ec2.Instance(
    f"{project_name}-web-server",
    instance_type="t3.small",  # ← Changed from t3.micro
    # ... rest stays same
)
```

**Note:** This will REPLACE the instance (delete + recreate)

---

### **5. Add Second Web Server**

**File:** `pulumi/__main__.py`

**Add after first web server:**
```python
web_server_b = aws.ec2.Instance(
    f"{project_name}-web-server-b",
    instance_type="t3.micro",
    ami=ami.id,
    subnet_id=public_subnet_b.id,  # ← Different subnet!
    vpc_security_group_ids=[default_sg.id],
    user_data=user_data,
    associate_public_ip_address=True,
    tags={**common_tags, "Name": f"{project_name}-web-server-b-{stack_name}"}
)

pulumi.export("web_server_b_public_ip", web_server_b.public_ip)
```

---

### **6. Add NAT Gateway**

**File:** `pulumi/__main__.py`

**Add after public subnet:**
```python
# Elastic IP for NAT
nat_eip = aws.ec2.Eip(
    f"{project_name}-nat-eip",
    vpc=True,
    tags={**common_tags, "Name": f"{project_name}-nat-eip-{stack_name}"}
)

# NAT Gateway (in public subnet!)
nat_gateway = aws.ec2.NatGateway(
    f"{project_name}-nat-gw",
    subnet_id=public_subnet_a.id,
    allocation_id=nat_eip.id,
    tags={**common_tags, "Name": f"{project_name}-nat-gw-{stack_name}"}
)
```

**Cost:** ~$32/month (not free!)

---

### **7. Restrict SSH to Your IP**

**File:** `pulumi/__main__.py`

**Find SSH rule in security group:**
```python
# Get your IP first
curl ifconfig.me  # Example: 73.158.197.42

# Update rule
aws.ec2.SecurityGroupIngressArgs(
    protocol="tcp",
    from_port=22,
    to_port=22,
    cidr_blocks=["73.158.197.42/32"],  # ← Your IP only!
    description="SSH from my IP"
),
```

---

### **8. Add Tags**

**File:** `pulumi/__main__.py`

**Find common_tags:**
```python
common_tags = {
    "Project": project_name,
    "ManagedBy": "Pulumi",
    "Stack": stack_name,
    "Environment": stack_name,
    "CostCenter": "Engineering",  # ← NEW
    "Owner": "YourName",  # ← NEW
}
```

**Deploy:** All resources get new tags automatically!

---

### **9. Add Private Subnet**

**File:** `pulumi/__main__.py`

**Add after public subnets:**
```python
# Private Subnet (no internet access)
private_subnet_a = aws.ec2.Subnet(
    f"{project_name}-private-a",
    vpc_id=vpc.id,
    cidr_block="10.0.10.0/24",
    availability_zone=f"{aws_region}a",
    map_public_ip_on_launch=False,  # ← No public IPs!
    tags={**common_tags, "Name": f"{project_name}-private-a-{stack_name}"}
)

# Private Route Table (no IGW route!)
private_route_table = aws.ec2.RouteTable(
    f"{project_name}-private-rt",
    vpc_id=vpc.id,
    tags={**common_tags, "Name": f"{project_name}-private-rt-{stack_name}"}
)

# Associate
private_rt_assoc_a = aws.ec2.RouteTableAssociation(
    f"{project_name}-private-rt-assoc-a",
    subnet_id=private_subnet_a.id,
    route_table_id=private_route_table.id
)
```

---

### **10. Change Configuration Value**

**Instead of editing code:**
```bash
# Change via CLI
pulumi config set vpc_cidr "10.10.0.0/16"
pulumi config set enable_web_server true
pulumi config set enable_vpn false

# View current config
pulumi config

# Deploy with new config
pulumi up
```

---

## ⚠️ **Important Warnings**

### **Resources That Get REPLACED (not updated):**

These changes cause resource deletion + recreation:

```
❌ VPC CIDR block change → Replaces VPC + everything in it
❌ Subnet CIDR block → Replaces subnet + instances in it
❌ Instance type change → Replaces instance (new IP!)
❌ AMI change → Replaces instance
❌ Availability zone change → Replaces subnet
```

**Always run `pulumi preview` first to see what will be replaced!**

### **Resources That Update In-Place:**

These can be changed without replacement:

```
✅ Security group rules
✅ Route table entries
✅ Tags
✅ Instance user data (but won't re-run on existing instance)
✅ Route table associations
```

---

## 🎓 **Learning Tips**

### **1. Start with Documentation**
- Always read the Pulumi docs page first
- Look at the example code
- Copy/modify examples to your needs

### **2. Use Preview Religiously**
```bash
# ALWAYS preview before applying
pulumi preview

# Check:
# - Does it do what I expect?
# - Are resources being replaced unexpectedly?
# - Are dependencies correct?
```

### **3. Make Small Changes**
```
✅ Good: Add one security group rule
✅ Good: Add one subnet
✅ Good: Change one config value

❌ Bad: Rewrite entire __main__.py at once
❌ Bad: Change 10 things simultaneously
```

### **4. Commit Often**
```bash
# After each successful change:
git add .
git commit -m "Add port 8080 to security group"

# Easy to rollback if needed:
git revert HEAD
pulumi up
```

### **5. Read Error Messages**
```
Pulumi errors usually tell you exactly what's wrong:

Error: expecting a single value, received array
→ You passed a list when it expected a single value

Error: resource already exists
→ Name conflict, choose different name

Error: invalid CIDR block
→ Check your CIDR syntax
```

---

## 📝 **Useful Commands**

### **Preview & Deploy:**
```bash
pulumi preview              # Show what will change
pulumi up                   # Apply changes
pulumi up --yes             # Apply without confirmation
pulumi up --diff            # Show detailed diff
```

### **State Management:**
```bash
pulumi stack output         # Show all outputs
pulumi stack output vpc_id  # Show specific output
pulumi stack export         # Export state to JSON
pulumi refresh              # Sync state with AWS
```

### **Configuration:**
```bash
pulumi config               # Show all config
pulumi config set key value # Set config value
pulumi config get key       # Get config value
pulumi config rm key        # Remove config value
```

### **Stack Management:**
```bash
pulumi stack                # Show current stack
pulumi stack ls             # List all stacks
pulumi stack select dev     # Switch to stack
```

### **Cleanup:**
```bash
pulumi destroy              # Delete all resources
pulumi destroy --yes        # Delete without confirmation
pulumi stack rm dev         # Delete stack (after destroy)
```

---

## 🔗 **Quick Links**

**Main Resources:**
- Pulumi AWS Docs: https://www.pulumi.com/registry/packages/aws/
- Pulumi Python Guide: https://www.pulumi.com/docs/languages-sdks/python/
- AWS CLI Reference: https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/index.html

**Your Project:**
- Project Location: `~/Cloud_Networking_Lab/pulumi/__main__.py`
- Config: `~/Cloud_Networking_Lab/pulumi/Pulumi.dev.yaml`
- State: Managed by Pulumi Cloud automatically

---

## 💾 **Save This File!**

Keep this as a reference when making changes to your infrastructure.

**Happy building!** 🚀