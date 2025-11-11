# Quick Start - Python Only

**Simple Python + Pulumi workflow - No shell scripts!**

---

## 🎯 **Core Concept**

Use **Pulumi stacks** to switch between environments:
- `local` stack → LocalStack (development)
- `dev` stack → Real AWS (validation)

**Everything else is just Pulumi commands!**

---

## 🚀 **Simplest Workflow**

### **1. Start LocalStack**

```bash
docker compose up -d
```

### **2. Deploy to LocalStack**

```bash
cd pulumi

# Select local stack (or create if first time)
pulumi stack select local --create

# Deploy!
pulumi up
```

**That's it!** No scripts needed! 🎉

---

## 📊 **Complete Example**

```bash
# Start your day
cd ~/Cloud_Networking_Lab
docker compose up -d

# Go to Pulumi directory (do all work here)
cd pulumi

# Select LocalStack environment
pulumi stack select local

# See what will change
pulumi preview

# Deploy
pulumi up

# View what was created
pulumi stack output

# Make a change
vim __main__.py

# Deploy change (super fast on LocalStack!)
pulumi up

# Clean up
pulumi destroy

# End of day
cd ..
docker compose down
```

---

## 🔄 **Switching Environments**

```bash
cd pulumi

# Work on LocalStack
pulumi stack select local
pulumi up

# Validate on AWS
pulumi stack select dev
pulumi up

# Destroy AWS (important!)
pulumi destroy

# Back to LocalStack
pulumi stack select local
```

---

## ⚙️ **Configuration**

Each stack has its own config file:

**LocalStack:** `Pulumi.local.yaml`
```yaml
config:
  aws:region: us-east-1
  aws:endpoints:
    - ec2: http://localhost:4566
    - iam: http://localhost:4566
    # etc...
  cloud-networking-lab:vpc_cidr: 10.0.0.0/16
  cloud-networking-lab:enable_web_server: "true"
```

**AWS:** `Pulumi.dev.yaml`
```yaml
config:
  aws:region: us-east-1
  cloud-networking-lab:vpc_cidr: 10.0.0.0/16
  cloud-networking-lab:enable_web_server: "true"
```

**Change config:**
```bash
cd pulumi
pulumi config set vpc_cidr 10.10.0.0/16
pulumi config set enable_web_server true
```

---

## 🎯 **The Key Commands**

You only need these:

```bash
# Select environment
pulumi stack select local    # or: dev

# Preview changes
pulumi preview

# Deploy
pulumi up

# Destroy
pulumi destroy

# View outputs
pulumi stack output
```

**That's your entire workflow!** 🎉

---

## 📝 **Optional: Python Script**

If you want a helper script, use `deploy.py`:

```bash
# Deploy to LocalStack (starts it automatically)
python deploy.py deploy --stack local --start-localstack

# Deploy to AWS
python deploy.py deploy --stack dev

# Destroy
python deploy.py destroy --stack local
```

But **you don't need it** - raw Pulumi commands work great!

---

## ✅ **Recommended Approach**

**For daily work:**
```bash
cd pulumi
pulumi stack select local
pulumi up
```

**For validation:**
```bash
pulumi stack select dev
pulumi up
# Take screenshots
pulumi destroy  # ← Don't forget!
```

**Simple, clean, pure Python + Pulumi!** 🐍

---

## 🎓 **What You're Actually Doing**

When you run `pulumi up`:

1. Pulumi reads `__main__.py` (your Python code)
2. Executes your Python infrastructure code
3. Determines what AWS resources to create
4. Talks to AWS (or LocalStack if local stack)
5. Creates/updates resources
6. Saves state

**It's all Python!** Your infrastructure IS Python code! 🎯

---

## 💡 **Pro Tips**

```bash
# Work faster
pulumi up --yes              # Skip confirmation

# See detailed diff
pulumi up --diff

# Refresh state from cloud
pulumi refresh

# See what's deployed
pulumi stack export

# List all stacks
pulumi stack ls
```

---

## 🚀 **Get Started Right Now**

```bash
cd ~/Cloud_Networking_Lab
docker compose up -d
cd pulumi
pulumi stack select local --create
pulumi up
```

**Done! You're deploying infrastructure with pure Python!** ✨

---

**Keep it simple. Use Pulumi. Everything is Python.** 🐍