# Pulumi Guide - How Infrastructure as Code Works

Complete guide to understanding and using Pulumi in this project.

---

## 🎯 **What is Pulumi?**

Pulumi is an **Infrastructure as Code (IaC)** tool that lets you define cloud infrastructure using **real programming languages** like Python, instead of custom DSLs like Terraform's HCL.

**Key concept:** You write Python code that *declares* what infrastructure you want, then the Pulumi CLI *executes* it.

---

## 🔄 **How Pulumi Works: The Two-Part System**

### **Part 1: Write Python Code** 🐍

You write normal Python code using Pulumi libraries:

```python
# pulumi/__main__.py
import pulumi
import pulumi_aws as aws

# This is just Python!
vpc = aws.ec2.Vpc(
    "my-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True
)

# Export outputs
pulumi.export("vpc_id", vpc.id)
```

**At this point:**
- ❌ Nothing is deployed
- ❌ No AWS resources created  
- ✅ Just Python code declaring your intent

---

### **Part 2: Execute with Pulumi CLI** 💻

Then run the Pulumi CLI to deploy:

```bash
cd pulumi/
pulumi up
```

**What happens:**

1. **Reads `Pulumi.yaml`** → Knows it's a Python project
2. **Executes your Python code** → Runs `__main__.py`
3. **Builds resource graph** → Figures out dependencies
4. **Shows preview** → What will be created/changed/deleted
5. **Waits for confirmation** → You type `yes`
6. **Calls AWS APIs** → Actually creates resources
7. **Stores state** → Remembers what was created
8. **Displays outputs** → Shows `vpc_id`, etc.

---

## 📊 **The Complete Flow Diagram**

```
┌─────────────────────────────────────────────────────────────┐
│ 1. You Write Python Code                                    │
│    vpc = aws.ec2.Vpc("my-vpc", cidr_block="10.0.0.0/16")  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. You Run: pulumi up                                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Pulumi Executes Python                                   │
│    - Runs __main__.py                                       │
│    - Collects resource declarations                         │
│    - Builds dependency graph                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Shows Preview                                            │
│    + aws:ec2:Vpc my-vpc create                              │
│    + aws:ec2:Subnet my-subnet create                        │
│    Do you want to perform this update? [yes/no]            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Calls AWS APIs                                           │
│    - CreateVpc()                                            │
│    - CreateSubnet()                                         │
│    - Tags resources                                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Stores State                                             │
│    - Resource IDs                                           │
│    - Dependencies                                           │
│    - Configuration                                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Shows Results                                            │
│    Resources: 2 created                                     │
│    Outputs:                                                  │
│      vpc_id: "vpc-0abc123..."                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔑 **Key Concepts**

### **Declarative vs Imperative**

**Imperative (boto3):**
```python
# You tell AWS HOW to do it step-by-step
import boto3
ec2 = boto3.client('ec2')

# Step 1: Check if VPC exists
existing = ec2.describe_vpcs(Filters=[{'Name': 'tag:Name', 'Values': ['my-vpc']}])
if not existing['Vpcs']:
    # Step 2: Create it
    vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
    vpc_id = vpc['Vpc']['VpcId']
else:
    # Step 3: Update it
    vpc_id = existing['Vpcs'][0]['VpcId']
    # ... modify tags, etc.
```

**Declarative (Pulumi):**
```python
# You declare WHAT you want, Pulumi figures out HOW
import pulumi_aws as aws

vpc = aws.ec2.Vpc("my-vpc", cidr_block="10.0.0.0/16")
# Pulumi automatically: checks existence, creates/updates/ignores
```

---

### **Resources are Objects**

When you write:
```python
vpc = aws.ec2.Vpc("my-vpc", cidr_block="10.0.0.0/16")
```

You're creating a **Pulumi Resource object**, NOT immediately creating an AWS VPC.

**Think of it as:**
```python
vpc = Resource(
    type="aws:ec2/vpc:Vpc",
    name="my-vpc", 
    properties={"cidr_block": "10.0.0.0/16"}
)
```

It's a *declaration of intent*. The actual VPC is created when you run `pulumi up`.

---

### **Automatic Dependency Management**

```python
vpc = aws.ec2.Vpc("my-vpc", cidr_block="10.0.0.0/16")

