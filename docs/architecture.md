# Architecture Overview - Cloud Networking Lab

Comprehensive architecture documentation for the AWS Cloud Networking Lab project.

---

## 🎯 **Project Architecture**

This project implements a **modern, scalable AWS network infrastructure** using Infrastructure as Code principles with Pulumi and Python.

---

## 📊 **High-Level Architecture**

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AWS Cloud (us-east-1)                        │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                    VPC (10.0.0.0/16)                            ││
│  │                                                                  ││
│  │  ┌──────────────────────────────────────────────────────────┐  ││
│  │  │              Availability Zone A (us-east-1a)            │  ││
│  │  │                                                           │  ││
│  │  │  ┌─────────────────────────────────────────────────┐    │  ││
│  │  │  │    Public Subnet A (10.0.1.0/24)               │    │  ││
│  │  │  │                                                 │    │  ││
│  │  │  │  [EC2 Instance] [EC2 Instance] ...            │    │  ││
│  │  │  │                                                 │    │  ││
│  │  │  └─────────────────────────────────────────────────┘    │  ││
│  │  └──────────────────────────────────────────────────────────┘  ││
│  │                                                                  ││
│  │  ┌──────────────────────────────────────────────────────────┐  ││
│  │  │              Availability Zone B (us-east-1b)            │  ││
│  │  │                                                           │  ││
│  │  │  ┌─────────────────────────────────────────────────┐    │  ││
│  │  │  │    Public Subnet B (10.0.2.0/24)               │    │  ││
│  │  │  │                                                 │    │  ││
│  │  │  │  [EC2 Instance] [EC2 Instance] ...            │    │  ││
│  │  │  │                                                 │    │  ││
│  │  │  └─────────────────────────────────────────────────┘    │  ││
│  │  └──────────────────────────────────────────────────────────┘  ││
│  │                                                                  ││
│  │                    ┌──────────────────┐                         ││
│  │                    │   Route Tables   │                         ││
│  │                    │  - Public RT     │                         ││
│  │                    └────────┬─────────┘                         ││
│  │                             │                                    ││
│  │                    ┌────────▼──────────┐                        ││
│  │                    │ Internet Gateway  │                        ││
│  │                    │  (Public Access)  │                        ││
│  │                    └────────┬──────────┘                        ││
│  └─────────────────────────────┼───────────────────────────────────┘│
└────────────────────────────────┼────────────────────────────────────┘
                                  │
                            ┌─────▼──────┐
                            │  Internet  │
                            └────────────┘
```

---

## 🏗️ **Component Architecture**

### **Network Layer**

```
┌─────────────────────────────────────────────────────────────┐
│                         VPC Layer                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │   Subnet   │  │   Subnet   │  │  Route     │           │
│  │   10.0.1/24│  │   10.0.2/24│  │  Tables    │           │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘           │
│        └─────────────────┼──────────────┘                   │
│                          │                                   │
│                    ┌─────▼──────┐                           │
│                    │  Internet  │                           │
│                    │  Gateway   │                           │
│                    └────────────┘                           │
└─────────────────────────────────────────────────────────────┘
```

### **Security Layer**

```
┌─────────────────────────────────────────────────────────────┐
│                      Security Layer                          │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Network ACLs (Subnet Level)                │   │
│  │  - Stateless filtering                               │   │
│  │  - Allow/Deny rules                                  │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                   │
│  ┌────────────────────────▼──────────────────────────────┐  │
│  │        Security Groups (Instance Level)               │  │
│  │  - Stateful filtering                                 │  │
│  │  - Allow rules only                                   │  │
│  │  - Applied to EC2 instances                           │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 **Infrastructure as Code Architecture**

### **Pulumi Program Flow**

