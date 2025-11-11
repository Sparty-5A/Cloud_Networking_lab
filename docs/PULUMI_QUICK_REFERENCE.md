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

## 💡 **Common Changes (Complete Examples)**

All examples below work directly in your Cloud Networking Lab project!

---

### **Example 1: Add Security Group Rule (Port 3306 for MySQL)**

**Scenario:** Allow MySQL traffic (port 3306) from VPC only (for database tier)

**Documentation:** https://www.pulumi.com/registry/packages/aws/api-docs/ec2/securitygroup/

**File:** `pulumi/__main__.py` (around line 205)

**Find this section:**
```python
default_sg = aws.ec2.SecurityGroup(
    f"{project_name}-default-sg",
    vpc_id=vpc.id,
    description="Default security group for Cloud Networking Lab",
    ingress=[
        # ... existing rules ...
    ],
```

**Add this rule to the ingress list:**
```python
        # Allow MySQL from VPC only
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=3306,
            to_port=3306,
            cidr_blocks=[vpc_cidr],
            description="MySQL from VPC"
        ),
```

**Complete updated section:**
```python
default_sg = aws.ec2.SecurityGroup(
    f"{project_name}-default-sg",
    vpc_id=vpc.id,
    description="Default security group for Cloud Networking Lab",
    ingress=[
        # Allow ICMP (ping) from VPC
        aws.ec2.SecurityGroupIngressArgs(
            protocol="icmp",
            from_port=-1,
            to_port=-1,
            cidr_blocks=[vpc_cidr]
        ),
        # Allow SSH from anywhere (restrict in production!)
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"]
        ),
        # Allow HTTP from anywhere (for web server)
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=80,
            to_port=80,
            cidr_blocks=["0.0.0.0/0"]
        ),
        # Allow HTTPS from anywhere (for future use)
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=443,
            to_port=443,
            cidr_blocks=["0.0.0.0/0"]
        ),
        # NEW: Allow MySQL from VPC only
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=3306,
            to_port=3306,
            cidr_blocks=[vpc_cidr],
            description="MySQL from VPC"
        ),
        # Allow all traffic within VPC
        aws.ec2.SecurityGroupIngressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=[vpc_cidr]
        )
    ],
    egress=[
        # Allow all outbound traffic
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"]
        )
    ],
    tags={**common_tags, "Name": f"{project_name}-default-sg-{stack_name}"}
)
```

**Deploy:**
```bash
cd ~/Cloud_Networking_Lab/pulumi
source ../.venv/bin/activate
pulumi preview  # Check the change
pulumi up       # Apply it
```

**What happens:**
- Security group updated in-place (no replacement)
- Port 3306 now allowed from 10.0.0.0/16
- Web server can now connect to database on port 3306

---

### **Example 2: Add Third Subnet (us-east-1c)**

**Scenario:** Add third public subnet for more availability zones

**Documentation:** https://www.pulumi.com/registry/packages/aws/api-docs/ec2/subnet/

**File:** `pulumi/__main__.py` (around line 140, after subnet B)

**Add this code:**
```python
# Public Subnet C (us-east-1c)
public_subnet_c = aws.ec2.Subnet(
    f"{project_name}-public-c",
    vpc_id=vpc.id,
    cidr_block="10.0.3.0/24",  # New CIDR block (10.0.3.x)
    availability_zone=f"{aws_region}c",  # Third AZ
    map_public_ip_on_launch=True,
    tags={**common_tags, "Name": f"{project_name}-public-c-{stack_name}"}
)

# Associate Subnet C with public route table
public_rt_assoc_c = aws.ec2.RouteTableAssociation(
    f"{project_name}-public-rt-assoc-c",
    subnet_id=public_subnet_c.id,
    route_table_id=public_route_table.id
)
```

**Also add exports (around line 395):**
```python
pulumi.export("public_subnet_c_id", public_subnet_c.id)
pulumi.export("public_subnet_c_cidr", public_subnet_c.cidr_block)
pulumi.export("public_subnet_c_az", public_subnet_c.availability_zone)
```

**Deploy:**
```bash
pulumi up
```

