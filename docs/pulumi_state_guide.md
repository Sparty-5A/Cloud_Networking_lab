# Pulumi State Management Guide

**Complete guide to understanding, viewing, and managing Pulumi state**

---

## 📍 **Where is Your State Stored?**

### **Check Your Backend:**

```bash
cd ~/Cloud_Networking_Lab/pulumi

# See where state is stored
pulumi whoami -v
```

**Possible outputs:**

**Pulumi Cloud (Default):**
```
User: your-username
Backend URL: https://api.pulumi.com/your-username
```

**Local Backend:**
```
User: your-username
Backend URL: file://~/.pulumi
```

---

## 🔄 **Switching Backends**

### **Use Pulumi Cloud (Default):**

```bash
# Login to Pulumi Cloud
pulumi login

# Your state will be stored at:
# https://app.pulumi.com
```

**Pros:**
- ✅ Backed up automatically
- ✅ Team collaboration support
- ✅ State locking (prevents conflicts)
- ✅ Free for individuals
- ✅ History tracking
- ✅ Web UI to view state

**Cons:**
- ⚠️ Requires internet connection
- ⚠️ State is on external service

---

### **Use Local Backend:**

```bash
# Logout from Pulumi Cloud
pulumi logout

# Login to local backend
pulumi login --local

# Your state will be stored at:
# ~/.pulumi/stacks/
```

**Pros:**
- ✅ Complete control over state
- ✅ No external dependencies
- ✅ Works offline
- ✅ No account needed

**Cons:**
- ⚠️ Manual backups required
- ⚠️ No collaboration features
- ⚠️ No automatic state locking
- ⚠️ State created ONLY after first `pulumi up`

---

## ⏰ **When is State Created?**

### **IMPORTANT: State is NOT Created Until First Deployment**

```bash
# You do this:
pulumi login --local
pulumi stack init local

# At this point: NO state file exists yet!
# ~/.pulumi/stacks/ directory doesn't exist yet

# State is created ONLY when you run:
pulumi up

# THEN ~/.pulumi/stacks/cloud-networking-lab/local.json is created
```

**Why?**
- Stack initialization just registers the stack
- State file is created when first resource is deployed
- Empty stacks don't need state files

---

## 📂 **Local State Location**

### **After First `pulumi up`:**

```bash
# State files are stored at:
~/.pulumi/
├── credentials.json          # Your login info
├── workspaces/
│   └── cloud-networking-lab-xyz123/
│       └── .pulumi/
│           └── stacks/
│               ├── local.json      # Local stack state
│               └── dev.json        # Dev stack state
```

**OR (simpler structure):**

```bash
~/.pulumi/
├── stacks/
│   └── cloud-networking-lab/
│       ├── local.json
│       └── dev.json
```

---

## 🔍 **How to View Your State**

### **Method 1: Export State (Easiest)**

```bash
cd ~/Cloud_Networking_Lab/pulumi

# Select your stack
pulumi stack select local

# Export entire state as JSON (to screen)
pulumi stack export

# Save to file for easier reading
pulumi stack export > state.json

# View with nice formatting (requires jq)
pulumi stack export | jq .

# View without jq
pulumi stack export | python -m json.tool
```

---

### **Method 2: View Outputs (Quick Check)**

```bash
# See what's deployed (high-level)
pulumi stack output

# Example output:
# vpc_id                : vpc-abc123
# vpc_cidr             : 10.0.0.0/16
# public_subnet_a_id   : subnet-xyz789
# web_server_public_ip : 127.0.0.1
```

---

### **Method 3: List Resources**

```bash
# See all resources in current stack
pulumi stack --show-urns

# List just resource types and IDs
pulumi stack export | jq '.deployment.resources[] | {type: .type, id: .id}'

# Count resources
pulumi stack export | jq '.deployment.resources | length'
```

**Output:**
```json
{
  "type": "aws:ec2/vpc:Vpc",
  "id": "vpc-abc123"
}
{
  "type": "aws:ec2/subnet:Subnet",
  "id": "subnet-xyz789"
}
{
  "type": "aws:ec2/internetGateway:InternetGateway",
  "id": "igw-def456"
}
```

---

### **Method 4: View in Pulumi Cloud**

**If using Pulumi Cloud:**

1. Go to: https://app.pulumi.com
2. Login with your account
3. Navigate to: Your organization → cloud-networking-lab project
4. Select stack: `local` or `dev`
5. Click **"Resources" tab** - See all resources
6. Click **"Activity" tab** - See deployment history
7. Click **"Settings" tab** - Manage stack

---

## 📊 **State File Structure**