```
┌────────────────────────────────────────────────────────────────┐
│                      Developer Workflow                         │
│                                                                  │
│  1. Write Python Code         ┌──────────────────┐            │
│     (declarative intent)  ────▶│  __main__.py    │            │
│                                 │  vpc.py         │            │
│                                 │  vpn.py         │            │
│                                 │  networking.py  │            │
│                                 └────────┬─────────┘            │
│                                          │                       │
│  2. Run Pulumi CLI            ┌─────────▼─────────┐            │
│     pulumi up             ────▶│  Pulumi Engine   │            │
│                                 │  - Parse code    │            │
│                                 │  - Build graph   │            │
│                                 │  - Generate plan │            │
│                                 └────────┬─────────┘            │
│                                          │                       │
│  3. Review & Approve          ┌─────────▼─────────┐            │
│     (preview changes)     ────▶│  Show Diff       │            │
│                                 │  + Create: 5     │            │
│                                 │  ~ Update: 2     │            │
│                                 │  - Delete: 0     │            │
│                                 └────────┬─────────┘            │
│                                          │                       │
│  4. Apply Changes             ┌─────────▼─────────┐            │
│     (create resources)    ────▶│  AWS API Calls   │            │
│                                 │  - CreateVpc()   │            │
│                                 │  - CreateSubnet()│            │
│                                 │  - etc.          │            │
│                                 └────────┬─────────┘            │
│                                          │                       │
│  5. Update State              ┌─────────▼─────────┐            │
│     (track resources)     ────▶│  Pulumi State    │            │
│                                 │  (local or cloud)│            │
│                                 └──────────────────┘            │
└────────────────────────────────────────────────────────────────┘
```

---

## 🎨 **Design Decisions**

### **1. Multi-AZ Design**

**Decision:** Deploy subnets across two Availability Zones

**Rationale:**
- ✅ **High Availability** - If one AZ fails, other continues
- ✅ **Fault Tolerance** - Distributed workload reduces risk
- ✅ **Best Practice** - AWS recommends multi-AZ for production
- ✅ **No Extra Cost** - AZs are free, only pay for resources

**Trade-offs:**
- Slightly more complex routing
- Need to balance load across AZs

---

### **2. Public Subnets Only (Phase 1)**

**Decision:** Start with public subnets, add private later

**Rationale:**
- ✅ **Simplicity** - Easier to learn and test
- ✅ **Cost** - No NAT Gateway required ($32/month)
- ✅ **Direct Access** - Can SSH/HTTP directly
- ✅ **Incremental** - Add private subnets in Phase 2+

**When to Add Private Subnets:**
- Running databases (security)
- Internal applications (no internet needed)
- Multi-tier architecture (web/app/db layers)

---

### **3. Infrastructure as Code (Pulumi + Python)**

**Decision:** Use Pulumi with Python instead of Terraform/CloudFormation

**Rationale:**
- ✅ **Real Language** - Python, not DSL (HCL)
- ✅ **Type Safety** - IDE support, autocomplete
- ✅ **Testable** - Use pytest directly
- ✅ **Familiar** - Leverage existing Python skills
- ✅ **Pydantic Integration** - Intent-based config
- ✅ **Modern** - Active development, good docs

**Comparison:**
```python
# Pulumi (Python)
vpc = aws.ec2.Vpc("my-vpc", 
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True
)

# vs Terraform (HCL)
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
}
```

---

### **4. Intent-Based Configuration (Pydantic)**

**Decision:** Use Pydantic models for configuration validation

**Rationale:**
- ✅ **Validation** - Catch errors before deployment
- ✅ **Type Safety** - Full IDE support
- ✅ **Documentation** - Self-documenting configs
- ✅ **Reusable** - Same pattern as Nokia SROS project
- ✅ **Testable** - Unit test intent models

**Example:**
```python
# Invalid CIDR caught immediately
vpc = VPCIntent(cidr_block="10.0.0.0/15")  # ❌ Too large!
# ValidationError: VPC CIDR must be between /16 and /28
```

---

### **5. Security Group Design**

**Decision:** Single security group with permissive rules for learning

**Rationale:**
- ✅ **Learning Focus** - Easy to test and troubleshoot
- ✅ **Flexible** - Can SSH, ping, HTTP all work
- ✅ **Temporary** - Tighten in production