**What happens:**
- New subnet created: 10.0.3.0/24 in us-east-1c
- Automatically associated with public route table
- Has internet access via IGW
- Can deploy resources across 3 AZs now!

---

### **Example 3: Add Private Subnet (No Internet Access)**

**Scenario:** Create private subnet for databases (no direct internet access)

**Documentation:** https://www.pulumi.com/registry/packages/aws/api-docs/ec2/subnet/

**File:** `pulumi/__main__.py` (add after public subnets section)

**Add this complete section:**
```python
# ==========================================
# Private Subnets (no direct internet access)
# ==========================================

# Private Subnet A (us-east-1a)
private_subnet_a = aws.ec2.Subnet(
    f"{project_name}-private-a",
    vpc_id=vpc.id,
    cidr_block="10.0.10.0/24",  # Different range from public
    availability_zone=f"{aws_region}a",
    map_public_ip_on_launch=False,  # ← KEY: No public IPs!
    tags={**common_tags, "Name": f"{project_name}-private-a-{stack_name}"}
)

# Private Route Table (no IGW route!)
private_route_table = aws.ec2.RouteTable(
    f"{project_name}-private-rt",
    vpc_id=vpc.id,
    tags={**common_tags, "Name": f"{project_name}-private-rt-{stack_name}"}
)

# Associate private subnet with private route table
private_rt_assoc_a = aws.ec2.RouteTableAssociation(
    f"{project_name}-private-rt-assoc-a",
    subnet_id=private_subnet_a.id,
    route_table_id=private_route_table.id
)

# Note: No route to IGW! Only has local route (automatic)
# Resources here can talk to VPC but NOT internet
```

**Add exports:**
```python
pulumi.export("private_subnet_a_id", private_subnet_a.id)
pulumi.export("private_subnet_a_cidr", private_subnet_a.cidr_block)
pulumi.export("private_route_table_id", private_route_table.id)
```

**What's different from public subnet:**
```
Public Subnet:
- map_public_ip_on_launch=True
- Route table has: 0.0.0.0/0 → IGW
- Resources get public IPs
- Direct internet access

Private Subnet:
- map_public_ip_on_launch=False
- Route table has: only local routes
- Resources get private IPs only
- No direct internet access
```

**Use case:** Deploy RDS database in private subnet for security!

---

### **Example 4: Add Static Route to On-Prem (VPN)**

**Scenario:** Route traffic to on-premises network (192.168.0.0/16) through VPN gateway

**Documentation:** https://www.pulumi.com/registry/packages/aws/api-docs/ec2/route/

**File:** `pulumi/__main__.py` (in VPN section, around line 280)

**Add after VPN gateway creation:**
```python
if enable_vpn:
    # ... existing VPN gateway code ...
    
    # NEW: Add static route to on-prem network
    on_prem_route = aws.ec2.Route(
        "to-on-prem",
        route_table_id=public_route_table.id,
        destination_cidr_block="192.168.0.0/16",  # Your on-prem network
        gateway_id=vpn_gateway.id  # Send through VPN
    )
    
    pulumi.export("on_prem_route", "192.168.0.0/16 → VPN Gateway")
```

**What this does:**
```
Before:
10.0.0.0/16  → local
0.0.0.0/0    → Internet Gateway

After:
10.0.0.0/16    → local
192.168.0.0/16 → VPN Gateway  ← NEW!
0.0.0.0/0      → Internet Gateway
```

**Result:** Traffic to 192.168.x.x goes through VPN to your home network!

---

### **Example 5: Change Instance Type (t3.micro → t3.small)**

**Scenario:** Upgrade web server for more CPU/memory

**Documentation:** https://www.pulumi.com/registry/packages/aws/api-docs/ec2/instance/

**File:** `pulumi/__main__.py` (around line 350)

**Change from:**
```python
    web_server = aws.ec2.Instance(
        f"{project_name}-web-server",
        instance_type="t3.micro",  # 1 vCPU, 1 GB RAM
        ami=ami.id,
        # ... rest
    )
```

**To:**
```python
    web_server = aws.ec2.Instance(
        f"{project_name}-web-server",
        instance_type="t3.small",  # 2 vCPU, 2 GB RAM
        ami=ami.id,
        # ... rest
    )
```

