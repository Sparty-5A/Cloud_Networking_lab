# Quick Start: Deploy Web Server

Deploy a working web server in AWS that you can access from your browser!

---

## 🎯 **What You'll Deploy**

```
Your PC ←─── HTTP ───→ Internet Gateway ←─── VPC ───→ EC2 Web Server
                                                       (t2.micro, nginx)
```

**Components:**
- ✅ VPC with public subnet
- ✅ Internet Gateway
- ✅ EC2 t2.micro instance (FREE TIER!)
- ✅ Nginx web server
- ✅ Custom webpage

**Cost:** $0/month (free tier eligible for 750 hours/month)

---

## 🚀 **Deploy in 5 Minutes**

### **Step 1: Navigate and Activate**

```bash
cd ~/Cloud_Networking_Lab
source .venv/bin/activate
cd pulumi
```

### **Step 2: Configure**

```bash
# Initialize stack (if not already done)
pulumi stack init dev

# Set configuration
pulumi config set aws:region us-east-1
pulumi config set vpc_cidr 10.0.0.0/16
pulumi config set enable_vpn false
pulumi config set enable_flow_logs false
pulumi config set enable_web_server true  # ← Enable web server!
```

### **Step 3: Preview**

```bash
pulumi preview
```

**You should see:**
```
Previewing update (dev):
     Type                          Name                          Plan
 +   pulumi:pulumi:Stack           cloud-networking-lab-dev      create
 +   ├─ aws:ec2:Vpc               cloud-networking-lab-vpc       create
 +   ├─ aws:ec2:InternetGateway   cloud-networking-lab-igw       create
 +   ├─ aws:ec2:Subnet            cloud-networking-lab-public-a  create
 +   ├─ aws:ec2:Subnet            cloud-networking-lab-public-b  create
 +   ├─ aws:ec2:RouteTable        cloud-networking-lab-public-rt create
 +   ├─ aws:ec2:Route             cloud-networking-lab-public-route create
 +   ├─ aws:ec2:RouteTableAssociation  ...                       create
 +   ├─ aws:ec2:SecurityGroup     cloud-networking-lab-default-sg create
 +   └─ aws:ec2:Instance          cloud-networking-lab-web-server create ← Your server!

Resources:
    + 11 to create
```

### **Step 4: Deploy!**

```bash
pulumi up
```

**Select "yes" when prompted**

**Wait 2-3 minutes...**

---

## 🎉 **Access Your Website**

### **Get the URL:**

```bash
pulumi stack output web_server_url
```

**Example output:**
```
http://54.123.45.67
```

### **Open in Browser:**

```bash
# Copy the URL and paste in your browser
# Or use curl:
curl $(pulumi stack output web_server_url)
```

**You should see:**
- 🎉 Beautiful gradient background
- ✓ "Cloud Networking Lab" title
- Server information (hostname, IP, AZ, instance ID)
- What you built list
- Technologies used

---

## 📊 **View All Outputs**

```bash
pulumi stack output
```

**Example:**
```
Current stack outputs (17):
    OUTPUT                     VALUE
    vpc_id                     vpc-abc123
    vpc_cidr                   10.0.0.0/16
    public_subnet_a_id         subnet-xyz789
    internet_gateway_id        igw-def456
    web_server_id              i-0123456789abcdef0
    web_server_public_ip       54.123.45.67
    web_server_private_ip      10.0.1.50
    web_server_url             http://54.123.45.67
    deployment_message         ✓ VPC deployed successfully. Web server enabled.
```

---

## 🔍 **Verify in AWS Console**

### **EC2 Dashboard:**
https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Instances:

**You should see:**
- Instance: `cloud-networking-lab-web-server`
- State: Running (green)
- Instance type: t2.micro
- Public IP: 54.123.45.67
- Security group: allows HTTP (80)

### **Connect via SSH (optional):**

```bash
# Get the public IP
WEB_IP=$(pulumi stack output web_server_public_ip)

# SSH into the server (if you have keypair configured)
ssh ec2-user@$WEB_IP

# Once inside:
curl localhost  # Test nginx locally
systemctl status nginx  # Check nginx status
tail /var/log/nginx/access.log  # See access logs
```

---

## 🧪 **Test Everything Works**

### **From Your Browser:**
```
http://54.123.45.67
↓
Should show beautiful webpage ✓
```

### **From Command Line:**
```bash
# Test HTTP
curl -I $(pulumi stack output web_server_url)
# Should return: HTTP/1.1 200 OK

# Test with full content
curl $(pulumi stack output web_server_url)
# Should return: HTML content

# Test from different location (phone/other computer)
# Should work from anywhere! (public IP)
```

---

## 🎨 **What Just Happened?**

### **Behind the Scenes:**