subnet = aws.ec2.Subnet(
    "my-subnet",
    vpc_id=vpc.id,  # ← This creates a dependency!
    cidr_block="10.0.1.0/24"
)
```

**Pulumi sees:** Subnet needs VPC ID → VPC must be created first

**Pulumi automatically:**
1. Creates VPC
2. Waits for VPC to be ready
3. Gets VPC ID
4. Creates Subnet with that VPC ID

**You don't manage order manually!**

---

### **State Management**

Pulumi stores state about your infrastructure:

- What resources exist
- Their IDs and properties
- Dependencies between them
- Configuration values

**State can be stored:**
- Pulumi Cloud (free, recommended)
- Local filesystem
- S3 bucket
- Azure Blob Storage

```bash
# View state
pulumi stack

# View specific resource
pulumi stack export
```

---

### **Outputs**

Export values you'll need later:

```python
import pulumi

vpc = aws.ec2.Vpc("my-vpc", cidr_block="10.0.0.0/16")

# Export the VPC ID
pulumi.export("vpc_id", vpc.id)
pulumi.export("vpc_cidr", vpc.cidr_block)
```

**View outputs:**
```bash
pulumi stack output
pulumi stack output vpc_id
```

---

## 📝 **Essential Pulumi CLI Commands**

### **One-Time Setup**

```bash
cd pulumi/

# Create a new stack (dev, staging, prod)
pulumi stack init dev

# Login to Pulumi Cloud (or use --local)
pulumi login
```

---

### **Configuration**

```bash
# Set configuration values
pulumi config set aws:region us-east-1
pulumi config set vpc_cidr 10.0.0.0/16

# Set secrets (encrypted)
pulumi config set --secret db_password mySecretPassword

# View configuration
pulumi config
```

---

### **Core Workflow**

```bash
# Preview changes (dry-run)
pulumi preview

# Create/update infrastructure
pulumi up

# Skip preview and auto-approve
pulumi up --yes

# Refresh state from actual infrastructure
pulumi refresh

# View stack information
pulumi stack

# View outputs
pulumi stack output
pulumi stack output vpc_id

# Destroy all resources
pulumi destroy
```

---

### **Stack Management**

```bash
# List all stacks
pulumi stack ls

# Switch to a different stack
pulumi stack select staging

# View stack history
pulumi stack history

# Export stack state (backup)
pulumi stack export > backup.json

# Import stack state (restore)
pulumi stack import < backup.json
```

---

## 🎯 **Stacks: Multiple Environments**

A **stack** is an instance of your Pulumi program. Use stacks for:

- **dev** - Development environment
- **staging** - Pre-production testing
- **prod** - Production

### **Same code, different configs:**

```bash
# Development stack
pulumi stack init dev
pulumi config set aws:region us-east-1
pulumi config set vpc_cidr 10.0.0.0/16
pulumi up

# Production stack (separate infrastructure!)
pulumi stack init prod
pulumi config set aws:region us-west-2
pulumi config set vpc_cidr 10.1.0.0/16
pulumi up
```

**Result:** Two completely separate VPCs, managed by the same code!

---

## 🔄 **Pulumi Update Process**

### **What Happens During `pulumi up`:**

1. **Read configuration**
   - Reads `Pulumi.yaml`
   - Loads stack config
   - Sets environment variables

2. **Execute Python program**
   - Runs `__main__.py`
   - Collects resource declarations
   - Builds dependency graph

3. **Compare desired vs actual**
   - Reads stored state
   - Compares to what you declared
   - Determines diff

4. **Show preview**
   ```
   + Create: 2 resources
   ~ Update: 1 resource
   - Delete: 0 resources
   ```

5. **Wait for confirmation**
   - `yes` = proceed
   - `no` = cancel

6. **Apply changes**
   - Calls AWS APIs in dependency order
   - Updates state after each resource
   - Rolls back on error (if possible)

7. **Display results**
   - Shows what was created/updated
   - Displays outputs
   - Reports any errors

---

## 🆚 **Pulumi vs Other Tools**

### **Pulumi vs Terraform**

| Feature | Terraform | Pulumi |
|---------|-----------|--------|
| **Language** | HCL (custom DSL) | Real Python/TypeScript/Go |
| **Loops** | `for_each`, `count` | Native Python loops |
| **Conditionals** | `count = condition ? 1 : 0` | Native Python `if/else` |
| **Functions** | Limited built-ins | Full Python standard library |
| **Testing** | External tools | pytest, unittest |
| **Type Safety** | Limited | Full (with Pydantic!) |
| **IDE Support** | Basic | Full autocomplete/IntelliSense |
| **Learning Curve** | Learn HCL | Use Python you know |

### **Pulumi vs boto3**

| Feature | boto3 | Pulumi |
|---------|-------|--------|
| **Style** | Imperative | Declarative |
| **State** | You manage | Automatic |
| **Idempotency** | You implement | Built-in |
| **Dependencies** | You order | Automatic |
| **Diffs** | Manual | Automatic preview |
| **Rollback** | Manual | Automatic (partial) |

---

## 💡 **Best Practices**

### **1. Use Configuration, Not Hard-Coding**

❌ **Bad:**
```python
vpc = aws.ec2.Vpc("my-vpc", cidr_block="10.0.0.0/16")
```

✅ **Good:**
```python
config = pulumi.Config()
vpc_cidr = config.get("vpc_cidr") or "10.0.0.0/16"
vpc = aws.ec2.Vpc("my-vpc", cidr_block=vpc_cidr)
```

---

### **2. Use Stacks for Environments**

```bash
# Don't create dev-vpc, staging-vpc, prod-vpc resources
# Instead, use stacks:

pulumi stack init dev
pulumi up  # Creates resources with stack name

pulumi stack init prod
pulumi up  # Creates separate resources
```

---

### **3. Export Important Outputs**

```python
# Export anything you might need later
pulumi.export("vpc_id", vpc.id)
pulumi.export("subnet_ids", [s.id for s in subnets])
pulumi.export("vpn_config", vpn_connection.customer_gateway_configuration)
```

---

### **4. Use Tags Consistently**

```python
common_tags = {
    "Environment": pulumi.get_stack(),
    "Project": pulumi.get_project(),
    "ManagedBy": "Pulumi"
}

vpc = aws.ec2.Vpc(
    "my-vpc",
    cidr_block="10.0.0.0/16",
    tags=common_tags
)
```

---

### **5. Modularize Code**

Don't put everything in `__main__.py`:

```
pulumi/
├── __main__.py       # Main program
├── vpc.py            # VPC module
├── vpn.py            # VPN module
└── networking.py     # Networking module
```

```python
# __main__.py
from vpc import create_vpc
from vpn import create_vpn_gateway

vpc = create_vpc("my-vpc", "10.0.0.0/16")
vpn = create_vpn_gateway("my-vpn", vpc.id)
```

---

## 🐛 **Troubleshooting**

### **"No Pulumi.yaml found"**

```bash
# Make sure you're in the right directory
cd pulumi/
ls Pulumi.yaml  # Should exist

# Or specify the path
pulumi up --cwd pulumi/
```

---

### **"Resource already exists"**

Pulumi detected a resource in AWS that matches but isn't in state.

**Option 1: Import it**
```bash
pulumi import aws:ec2/vpc:Vpc my-vpc vpc-abc123
```

**Option 2: Delete and recreate**
```bash
# Delete from AWS manually, then
pulumi up
```

---

### **"Conflict: Another update in progress"**

Someone else is running `pulumi up`, or previous run crashed.

```bash
# Cancel the lock (if you're sure it's safe)
pulumi cancel
```

---

### **State is out of sync**

Actual infrastructure doesn't match Pulumi's state.

```bash
# Refresh state from AWS
pulumi refresh

# Then update as needed
pulumi up
```

---

## 🧪 **Testing Your Pulumi Code**

### **Unit Tests (pytest)**

Test your infrastructure logic:

```python
# tests/unit/test_vpc.py
from pulumi import Config
from pulumi_aws import ec2

def test_vpc_cidr():
    """Test VPC CIDR is valid."""
    vpc = ec2.Vpc("test-vpc", cidr_block="10.0.0.0/16")
    assert vpc.cidr_block == "10.0.0.0/16"
```

### **Preview Before Apply**

Always run preview first:

```bash
# See what will change
pulumi preview

# Then apply
pulumi up
```

---

## 📚 **Learning Resources**

- **Pulumi Docs:** https://www.pulumi.com/docs/
- **AWS Provider:** https://www.pulumi.com/registry/packages/aws/
- **Python Guide:** https://www.pulumi.com/docs/languages-sdks/python/
- **Examples:** https://github.com/pulumi/examples

---

## 🎓 **Summary**

**Remember:**

1. ✅ **Python = Declaration** - "I want this infrastructure"
2. ✅ **CLI = Execution** - "Let me create it"
3. ✅ **State = Memory** - "Here's what exists"
4. ✅ **Stacks = Environments** - "Dev, staging, prod"
5. ✅ **Outputs = Results** - "Here's what was created"

**Workflow:**
```bash
# Write Python code
vim __main__.py

# Preview changes
pulumi preview

# Apply changes
pulumi up

# View results
pulumi stack output
```

**That's Pulumi!** 🚀

---

**Next:** Try deploying your first VPC with `pulumi up`!