**Preview first:**
```bash
pulumi preview
```

**Output shows:**
```
~ aws:ec2:Instance: (replace)
    [id=i-0155f5650a02758b4]
  ~ instanceType: "t3.micro" => "t3.small"

Warning: This will REPLACE the instance!
- Old instance deleted
- New instance created
- New public IP assigned
- User data runs again
```

**Important notes:**
- ⚠️ Instance will be REPLACED (not updated in-place)
- ⚠️ Public IP will change
- ⚠️ Any data on instance will be lost
- 💰 Cost changes: ~$7.60/month → ~$15/month

**Deploy:**
```bash
pulumi up  # Type "yes" to confirm replacement
```

---

### **Example 6: Add Second Web Server (Multi-AZ)**

**Scenario:** Deploy second web server in different AZ for high availability

**Documentation:** https://www.pulumi.com/registry/packages/aws/api-docs/ec2/instance/

**File:** `pulumi/__main__.py` (around line 350)

**Modify existing web server code:**
```python
if enable_web_server:
    pulumi.log.info(f"Launching web servers in {project_name}-vpc")
    
    # User data script (same for both)
    user_data = """#!/bin/bash
    # ... (keep existing user data script)
    """
    
    # Web Server A (existing, rename)
    web_server_a = aws.ec2.Instance(
        f"{project_name}-web-server-a",  # ← Changed name
        instance_type="t3.micro",
        ami=ami.id,
        subnet_id=public_subnet_a.id,  # ← In AZ-A
        vpc_security_group_ids=[default_sg.id],
        user_data=user_data,
        associate_public_ip_address=True,
        tags={**common_tags, "Name": f"{project_name}-web-server-a-{stack_name}"}
    )
    
    # Web Server B (NEW!)
    web_server_b = aws.ec2.Instance(
        f"{project_name}-web-server-b",  # ← New server
        instance_type="t3.micro",
        ami=ami.id,
        subnet_id=public_subnet_b.id,  # ← In AZ-B (different AZ!)
        vpc_security_group_ids=[default_sg.id],
        user_data=user_data,  # Same configuration
        associate_public_ip_address=True,
        tags={**common_tags, "Name": f"{project_name}-web-server-b-{stack_name}"}
    )
    
    # Export both IPs
    pulumi.export("web_server_a_id", web_server_a.id)
    pulumi.export("web_server_a_public_ip", web_server_a.public_ip)
    pulumi.export("web_server_a_url", web_server_a.public_ip.apply(lambda ip: f"http://{ip}"))
    
    pulumi.export("web_server_b_id", web_server_b.id)
    pulumi.export("web_server_b_public_ip", web_server_b.public_ip)
    pulumi.export("web_server_b_url", web_server_b.public_ip.apply(lambda ip: f"http://{ip}"))
```

**What you get:**
```
Web Server A: 10.0.1.x in us-east-1a
Web Server B: 10.0.2.x in us-east-1b

Both running nginx with same content
Both have public IPs
Survive single AZ failure!
```

**Cost:** ~$15/month (double the web servers)

**Next step:** Add Application Load Balancer to distribute traffic between them!

---

### **Example 7: Add NAT Gateway (For Private Subnets)**

**Scenario:** Allow private subnet resources to access internet (outbound only)

**Documentation:** https://www.pulumi.com/registry/packages/aws/api-docs/ec2/natgateway/

**File:** `pulumi/__main__.py` (after private subnet section)