1. **Pulumi created VPC infrastructure** (VPC, subnets, IGW, routes)
2. **Launched EC2 instance** (t2.micro with Amazon Linux 2023)
3. **User data script ran** on first boot:
   - Updated system packages
   - Installed nginx
   - Created custom HTML page
   - Started nginx service
   - Disabled firewall
4. **Security group allowed** HTTP (port 80) from internet
5. **Instance got public IP** via Internet Gateway
6. **You accessed it** from your browser!

### **The Flow:**

```
Your Browser
    ↓ (HTTP request)
Internet
    ↓
AWS Internet Gateway
    ↓
VPC Route Table (0.0.0.0/0 → IGW)
    ↓
Public Subnet (10.0.1.0/24)
    ↓
Security Group (allow port 80)
    ↓
EC2 Instance (10.0.1.50)
    ↓
Nginx (port 80)
    ↓
HTML Page
    ↑ (HTTP response)
Back to Your Browser!
```

---

## 💰 **Cost Tracking**

**Free Tier Status:**
```
✅ VPC, Subnets, IGW, Route Tables: $0 (always free)
✅ t2.micro: 750 hours/month free (first 12 months)
✅ Security Groups: $0 (always free)
✅ Data transfer: 1GB/month free (should be enough)

Total: $0/month ✓
```

**After Free Tier (or if exceeded):**
```
⚠️ t2.micro: ~$8.50/month (if running 24/7)
⚠️ Data transfer: $0.09/GB (outbound)
```

**Best Practice:** Destroy when done testing!

---

## 🧹 **Clean Up**

### **Stop (but keep resources):**
```bash
# Stop instance (no charge when stopped)
aws ec2 stop-instances --instance-ids $(pulumi stack output web_server_id)
```

### **Destroy Everything:**
```bash
pulumi destroy
```

**This will delete:**
- ✅ EC2 instance
- ✅ VPC
- ✅ Subnets
- ✅ Internet Gateway
- ✅ Route Tables
- ✅ Security Groups
- ✅ Everything! 

**Cost after destruction:** $0/month

---

## 🔧 **Troubleshooting**

### **Can't access webpage?**

**1. Check instance is running:**
```bash
aws ec2 describe-instances \
  --instance-ids $(pulumi stack output web_server_id) \
  --query 'Reservations[0].Instances[0].State.Name'
# Should be: "running"
```

**2. Check security group:**
```bash
aws ec2 describe-security-groups \
  --group-ids $(pulumi stack output default_security_group_id) \
  --query 'SecurityGroups[0].IpPermissions[?FromPort==`80`]'
# Should show port 80 allowed from 0.0.0.0/0
```

**3. Wait for user data to complete:**
```bash
# It takes 2-3 minutes for nginx to install and start
# Check status:
ssh ec2-user@$(pulumi stack output web_server_public_ip)
sudo systemctl status nginx
```

**4. Check nginx logs:**
```bash
ssh ec2-user@$(pulumi stack output web_server_public_ip)
sudo tail -f /var/log/nginx/error.log
```

---

## 🎓 **What You Learned**

By deploying this web server, you now understand:

1. ✅ **Infrastructure as Code** - Defined servers in Python
2. ✅ **AWS Networking** - VPC, subnets, IGW, routing
3. ✅ **Security Groups** - Allow HTTP traffic
4. ✅ **EC2 Basics** - Launch instances with user data
5. ✅ **User Data Scripts** - Automate server configuration
6. ✅ **End-to-End Flow** - Request → IGW → EC2 → Response
7. ✅ **Public vs Private** - Instance has both IPs

---

## 🚀 **Next Steps**

Now that you have a working web server:

### **Phase 1.5 Enhancements:**
- [ ] Add second web server in AZ-B (high availability)
- [ ] Add Application Load Balancer
- [ ] Use Let's Encrypt for HTTPS
- [ ] Add CloudWatch monitoring

### **Phase 2: VPN Connectivity**
- [ ] Set up on-prem router (Ubuntu VM)
- [ ] Enable VPN Gateway in AWS
- [ ] Connect home network to AWS
- [ ] Private access to resources

### **Phase 3: Database Tier**
- [ ] Add private subnets
- [ ] Deploy RDS database
- [ ] Connect web server to database
- [ ] Multi-tier architecture

---

## 📸 **Portfolio Screenshot Ideas**

Take screenshots of:
1. ✅ Your custom webpage in browser
2. ✅ AWS EC2 Console showing running instance
3. ✅ `pulumi stack output` command
4. ✅ Network diagram (draw.io)
5. ✅ Your code in PyCharm

---

## 🎉 **Congratulations!**

You just:
- ✅ Deployed real cloud infrastructure
- ✅ Launched a working web server
- ✅ Made it accessible from the internet
- ✅ All using Infrastructure as Code
- ✅ $0 cost (free tier)!

**This is exactly what professional cloud engineers do!** 🚀

---

**Last Updated:** October 30, 2025  
**Deployment Time:** ~5 minutes  
**Cost:** $0/month (free tier)