**Production Changes Needed:**
- Separate SGs per tier (web, app, db)
- Restrict SSH to specific IPs
- Use bastion hosts
- Implement least privilege

---

## 🔐 **Security Architecture**

### **Current Security Posture (Phase 1)**

```
┌─────────────────────────────────────────────────────────┐
│                    Security Layers                       │
│                                                           │
│  Layer 1: VPC Isolation                                  │
│  ├─ Private network (10.0.0.0/16)                       │
│  └─ Isolated from other AWS customers                    │
│                                                           │
│  Layer 2: Subnet Segregation                             │
│  ├─ Public subnets (internet-facing)                    │
│  └─ Future: Private subnets (no direct internet)        │
│                                                           │
│  Layer 3: Security Groups                                │
│  ├─ Stateful firewall                                    │
│  ├─ Allow: SSH (22), ICMP, HTTP (80)                    │
│  └─ Default deny all inbound                             │
│                                                           │
│  Layer 4: Network ACLs (Default)                         │
│  ├─ Stateless firewall                                   │
│  └─ Allow all (can be customized)                        │
│                                                           │
│  Layer 5: IAM (Infrastructure Access)                    │
│  ├─ AWS credentials for Pulumi                           │
│  └─ Least privilege policies                             │
└─────────────────────────────────────────────────────────┘
```

### **Security Improvements for Production**

**Phase 2+:**
- [ ] Private subnets for databases/apps
- [ ] Bastion host for SSH access
- [ ] VPN for secure access (instead of public SSH)
- [ ] WAF for web application protection
- [ ] GuardDuty for threat detection
- [ ] VPC Flow Logs for network monitoring
- [ ] Secrets Manager for credentials
- [ ] KMS for encryption

---

## 📈 **Scalability Design**

### **Current Capacity**

```
VPC:        10.0.0.0/16     = 65,536 IPs
Subnet A:   10.0.1.0/24     = 256 IPs (251 usable)
Subnet B:   10.0.2.0/24     = 256 IPs (251 usable)
Total:                      = 502 usable IPs
```

**Can support:**
- ~500 EC2 instances (if all in public subnets)
- Or: 250 public + 250 private (when added)

### **Scaling Options**

**Horizontal Scaling:**
- Add more subnets (10.0.3.0/24, 10.0.4.0/24, etc.)
- Add more Availability Zones (us-east-1c, etc.)
- Use Auto Scaling Groups for EC2

**Vertical Scaling:**
- Use larger CIDR blocks (though /16 is quite large)
- Use VPC peering for additional address space
- Use Transit Gateway for multi-VPC

---

## 🔄 **High Availability Design**

### **Multi-AZ Architecture**

```
┌─────────────────────────────────────────────────────────┐
│              High Availability Strategy                  │
│                                                           │
│  us-east-1a                    us-east-1b               │
│  ┌────────────┐                ┌────────────┐           │
│  │  Subnet A  │                │  Subnet B  │           │
│  │            │                │            │           │
│  │ [Server 1] │◄──── LB ──────▶│ [Server 2] │          │
│  │ [Server 3] │                │ [Server 4] │           │
│  └────────────┘                └────────────┘           │
│                                                           │
│  If AZ-A fails ───▶ Traffic routes to AZ-B              │
│  Automatic failover with health checks                   │
└─────────────────────────────────────────────────────────┘
```

**HA Components to Add (Future):**
- Load Balancer (ALB/NLB) - Distribute traffic
- Auto Scaling Groups - Replace failed instances
- Route 53 - DNS-based failover
- RDS Multi-AZ - Database replication

---

## 💾 **State Management**

### **Pulumi State Architecture**