**Add this code:**
```python
# ==========================================
# NAT Gateway (for private subnet internet access)
# ==========================================

enable_nat = config.get_bool("enable_nat") or False

if enable_nat:
    pulumi.log.info("Creating NAT Gateway for private subnet internet access")
    
    # Elastic IP for NAT Gateway
    nat_eip = aws.ec2.Eip(
        f"{project_name}-nat-eip",
        vpc=True,
        tags={**common_tags, "Name": f"{project_name}-nat-eip-{stack_name}"}
    )
    
    # NAT Gateway (must be in PUBLIC subnet!)
    nat_gateway = aws.ec2.NatGateway(
        f"{project_name}-nat-gw",
        subnet_id=public_subnet_a.id,  # ← In PUBLIC subnet!
        allocation_id=nat_eip.id,
        tags={**common_tags, "Name": f"{project_name}-nat-gw-{stack_name}"}
    )
    
    # Add route in PRIVATE route table
    private_nat_route = aws.ec2.Route(
        "private-to-nat",
        route_table_id=private_route_table.id,  # ← Private RT!
        destination_cidr_block="0.0.0.0/0",
        nat_gateway_id=nat_gateway.id  # ← Through NAT!
    )
    
    # Exports
    pulumi.export("nat_gateway_id", nat_gateway.id)
    pulumi.export("nat_eip", nat_eip.public_ip)
```

**Enable NAT Gateway:**
```bash
pulumi config set enable_nat true
pulumi up
```

**How it works:**
```
Private Subnet Resource (10.0.10.5):
    ↓ Wants to reach internet
Private Route Table:
    0.0.0.0/0 → NAT Gateway
    ↓
NAT Gateway (in public subnet):
    ↓ Translates private IP → public IP
Public Route Table:
    0.0.0.0/0 → Internet Gateway
    ↓
Internet!
```

**Use case:** 
- Database in private subnet needs to download updates
- App server in private subnet needs to call external API

**Cost:** ~$32/month + data transfer (NOT free tier!)

---

### **Example 8: Restrict SSH to Your IP Only**

**Scenario:** Lock down SSH access for security (best practice!)

**Documentation:** https://www.pulumi.com/registry/packages/aws/api-docs/ec2/securitygroup/

**File:** `pulumi/__main__.py` (around line 210)

**Step 1: Get your public IP:**
```bash
curl ifconfig.me
# Example output: 73.158.197.42
```

**Step 2: Update security group:**

**Change from:**
```python
        # Allow SSH from anywhere (restrict in production!)
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"]  # ← Anyone can try!
        ),
```

**To:**
```python
        # Allow SSH from my IP only
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["73.158.197.42/32"],  # ← Only you!
            description="SSH from my home"
        ),
```

**Deploy:**
```bash
pulumi up
```

**Result:**
- ✅ You can SSH from your IP
- ❌ No one else can even try
- 🔒 Much more secure!

**Note:** If your home IP changes (dynamic IP), update and redeploy!

**Better solution for production:**
- Use AWS Systems Manager Session Manager (no SSH needed!)
- Or use bastion host with AWS IAM authentication

---

### **Example 9: Add Tags to All Resources**

**Scenario:** Add cost tracking and ownership tags

**Documentation:** Tags are supported on all resources

**File:** `pulumi/__main__.py` (around line 35)

**Find common_tags, modify:**
```python
# Common tags for all resources
common_tags = {
    "Project": project_name,
    "ManagedBy": "Pulumi",
    "Stack": stack_name,
    "Environment": stack_name,
    # NEW TAGS:
    "CostCenter": "Engineering",  # For cost allocation
    "Owner": "YourName",           # Who manages this
    "Purpose": "CloudNetworkingLab", # What is this for
    "Terraform": "false",          # Track IaC tool used
}
```

**Deploy:**
```bash
pulumi up
```

**What happens:**
- All existing resources get new tags automatically!
- No resources replaced
- Updates in-place
- Can now filter/search by these tags in AWS Console

**Use in AWS Console:**
```
Cost Explorer → Filter by tag "CostCenter: Engineering"
→ See all costs for this project!

EC2 Dashboard → Filter by tag "Owner: YourName"
→ See all your resources!
```

---

### **Example 10: Change VPC CIDR Block**

**Scenario:** Use different IP address range

**Documentation:** https://www.pulumi.com/registry/packages/aws/api-docs/ec2/vpc/

**File:** Configuration (not code!)

**Via Pulumi config:**
```bash
# Check current CIDR
pulumi config get vpc_cidr
# Output: 10.0.0.0/16

# Change to different range
pulumi config set vpc_cidr "10.10.0.0/16"
```

**Also update subnet CIDRs in code:**

**File:** `pulumi/__main__.py`