### **What's in the State File:**

```json
{
  "version": 3,
  "deployment": {
    "manifest": {
      "time": "2025-11-09T10:30:00Z",
      "magic": "abc123...",
      "version": "v3.95.0"
    },
    "resources": [
      {
        // Resource 1: The Stack itself
        "urn": "urn:pulumi:local::cloud-networking-lab::pulumi:pulumi:Stack",
        "type": "pulumi:pulumi:Stack",
        "custom": true
      },
      {
        // Resource 2: Your VPC
        "urn": "urn:pulumi:local::cloud-networking-lab::aws:ec2/vpc:Vpc::cloud-networking-lab-vpc",
        "type": "aws:ec2/vpc:Vpc",
        "id": "vpc-abc123",
        "inputs": {
          "cidrBlock": "10.0.0.0/16",
          "enableDnsHostnames": true,
          "enableDnsSupport": true
        },
        "outputs": {
          "id": "vpc-abc123",
          "arn": "arn:aws:ec2:us-east-1:000000000000:vpc/vpc-abc123",
          "cidrBlock": "10.0.0.0/16",
          "enableDnsHostnames": true,
          "enableDnsSupport": true
        },
        "parent": "urn:pulumi:local::cloud-networking-lab::pulumi:pulumi:Stack",
        "dependencies": []
      },
      {
        // Resource 3: Subnet A
        "urn": "urn:pulumi:local::cloud-networking-lab::aws:ec2/subnet:Subnet::cloud-networking-lab-public-a",
        "type": "aws:ec2/subnet:Subnet",
        "id": "subnet-xyz789",
        "inputs": {
          "vpcId": "vpc-abc123",
          "cidrBlock": "10.0.1.0/24",
          "availabilityZone": "us-east-1a"
        },
        "outputs": {
          "id": "subnet-xyz789",
          "vpcId": "vpc-abc123",
          "cidrBlock": "10.0.1.0/24"
        },
        "dependencies": ["urn:...::Vpc::cloud-networking-lab-vpc"]
      }
      // ... more resources
    ]
  }
}
```

---

## 🔍 **Useful State Commands**

### **Export and Save:**

```bash
# Export complete state
pulumi stack export

# Export and save to file
pulumi stack export > ~/backup-state-$(date +%Y%m%d).json

# Export with secrets visible (CAREFUL!)
pulumi stack export --show-secrets > ~/state-with-secrets.json
```

---

### **Search State with jq:**

```bash
# Find all VPCs
pulumi stack export | jq '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc")'

# Find resource by ID
pulumi stack export | jq '.deployment.resources[] | select(.id == "vpc-abc123")'

# List all resource types
pulumi stack export | jq '.deployment.resources[].type' | sort -u

# Count resources by type
pulumi stack export | jq '.deployment.resources | group_by(.type) | map({type: .[0].type, count: length})'

# Get all resource IDs
pulumi stack export | jq -r '.deployment.resources[].id' | grep -v null

# Find dependencies of a resource
pulumi stack export | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | .dependencies'
```

---

### **Compare Stacks:**

```bash
# Export both stacks
pulumi stack select local
pulumi stack export > local-state.json

pulumi stack select dev
pulumi stack export > dev-state.json

# Compare
diff local-state.json dev-state.json

# Or with colored diff
diff -u local-state.json dev-state.json | colordiff
```

---

## 🔄 **State Operations**

### **Refresh State (Sync with Reality):**

```bash
# If you made manual changes in AWS/LocalStack outside of Pulumi
pulumi refresh

# This updates state to match actual infrastructure
# Pulumi will query AWS/LocalStack and update its state
```

**When to use:**
- Made manual changes in AWS Console
- Someone else modified infrastructure
- State might be out of sync

---

### **Import State:**

```bash
# If state is lost or you want to restore from backup
pulumi stack import --file backup-state.json

# This REPLACES current state with the backup
```

---

### **Export State History:**

```bash
# Get previous versions (Pulumi Cloud only)
pulumi stack history

# Export specific version
pulumi stack export --version 5
```

---

### **Delete Stack:**

```bash
# First destroy all resources
pulumi destroy

# Then remove the stack (deletes state!)
pulumi stack rm local

# This deletes:
# - State file
# - Stack configuration
# - History
```

---

## 📊 **Find Your State Files (Local Backend)**

### **Locate State Directory:**

```bash
# Find where Pulumi stores state
ls -la ~/.pulumi/

# List all stacks
find ~/.pulumi -name "*.json" -type f

# Check size
du -sh ~/.pulumi/stacks/

# View specific stack state
cat ~/.pulumi/stacks/cloud-networking-lab/local.json | jq .
```