```
┌─────────────────────────────────────────────────────────┐
│                   State Management                       │
│                                                           │
│  Developer Machine                                       │
│  ┌──────────────────────────────────────────────┐       │
│  │  Pulumi CLI                                  │       │
│  │  ├─ Reads: Pulumi.yaml                       │       │
│  │  ├─ Reads: __main__.py                       │       │
│  │  └─ Stores: State (local or cloud)          │       │
│  └──────────────┬───────────────────────────────┘       │
│                 │                                         │
│                 ▼                                         │
│  ┌──────────────────────────────────────────────┐       │
│  │  State Storage (Choose One)                  │       │
│  │  ├─ Local: ~/.pulumi/ (single user)         │       │
│  │  ├─ Pulumi Cloud: app.pulumi.com (team)     │       │
│  │  └─ S3: s3://bucket/state (self-hosted)     │       │
│  └──────────────┬───────────────────────────────┘       │
│                 │                                         │
│                 ▼                                         │
│  ┌──────────────────────────────────────────────┐       │
│  │  State Contents                              │       │
│  │  ├─ Resource IDs (vpc-abc123, subnet-xyz)   │       │
│  │  ├─ Dependencies (subnet depends on VPC)    │       │
│  │  ├─ Outputs (vpc_id, subnet_id, etc.)       │       │
│  │  └─ Configuration (encrypted)               │       │
│  └──────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────┘
```

---

## 🧪 **Testing Architecture**

### **Test Pyramid**

```
                    ▲
                   ╱ ╲
                  ╱   ╲
                 ╱     ╲
                ╱  E2E  ╲        Fewer, slower
               ╱ Tests   ╲       (future)
              ╱───────────╲
             ╱             ╲
            ╱  Integration  ╲    Some, medium speed
           ╱     Tests       ╲   (future)
          ╱─────────────────── ╲
         ╱                      ╲
        ╱      Unit Tests        ╲  Many, fast
       ╱    (Pydantic Models)     ╲ ✅ Current
      ╱────────────────────────────╲
```

**Current:**
- ✅ Unit tests (Pydantic validation)
- ✅ 25+ test cases
- ✅ Fast (<1 second)

**Future:**
- Integration tests (moto/LocalStack)
- E2E tests (actual AWS deployment)
- Connectivity tests (VPN, routing)

---

## 📊 **Cost Architecture**

### **Current Cost Breakdown (Phase 1)**

| Component | Monthly Cost | Notes |
|-----------|--------------|-------|
| VPC | $0 | Free |
| Subnets (2) | $0 | Free |
| Internet Gateway | $0 | Free |
| Route Tables | $0 | Free |
| Security Groups | $0 | Free |
| **Total Phase 1** | **$0/month** | ✅ Free tier |

### **Future Costs (Phase 2+)**

| Component | Monthly Cost | Notes |
|-----------|--------------|-------|
| VPN Gateway | ~$36 | $0.05/hour |
| NAT Gateway | ~$32 | $0.045/hour + data |
| EC2 t2.micro | $0 | 750 hours free/month |
| VPC Flow Logs | ~$1-5 | Depends on traffic |
| CloudWatch | ~$1-3 | Depends on metrics |

---

## 🎯 **Future Architecture Evolution**

### **Phase 2: Hybrid Cloud**
```
On-Premises ←─VPN─→ AWS VPC
```
- Site-to-site VPN
- BGP routing
- Private connectivity

### **Phase 3: Multi-Tier**
```
Public Subnet:  [Load Balancer] [Bastion]
Private Subnet: [App Servers] [Databases]
```
- Separation of concerns
- Enhanced security

### **Phase 4: Multi-Region**
```
us-east-1 ←─Peering─→ us-west-2
```
- Geographic redundancy
- Disaster recovery

---

## 📚 **References**

- **AWS VPC Documentation:** https://docs.aws.amazon.com/vpc/
- **Pulumi AWS Provider:** https://www.pulumi.com/registry/packages/aws/
- **AWS Well-Architected Framework:** https://aws.amazon.com/architecture/well-architected/
- **Cloud Networking Concepts:** See `networking_concepts.md`

---

**Last Updated:** October 30, 2025  
**Version:** 1.0 (Phase 1)