**Change:**
```python
# Public Subnet A
public_subnet_a = aws.ec2.Subnet(
    f"{project_name}-public-a",
    vpc_id=vpc.id,
    cidr_block="10.10.1.0/24",  # ← Changed from 10.0.1.0/24
    # ...
)

# Public Subnet B
public_subnet_b = aws.ec2.Subnet(
    f"{project_name}-public-b",
    vpc_id=vpc.id,
    cidr_block="10.10.2.0/24",  # ← Changed from 10.0.2.0/24
    # ...
)
```

**Preview:**
```bash
pulumi preview
```

**Output shows:**
```
Replacing resources:
  ~ VPC (CIDR change)
  ~ All subnets (VPC changed)
  ~ All instances (subnet changed)
  ~ Everything!

This is a MAJOR change!
```

**⚠️ WARNING:** This will destroy and recreate EVERYTHING!

**Better approach:**
1. Create new VPC with new CIDR
2. Migrate resources
3. Delete old VPC
4. Or just destroy and recreate if nothing important

**Use case:**
- Avoid IP conflicts with on-prem
- Need larger address space
- Starting fresh

---

## 🔄 **AWS vs Traditional Networking Examples**

Understanding how Pulumi maps to both AWS and traditional networking concepts.

---

### **Example: Add a Static Route**

**Traditional Router (Cisco IOS):**
```
router# configure terminal
router(config)# ip route 192.168.0.0 255.255.0.0 vpn-tunnel0
router(config)# exit
router# write memory
```

**AWS Console:**
```
1. VPC → Route Tables → Select rtb-xxxxx
2. Routes tab → Edit routes
3. Add route:
   - Destination: 192.168.0.0/16
   - Target: VPN Gateway (vgw-xxxxx)
4. Save routes
```

**AWS CLI:**
```bash
aws ec2 create-route \
  --route-table-id rtb-0590476d3f54ad6c2 \
  --destination-cidr-block 192.168.0.0/16 \
  --gateway-id vgw-xxxxx
```

**Pulumi (Infrastructure as Code):**
```python
on_prem_route = aws.ec2.Route(
    "to-on-prem",
    route_table_id=public_route_table.id,
    destination_cidr_block="192.168.0.0/16",
    gateway_id=vpn_gateway.id
)
```

**Benefits of Pulumi approach:**
- ✅ Version controlled (Git)
- ✅ Can preview before applying
- ✅ Documented in code
- ✅ Repeatable across environments
- ✅ Easy to rollback

---

### **Example: Configure Firewall Rule**

**Traditional Firewall:**
```
firewall(config)# access-list 100 permit tcp any any eq 80
firewall(config)# access-list 100 permit tcp any any eq 443
firewall(config)# interface outside
firewall(config-if)# ip access-group 100 in
```

**AWS Console:**
```
1. EC2 → Security Groups → Select sg-xxxxx
2. Inbound rules → Edit
3. Add rules:
   - Type: HTTP, Port: 80, Source: 0.0.0.0/0
   - Type: HTTPS, Port: 443, Source: 0.0.0.0/0
4. Save
```

**AWS CLI:**
```bash
aws ec2 authorize-security-group-ingress \
  --group-id sg-0b61c47c3ec676c5c \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-id sg-0b61c47c3ec676c5c \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0
```

**Pulumi:**
```python
web_sg = aws.ec2.SecurityGroup("web-sg",
    vpc_id=vpc.id,
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=80,
            to_port=80,
            cidr_blocks=["0.0.0.0/0"],
            description="HTTP from internet"
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=443,
            to_port=443,
            cidr_blocks=["0.0.0.0/0"],
            description="HTTPS from internet"
        ),
    ]
)
```

---

### **Example: View Configuration**

**Traditional Router:**
```
router# show running-config
router# show ip route
router# show ip interface brief
router# show access-lists
```

**AWS Console:**
```
1. VPC Dashboard → Your VPCs → Click vpc-xxxxx
2. Route Tables → Select → Routes tab
3. Subnets → View list
4. Security Groups → Select → Inbound rules
```