---

### **If State Directory Doesn't Exist:**

**This is NORMAL if you haven't deployed yet!**

```bash
# After pulumi login --local
ls ~/.pulumi/
# May only show: credentials.json

# State directory created AFTER first deployment:
pulumi up
# NOW ~/.pulumi/stacks/ exists!

# Verify
ls -la ~/.pulumi/stacks/cloud-networking-lab/
# Should show: local.json
```

---

## 🎯 **Practical Examples**

### **Example 1: Check What's Deployed**

```bash
cd ~/Cloud_Networking_Lab/pulumi

# Quick view (just outputs)
pulumi stack output

# Detailed view (all resources)
pulumi stack export | jq -r '.deployment.resources[] | "\(.type) - \(.id // "pending")"'
```

**Output:**
```
pulumi:pulumi:Stack - 
aws:ec2/vpc:Vpc - vpc-abc123
aws:ec2/subnet:Subnet - subnet-xyz789
aws:ec2/internetGateway:InternetGateway - igw-def456
aws:ec2/securityGroup:SecurityGroup - sg-ghi012
```

---

### **Example 2: Find Your VPC ID**

```bash
# Get VPC ID from state
pulumi stack export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc") | .id'

# Output: vpc-abc123

# Save to variable
VPC_ID=$(pulumi stack export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc") | .id')

# Use it
echo "My VPC ID is: $VPC_ID"
```

---

### **Example 3: Verify State Matches Reality**

```bash
# Get VPC ID from state
STATE_VPC=$(pulumi stack export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc") | .id')

# Check if it actually exists in LocalStack
awslocal ec2 describe-vpcs --vpc-ids $STATE_VPC

# If it exists, state is accurate!
# If it doesn't exist, run: pulumi refresh
```

---

### **Example 4: Backup Before Major Change**

```bash
# Before making major changes
pulumi stack export > ~/backup-before-change-$(date +%Y%m%d-%H%M).json

# Make your changes
vim __main__.py

# Deploy
pulumi up

# If something goes wrong, restore:
pulumi stack import --file ~/backup-before-change-*.json
```

---

### **Example 5: Compare Local vs Dev State**

```bash
# Export both stacks
pulumi stack select local
pulumi stack export | jq '.deployment.resources | length' > local-count.txt

pulumi stack select dev  
pulumi stack export | jq '.deployment.resources | length' > dev-count.txt

# Compare resource counts
echo "Local has $(cat local-count.txt) resources"
echo "Dev has $(cat dev-count.txt) resources"
```

---

## 🔐 **State Security**

### **What's in State?**

**Stored in state:**
- ✅ Resource IDs (vpc-abc123, subnet-xyz789)
- ✅ Resource configurations (CIDR blocks, settings)
- ✅ Dependencies between resources
- ⚠️ Secrets (encrypted with passphrase)
- ⚠️ Outputs (may contain sensitive data)

### **State Encryption:**

**Pulumi Cloud:**
- ✅ Encrypted at rest
- ✅ Encrypted in transit (HTTPS)
- ✅ Secrets are double-encrypted
- ✅ Access control with organizations

**Local Backend:**
- ⚠️ State file is plain JSON on disk
- ✅ Secrets are encrypted with your passphrase
- ⚠️ Be careful with `--show-secrets`
- ⚠️ Protect state files (chmod 600)

---

### **Protect Local State Files:**

```bash
# Set proper permissions
chmod 600 ~/.pulumi/stacks/cloud-networking-lab/*.json

# Never commit to git
echo ".pulumi/" >> .gitignore

# Backup encrypted
tar -czf state-backup.tar.gz ~/.pulumi/stacks/
gpg -c state-backup.tar.gz  # Encrypt with password
```

---

## 💡 **Best Practices**

### **DO:**

✅ **Export state before major changes**
```bash
pulumi stack export > backup-$(date +%Y%m%d).json
```

✅ **Use Pulumi Cloud for team projects**
- Automatic backups
- State locking
- Collaboration features

✅ **Run `pulumi refresh` if state might be out of sync**
```bash
pulumi refresh
```

✅ **Keep state backups (if using local backend)**
```bash
# Weekly backup
pulumi stack export > ~/pulumi-backups/backup-$(date +%Y%m%d).json
```

✅ **Use descriptive stack names**
```bash
pulumi stack init local     # Good
pulumi stack init test123   # Bad
```

---

### **DON'T:**

❌ **Edit state files manually**
- Always use `pulumi` commands
- Manual edits can corrupt state

❌ **Commit state files to git**
```bash
# Add to .gitignore
.pulumi/
*.json
*state*.json
```