**AWS CLI:**
```bash
# Show VPC config
aws ec2 describe-vpcs --vpc-ids vpc-06f243cd89e27f2de

# Show routes (like "show ip route")
aws ec2 describe-route-tables --route-table-ids rtb-0590476d3f54ad6c2

# Show subnets (like "show ip interface")
aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-06f243cd89e27f2de"

# Show security groups (like "show access-list")
aws ec2 describe-security-groups --group-ids sg-0b61c47c3ec676c5c
```

**Pulumi:**
```bash
# Show all outputs (like "show run")
pulumi stack output

# Show specific output
pulumi stack output vpc_id
pulumi stack output web_server_public_ip

# Show what's deployed
pulumi stack

# Export full state
pulumi stack export > state.json
```

---

### **Example: Backup Configuration**

**Traditional Router:**
```
router# copy running-config tftp://server/backup.cfg
router# copy running-config startup-config
```

**AWS:**
```
No native "backup config" command
Config is stored in AWS's database
Can export via CLI/SDK
```

**Pulumi:**
```bash
# Your code IS your backup!
git add .
git commit -m "Current working config"
git push

# Can also export state
pulumi stack export > backup-$(date +%Y%m%d).json

# Restore from Git
git checkout main
pulumi up  # Restores to this version
```

---

### **Example: Roll Back Changes**

**Traditional Router:**
```
! Undo last command
router(config)# no ip route 192.168.0.0 255.255.0.0

! Or reload from backup
router# copy tftp://server/backup.cfg running-config
router# reload
```

**AWS Console:**
```
Manual process:
1. Remember what you changed
2. Navigate to resource
3. Click Edit
4. Change back
5. Save
6. Hope you didn't forget anything
```

**AWS CLI:**
```bash
# Delete route
aws ec2 delete-route \
  --route-table-id rtb-0590476d3f54ad6c2 \
  --destination-cidr-block 192.168.0.0/16

# Manually undo each change
# Hope you documented what you did!
```

**Pulumi:**
```bash
# Option 1: Git revert
git revert HEAD
pulumi up  # Automatically undoes changes!

# Option 2: Git reset
git reset --hard HEAD~1
pulumi up

# Option 3: Redeploy specific version
git checkout abc123  # Previous commit
pulumi up
```

---

### **Concept Mapping Table**

| Traditional | AWS Service | Pulumi Resource | Your Code Location |
|-------------|-------------|-----------------|-------------------|
| **Router** | VPC + Route Tables | `aws.ec2.Vpc`, `aws.ec2.RouteTable` | Line 85, 170 |
| **Switch VLAN** | Subnet | `aws.ec2.Subnet` | Line 110, 130 |
| **ACL/Firewall** | Security Group | `aws.ec2.SecurityGroup` | Line 205 |
| **Interface** | ENI | `aws.ec2.NetworkInterface` | Auto-created |
| **Default route** | Internet Gateway | `aws.ec2.InternetGateway` | Line 155 |
| **Static route** | Route | `aws.ec2.Route` | Line 185 |
| **NAT** | NAT Gateway | `aws.ec2.NatGateway` | (example above) |
| **VPN tunnel** | VPN Gateway | `aws.ec2.VpnGateway` | Line 260 |
| **Server** | EC2 Instance | `aws.ec2.Instance` | Line 350 |
| **show run** | describe-* | `pulumi stack output` | Command line |
| **copy run start** | - | `git commit` | Command line |

---

## 🎓 **Key Differences**

### **Traditional Networking:**
```
✅ Physical devices
✅ CLI-first (SSH to device)
✅ Manual configuration
✅ Show/configure commands
✅ Save to startup-config
✅ Limited automation
```

### **AWS Cloud Networking:**
```
✅ Virtual/software-defined
✅ API-first (everything is API call)
✅ Multiple interfaces (Console, CLI, IaC)
✅ Infrastructure as Code
✅ Git as "startup-config"
✅ Fully automatable
```

### **Pulumi Benefits:**
```
✅ All AWS benefits PLUS:
✅ Version control (Git)
✅ Preview before apply
✅ Automatic rollback capability
✅ Code is documentation
✅ Type checking (Python)
✅ Reusable across environments
✅ Team collaboration
✅ Testing possible
```

---

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