❌ **Share state files with secrets unencrypted**
```bash
# Bad:
pulumi stack export --show-secrets > state.json
# email state.json

# Good:
pulumi stack export > state.json
gpg -c state.json
# email state.json.gpg
```

❌ **Delete state without destroying resources first**
```bash
# Bad:
pulumi stack rm local  # Resources still exist in AWS!

# Good:
pulumi destroy         # Remove resources
pulumi stack rm local  # Then remove state
```

❌ **Run `pulumi up` from multiple terminals simultaneously**
- Can corrupt state
- Use state locking (Pulumi Cloud) or coordinate carefully

---

## 🎯 **Quick Reference Commands**

### **View State:**
```bash
pulumi whoami -v                 # Where is state stored?
pulumi stack output              # Quick view of outputs
pulumi stack export              # Full state as JSON
pulumi stack export | jq .       # Pretty print state
pulumi stack --show-urns         # List all resources
```

### **Manage State:**
```bash
pulumi refresh                   # Sync state with reality
pulumi stack export > backup.json # Backup state
pulumi stack import --file backup.json # Restore state
pulumi stack history             # View deployment history
```

### **Switch Backends:**
```bash
pulumi logout                    # Logout from current backend
pulumi login                     # Login to Pulumi Cloud
pulumi login --local             # Login to local backend
```

### **Search State:**
```bash
# List all VPCs
pulumi stack export | jq '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc")'

# Count resources
pulumi stack export | jq '.deployment.resources | length'

# Find resource by ID
pulumi stack export | jq '.deployment.resources[] | select(.id == "vpc-123")'
```

---

## 🔍 **Troubleshooting**

### **Problem: Can't find .pulumi directory**

**Cause:** State not created yet (no deployments)

**Solution:**
```bash
# Run first deployment
pulumi up

# THEN check
ls -la ~/.pulumi/stacks/
```

---

### **Problem: State out of sync**

**Symptoms:**
- Pulumi thinks resources exist but they don't
- Resources exist but Pulumi doesn't know about them

**Solution:**
```bash
# Refresh state from actual infrastructure
pulumi refresh

# Pulumi will query AWS/LocalStack and update state
```

---

### **Problem: Corrupted state**

**Symptoms:**
- `pulumi up` fails with state errors
- Can't parse state file

**Solution:**
```bash
# Restore from backup
pulumi stack import --file backup-state.json

# Or start fresh (DANGER: loses tracking!)
pulumi stack rm local
pulumi stack init local
# Note: Existing resources in AWS won't be tracked!
```

---

### **Problem: Forgot passphrase**

**Symptoms:**
- Can't unlock secrets in state

**Solution:**
```bash
# If using Pulumi Cloud: Reset via web UI
# If using local backend: State may be unrecoverable

# Prevention:
export PULUMI_CONFIG_PASSPHRASE="your-passphrase"
# Or use passphrase file:
echo "your-passphrase" > ~/.pulumi-passphrase
export PULUMI_CONFIG_PASSPHRASE_FILE=~/.pulumi-passphrase
```

---

## 📚 **Further Reading**

- **Pulumi State Docs:** https://www.pulumi.com/docs/concepts/state/
- **Backends:** https://www.pulumi.com/docs/concepts/state/#backends
- **Import/Export:** https://www.pulumi.com/docs/cli/commands/pulumi_stack_export/
- **State Encryption:** https://www.pulumi.com/docs/concepts/secrets/

---

## 🎓 **Summary**

**Key Takeaways:**

1. **State tracks what exists** - Pulumi uses state to know what's deployed
2. **State created on first `pulumi up`** - Not during `stack init`
3. **Two backend options:**
   - Pulumi Cloud (default, recommended)
   - Local files (`~/.pulumi/stacks/`)
4. **View with `pulumi stack export`** - Shows entire state as JSON
5. **Always backup before major changes** - Easy to restore if needed
6. **Use `pulumi refresh`** - Sync state with reality
7. **Never edit state manually** - Always use Pulumi commands

---

## ✅ **Check Your State Now**

```bash
cd ~/Cloud_Networking_Lab/pulumi

# 1. Where is state stored?
pulumi whoami -v

# 2. What's deployed?
pulumi stack output

# 3. Export state
pulumi stack export | jq .

# 4. Count resources
pulumi stack export | jq '.deployment.resources | length'

# 5. Backup state
pulumi stack export > ~/state-backup-$(date +%Y%m%d).json
```

---

**Now you understand Pulumi state!** 🎉

**Remember: State = Source of Truth for what's deployed** 📊