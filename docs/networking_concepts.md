# Cloud Networking Concepts

A comprehensive guide to cloud networking fundamentals, specifically focused on AWS and how they differ from traditional on-premises networking.

---

## 🌐 **Cloud Networking vs Traditional Networking**

### **Traditional On-Premises Network**

```
┌─────────────────────────────────────────────────────────┐
│                Physical Data Center                      │
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ Physical │  │ Physical │  │ Physical │             │
│  │ Router   │  │ Switch   │  │ Firewall │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
│       │             │             │                      │
│  ┌────▼─────────────▼─────────────▼─────┐              │
│  │         Physical Cables               │              │
│  └───────────────────────────────────────┘              │
│                                                           │
│  Characteristics:                                        │
│  • Buy/rack physical hardware                            │
│  • Manual cable connections                              │
│  • Fixed capacity                                        │
│  • Weeks to provision                                    │
│  • High upfront cost                                     │
└─────────────────────────────────────────────────────────┘
```

### **Cloud Network (AWS)**

```
┌─────────────────────────────────────────────────────────┐
│                  AWS Cloud (Virtual)                     │
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ Virtual  │  │ Virtual  │  │ Virtual  │             │
│  │ Router   │  │ Switch   │  │ Firewall │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
│       │             │             │                      │
│  ┌────▼─────────────▼─────────────▼─────┐              │
│  │      Software-Defined Network         │              │
│  └───────────────────────────────────────┘              │
│                                                           │
│  Characteristics:                                        │
│  • API calls create resources                            │
│  • No physical hardware                                  │
│  • Elastic capacity                                      │
│  • Seconds to provision                                  │
│  • Pay-as-you-go                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🏗️ **Core Cloud Networking Concepts**

### **1. Virtual Private Cloud (VPC)**

**What it is:** Your own isolated network in the cloud

**Think of it as:** 
- Your own private data center
- A walled garden in AWS's infrastructure
- A logically isolated section of AWS

**Key Characteristics:**
```
┌─────────────────────────────────────────────────────────┐
│                    VPC: 10.0.0.0/16                      │
│                                                           │
│  Your Private Network Space                              │
│  • 65,536 IP addresses available                         │
│  • Completely isolated from other AWS customers          │
│  • You control all routing and security                  │
│  • Can connect to: Internet, VPN, other VPCs            │
│                                                           │
│  Default Resources:                                      │
│  ✓ Main route table                                     │
│  ✓ Default network ACL                                  │
│  ✓ Default security group                               │
└─────────────────────────────────────────────────────────┘
```

**Real-World Analogy:**
```
VPC = Your Office Building
├─ You own/control it
├─ Choose who can enter
├─ Decide internal layout
└─ Connect to outside world (or not)
```

**Traditional Equivalent:**
- On-prem: Your entire data center network
- Networking: A VLAN (but much more powerful)

---

### **2. Subnets**

**What it is:** Subdivisions of your VPC in specific Availability Zones

**Think of it as:**
- Floors in your office building
- Network segments for different purposes
- Smaller IP address ranges within your VPC

**Key Characteristics:**
```
VPC: 10.0.0.0/16 (65,536 IPs)
├─ Subnet A: 10.0.1.0/24 (256 IPs) → us-east-1a
├─ Subnet B: 10.0.2.0/24 (256 IPs) → us-east-1b
├─ Subnet C: 10.0.3.0/24 (256 IPs) → us-east-1a
└─ Subnet D: 10.0.4.0/24 (256 IPs) → us-east-1b

Rules:
• Must be within VPC CIDR range
• Cannot overlap with other subnets
• Tied to ONE Availability Zone
• Can be public or private
```

**Types of Subnets:**

**Public Subnet:**
```
┌────────────────────────────────────┐
│        Public Subnet                │
│                                     │
│  • Has route to Internet Gateway   │
│  • Resources get public IPs        │
│  • Direct internet access          │
│  • Use for: web servers, bastion   │
│                                     │
│  Example Route Table:               │
│  10.0.0.0/16  → local              │
│  0.0.0.0/0    → Internet Gateway   │
└────────────────────────────────────┘
```

**Private Subnet:**
```
┌────────────────────────────────────┐
│       Private Subnet                │
│                                     │
│  • No route to Internet Gateway    │
│  • No public IPs                   │
│  • Internet via NAT Gateway        │
│  • Use for: databases, app servers │
│                                     │
│  Example Route Table:               │
│  10.0.0.0/16  → local              │
│  0.0.0.0/0    → NAT Gateway        │
└────────────────────────────────────┘
```

**Traditional Equivalent:**
- On-prem: VLANs (VLAN 10, VLAN 20, etc.)
- But subnets are tied to physical locations (AZs)

---

### **3. Availability Zones (AZs)**

**What it is:** Physically separate data centers within a region

**Think of it as:**
- Different buildings in the same city
- Isolated failure domains
- Connected by high-speed private networks

**Key Characteristics:**
```
┌─────────────────────────────────────────────────────────┐
│                  AWS Region: us-east-1                   │
│                   (Northern Virginia)                    │
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   us-east-1a │  │   us-east-1b │  │   us-east-1c │ │
│  │              │  │              │  │              │ │
│  │  Data Center │  │  Data Center │  │  Data Center │ │
│  │  Building A  │  │  Building B  │  │  Building C  │ │
│  │              │  │              │  │              │ │
│  │  [Servers]   │  │  [Servers]   │  │  [Servers]   │ │
│  │  [Storage]   │  │  [Storage]   │  │  [Storage]   │ │
│  │  [Network]   │  │  [Network]   │  │  [Network]   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│         │                 │                 │           │
│         └─────────────────┴─────────────────┘           │
│              High-speed fiber links                      │
│            (<2ms latency between AZs)                    │
└─────────────────────────────────────────────────────────┘
```

**Why Multiple AZs Matter:**
```
Scenario: Power outage in us-east-1a

Single AZ Deployment:
┌────────────────┐
│   us-east-1a   │  ← OUTAGE!
│   [Server]     │  ← DOWN!
└────────────────┘
Result: Your service is DOWN ❌

Multi-AZ Deployment:
┌────────────────┐  ┌────────────────┐
│   us-east-1a   │  │   us-east-1b   │
│   [Server]     │  │   [Server]     │ ← Still running!
└────────────────┘  └────────────────┘
     OUTAGE!            WORKING! ✅
Result: Your service stays UP ✅
```

**Best Practice:**
- Always deploy across at least 2 AZs
- Distribute load evenly
- Use for high availability

**Traditional Equivalent:**
- On-prem: Having data centers in different cities
- Or: Having redundant equipment in different racks

---

### **4. Internet Gateway (IGW)**

**What it is:** The door between your VPC and the public internet

**Think of it as:**
- Main entrance to your building
- Highway on-ramp
- The "front door" for internet traffic

**How it Works:**
```
┌─────────────────────────────────────────────────────────┐
│                    The Internet                          │
│                    (0.0.0.0/0)                          │
└────────────────────┬────────────────────────────────────┘
                     │
              ┌──────▼──────┐
              │   Internet  │  ← ONE per VPC
              │   Gateway   │  ← AWS managed
              └──────┬──────┘  ← Highly available
                     │
┌────────────────────┼────────────────────────────────────┐
│                    ▼                                     │
│              VPC (10.0.0.0/16)                          │
│                                                          │
│  ┌─────────────┐              ┌─────────────┐          │
│  │  Public     │              │  Private    │          │
│  │  Subnet     │              │  Subnet     │          │
│  │             │              │             │          │
│  │ [Web Server]│              │ [Database]  │          │
│  │  (has IGW   │              │  (no IGW    │          │
│  │   route)    │              │   route)    │          │
│  └─────────────┘              └─────────────┘          │
│       ↑                              ↑                   │
│       │                              │                   │
│   Can reach                     Cannot reach             │
│   internet                      internet directly        │
└─────────────────────────────────────────────────────────┘
```

**What IGW Does:**
1. **Performs NAT** for instances with public IPs
2. **Routes traffic** between VPC and internet
3. **Scales automatically** (no bandwidth limit)
4. **Highly available** (redundant by design)

**Route Table Entry:**
```
Destination        Target
10.0.0.0/16    →  local          (stay in VPC)
0.0.0.0/0      →  igw-xxxxx      (everything else → internet)
```

**Traditional Equivalent:**
- On-prem: Border router with public IP
- Or: Firewall with internet connection

---

### **5. NAT Gateway**

**What it is:** Allows private subnet resources to access internet (outbound only)

**Think of it as:**
- One-way door (exit only, no entrance)
- Proxy for private resources
- Translator for private IPs

**How it Works:**
```
┌─────────────────────────────────────────────────────────┐
│                    The Internet                          │
└────────────────────┬────────────────────────────────────┘
                     │
              ┌──────▼──────┐
              │   Internet  │
              │   Gateway   │
              └──────┬──────┘
                     │
┌────────────────────┼────────────────────────────────────┐
│              VPC   │                                     │
│                    │                                     │
│  ┌─────────────────▼────────┐      ┌──────────────┐    │
│  │    Public Subnet         │      │   Private    │    │
│  │                          │      │   Subnet     │    │
│  │  ┌────────────────┐      │      │              │    │
│  │  │  NAT Gateway   │◄─────┼──────│ [Database]  │    │
│  │  │  (managed)     │      │      │              │    │
│  │  └────────────────┘      │      │  Needs to    │    │
│  │                          │      │  download    │    │
│  │  Has public IP:          │      │  updates     │    │
│  │  54.123.45.67            │      │              │    │
│  └──────────────────────────┘      └──────────────┘    │
│                                                          │
│  Private Subnet Route Table:                            │
│  10.0.0.0/16  → local                                   │
│  0.0.0.0/0    → nat-xxxxx                               │
└─────────────────────────────────────────────────────────┘

Traffic Flow:
1. Database (10.0.2.50) wants to reach internet
2. Sends to NAT Gateway via route table
3. NAT translates 10.0.2.50 → 54.123.45.67
4. Internet sees request from 54.123.45.67
5. Response comes back to NAT
6. NAT translates back to 10.0.2.50
7. Database receives response

✅ Outbound works (database can download updates)
❌ Inbound blocked (internet cannot initiate connection)
```

**NAT Gateway vs NAT Instance:**

| Feature | NAT Gateway | NAT Instance |
|---------|-------------|--------------|
| **Managed by** | AWS | You |
| **Availability** | Highly available in AZ | Single instance |
| **Bandwidth** | Up to 100 Gbps | Instance type limit |
| **Maintenance** | None required | You patch/manage |
| **Cost** | ~$32/month + data | Instance cost |
| **Recommendation** | ✅ Use this | ❌ Legacy option |

**Traditional Equivalent:**
- On-prem: Firewall doing source NAT
- Or: Proxy server for internet access

---

### **6. Route Tables**

**What it is:** Rules that determine where network traffic goes

**Think of it as:**
- GPS for your network
- Traffic signs/directions
- Routing map

**How Routing Works:**
```
┌─────────────────────────────────────────────────────────┐
│                    Route Table                           │
│                                                           │
│  Destination        Target           Priority            │
│  ────────────────────────────────────────────────        │
│  10.0.0.0/16    →  local             Most specific ✓    │
│  0.0.0.0/0      →  igw-xxxxx         Least specific      │
│                                                           │
│  Logic:                                                   │
│  1. Packet destined for 10.0.5.100                       │
│     → Matches 10.0.0.0/16 → Send to "local"             │
│  2. Packet destined for 8.8.8.8                          │
│     → Matches 0.0.0.0/0 → Send to Internet Gateway      │
└─────────────────────────────────────────────────────────┘
```

**Route Table Types:**

**Main Route Table:**
```
• Created automatically with VPC
• Default for all subnets (unless explicitly associated)
• Usually kept simple/secure
• Example: Only local routes
```

**Custom Route Tables:**
```
• Created by you
• Explicitly associated with subnets
• Can have custom routes
• Example: Routes to IGW, NAT, VPN
```

**Example Scenario:**
```
VPC: 10.0.0.0/16

Public Route Table (for public subnets):
  10.0.0.0/16  → local
  0.0.0.0/0    → igw-xxxxx

Private Route Table (for private subnets):
  10.0.0.0/16  → local
  0.0.0.0/0    → nat-xxxxx

Subnet Associations:
  Public Subnet A  → Public Route Table
  Public Subnet B  → Public Route Table
  Private Subnet A → Private Route Table
  Private Subnet B → Private Route Table
```

**Traditional Equivalent:**
- On-prem: Routing table on router
- Commands: `show ip route`, `ip route add`

---

### **7. Security Groups**

**What it is:** Virtual firewall for EC2 instances (stateful)

**Think of it as:**
- Bouncer at a nightclub
- Personal bodyguard for each instance
- Instance-level firewall

**Key Characteristics:**
```
┌─────────────────────────────────────────────────────────┐
│               Security Group (Stateful)                  │
│                                                           │
│  Operates at: Instance level (attached to ENI)          │
│  Type: Stateful (return traffic automatically allowed)  │
│  Default: Deny all inbound, allow all outbound          │
│  Rules: Allow only (no deny rules)                      │
│                                                           │
│  Example Rules:                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Inbound Rules                                    │   │
│  │ ────────────────────────────────────────────── │   │
│  │ Type    Protocol  Port   Source                 │   │
│  │ SSH     TCP       22     0.0.0.0/0              │   │
│  │ HTTP    TCP       80     0.0.0.0/0              │   │
│  │ HTTPS   TCP       443    0.0.0.0/0              │   │
│  │ MySQL   TCP       3306   sg-app-servers         │   │
│  └─────────────────────────────────────────────────┘   │
│                                                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Outbound Rules                                   │   │
│  │ ────────────────────────────────────────────── │   │
│  │ Type    Protocol  Port   Destination            │   │
│  │ All     All       All    0.0.0.0/0              │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Stateful Behavior:**
```
Scenario: You SSH into an instance

Outbound Connection:
  Your PC (1.2.3.4:54321) → AWS Instance (10.0.1.50:22)
  ✓ Allowed by inbound rule: TCP 22 from 0.0.0.0/0

Return Traffic:
  AWS Instance (10.0.1.50:22) → Your PC (1.2.3.4:54321)
  ✓ Automatically allowed (stateful tracking)
  ✓ No explicit outbound rule needed!

This is what "stateful" means:
  - Firewall remembers the connection
  - Return traffic automatically allowed
  - Don't need bidirectional rules
```

**Security Group Chaining:**
```
┌──────────────────┐
│  Web Server SG   │
│  Allow:          │
│  - HTTP from all │
│  - MySQL to      │──┐
│    DB SG         │  │
└──────────────────┘  │
                       │ Reference
                       │ by SG ID
┌──────────────────┐  │
│  Database SG     │◄─┘
│  Allow:          │
│  - MySQL from    │
│    Web Server SG │
└──────────────────┘

Benefits:
• No hardcoded IPs
• Scales automatically
• Follows instances
```

**Traditional Equivalent:**
- On-prem: Host-based firewall (iptables, Windows Firewall)
- Or: ACLs on switch ports

---

### **8. Network ACLs (NACLs)**

**What it is:** Stateless firewall at subnet level

**Think of it as:**
- Gate guard for entire neighborhood
- Subnet-level firewall
- Coarse-grained control

**Key Characteristics:**
```
┌─────────────────────────────────────────────────────────┐
│            Network ACL (Stateless)                       │
│                                                           │
│  Operates at: Subnet level                              │
│  Type: Stateless (must allow both directions)           │
│  Default: Allow all traffic                             │
│  Rules: Both allow AND deny                             │
│  Processing: Rules evaluated in number order            │
│                                                           │
│  Example Rules:                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Inbound Rules                                    │   │
│  │ ────────────────────────────────────────────── │   │
│  │ Rule #  Type     Protocol  Port   Source   Action│  │
│  │ 100     HTTP     TCP       80     0.0.0.0/0  ALLOW│ │
│  │ 110     HTTPS    TCP       443    0.0.0.0/0  ALLOW│ │
│  │ 120     SSH      TCP       22     1.2.3.0/24 ALLOW│ │
│  │ 130     Bad IP   All       All    5.6.7.8/32 DENY │ │
│  │ *       All      All       All    0.0.0.0/0  DENY │ │
│  └─────────────────────────────────────────────────┘   │
│                                                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Outbound Rules (MUST explicitly allow return!)  │   │
│  │ ────────────────────────────────────────────── │   │
│  │ Rule #  Type     Protocol  Port   Dest     Action│  │
│  │ 100     Ephem    TCP     1024-65535 0.0.0.0/0 ALLOW│ │
│  │ *       All      All       All    0.0.0.0/0  DENY │ │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Stateless Behavior:**
```
Scenario: HTTP request to web server

Inbound Request:
  Client (1.2.3.4:54321) → Server (10.0.1.50:80)
  ✓ NACL Rule 100: Allow TCP 80 inbound

Return Traffic:
  Server (10.0.1.50:80) → Client (1.2.3.4:54321)
  ? NACL must have explicit outbound rule!
  ✓ NACL Rule 100: Allow TCP 1024-65535 outbound
    (ephemeral ports for return traffic)

This is what "stateless" means:
  - Firewall doesn't remember connections
  - Must explicitly allow both directions
  - Need to understand TCP/ephemeral ports
```

**Security Groups vs NACLs:**

| Feature | Security Group | Network ACL |
|---------|----------------|-------------|
| **Level** | Instance (ENI) | Subnet |
| **State** | Stateful | Stateless |
| **Rules** | Allow only | Allow AND deny |
| **Return traffic** | Automatic | Must explicit |
| **Processing** | All rules | Number order |
| **Use case** | Primary security | Backup/subnet-level |
| **Recommendation** | ✅ Main defense | Supplement only |

**Best Practice:**
```
Defense in Depth:

Layer 1: NACL (Subnet level)
  ├─ Broad rules
  ├─ Block known bad IPs
  └─ Allow general traffic types

Layer 2: Security Group (Instance level)
  ├─ Specific rules
  ├─ Application-aware
  └─ Principle of least privilege

Result: Multiple layers of security
```

**Traditional Equivalent:**
- On-prem: Router/switch ACLs
- Commands: `access-list`, `ip access-group`

---

## 🔐 **Cloud Security Concepts**

### **Defense in Depth**

```
┌─────────────────────────────────────────────────────────┐
│                    Security Layers                       │
│                                                           │
│  Internet                                                │
│    ↓                                                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Layer 1: Network ACL (Subnet boundary)          │   │
│  │          • Stateless filtering                   │   │
│  │          • Coarse rules                          │   │
│  └────────────────────┬────────────────────────────┘   │
│                       ↓                                   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Layer 2: Security Group (Instance level)        │   │
│  │          • Stateful filtering                    │   │
│  │          • Fine-grained rules                    │   │
│  └────────────────────┬────────────────────────────┘   │
│                       ↓                                   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Layer 3: IAM (Who can access AWS resources)     │   │
│  │          • Identity-based policies               │   │
│  │          • Role-based access                     │   │
│  └────────────────────┬────────────────────────────┘   │
│                       ↓                                   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Layer 4: Application (Instance firewall/auth)   │   │
│  │          • OS firewall (iptables)                │   │
│  │          • Application authentication            │   │
│  └─────────────────────────────────────────────────┘   │
│                                                           │
│  Each layer provides independent security                │
│  Breach one layer? Still have others!                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🌍 **Hybrid Cloud Connectivity**

### **VPN Connection**

**What it is:** Encrypted tunnel between on-premises and AWS

```
┌─────────────────────────────────────────────────────────┐
│              Hybrid Cloud with VPN                       │
│                                                           │
│  On-Premises                      AWS VPC                │
│  ┌────────────────┐              ┌────────────────┐    │
│  │                │   IPSec      │                │    │
│  │  Your Router   │◄────VPN─────►│  VPN Gateway   │    │
│  │  (CGW)         │   Tunnel     │  (VGW)         │    │
│  │                │              │                │    │
│  │  192.168.0/16  │              │  10.0.0.0/16   │    │
│  └────────────────┘              └────────────────┘    │
│                                                           │
│  Characteristics:                                        │
│  • Encrypted (IPSec)                                     │
│  • Over public internet                                  │
│  • Cost: ~$36/month (VPN Gateway)                       │
│  • Latency: Varies (internet dependent)                 │
│  • Bandwidth: Up to 1.25 Gbps per tunnel               │
│  • Redundancy: 2 tunnels per connection                 │
└─────────────────────────────────────────────────────────┘
```

### **Direct Connect**

**What it is:** Dedicated physical connection to AWS

```
┌─────────────────────────────────────────────────────────┐
│          Hybrid Cloud with Direct Connect                │
│                                                           │
│  On-Premises          Direct Connect         AWS VPC    │
│  ┌──────────┐        Location      ┌──────────────┐    │
│  │          │  Fiber  ┌────────┐   │              │    │
│  │  Router  │◄───────►│  AWS   │◄──│  Virtual     │    │
│  │          │         │  Cage  │   │  Private     │    │
│  │          │         └────────┘   │  Gateway     │    │
│  └──────────┘                      └──────────────┘    │
│                                                           │
│  Characteristics:                                        │
│  • Dedicated fiber                                       │
│  • Private connection (not internet)                     │
│  • Cost: $300-500+/month (1 Gbps)                       │
│  • Latency: Consistent, low                             │
│  • Bandwidth: Up to 100 Gbps                            │
│  • Best for: Production, high bandwidth                 │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 **Cloud Networking Best Practices**

### **1. Design for High Availability**

```
✅ DO: Multi-AZ deployment
┌──────────┐  ┌──────────┐
│  AZ-A    │  │  AZ-B    │
│ [Server] │  │ [Server] │
└──────────┘  └──────────┘
Both zones active, load balanced

❌ DON'T: Single AZ
┌──────────┐
│  AZ-A    │
│ [Server] │
└──────────┘
Single point of failure
```

### **2. Separate Public and Private Resources**

```
✅ DO: Multi-tier architecture
┌─────────────────┐
│ Public Subnet   │
│  [Web Servers]  │
└────────┬────────┘
         │
┌────────▼────────┐
│ Private Subnet  │
│  [Databases]    │
└─────────────────┘

❌ DON'T: Everything public
┌─────────────────┐
│ Public Subnet   │
│  [Web Servers]  │
│  [Databases] ←── Exposed!
└─────────────────┘
```

### **3. Use Security Groups Properly**

```
✅ DO: Least privilege
Web SG: Allow 80, 443 from 0.0.0.0/0
App SG: Allow 8080 from Web SG only
DB SG: Allow 3306 from App SG only

❌ DON'T: Open everything
All SG: Allow 0-65535 from 0.0.0.0/0
```

### **4. Plan IP Address Space**

```
✅ DO: Leave room to grow
VPC:         10.0.0.0/16   (65,536 IPs)
Public-A:    10.0.1.0/24   (256 IPs)
Public-B:    10.0.2.0/24   (256 IPs)
Private-A:   10.0.10.0/24  (256 IPs)
Private-B:   10.0.11.0/24  (256 IPs)
Reserved:    10.0.3-9.*    (for future)

❌ DON'T: Use all space immediately
VPC:         10.0.0.0/24   (256 IPs total!)
No room for growth
```

### **5. Monitor and Log**

```
✅ DO: Enable monitoring
• VPC Flow Logs → CloudWatch
• CloudTrail → API calls
• GuardDuty → Threat detection
• Config → Compliance

❌ DON'T: Deploy blind
No visibility into traffic or changes
```

---

## 🎓 **Key Takeaways**

**Cloud networking is different:**
- ✅ Everything is software-defined
- ✅ Instantly provisioned via API
- ✅ Elastic and scalable
- ✅ Pay for what you use
- ✅ Built-in redundancy (AZs)

**Core concepts to master:**
1. **VPC** - Your isolated network
2. **Subnets** - Network segments in AZs
3. **IGW** - Internet connectivity
4. **Route Tables** - Traffic direction
5. **Security Groups** - Instance firewalls
6. **NACLs** - Subnet firewalls

**Remember:**
- Design for high availability (multi-AZ)
- Separate public and private resources
- Use security groups as primary defense
- Plan IP space for growth
- Monitor everything

---

## 📚 **Additional Resources**

- **AWS VPC Documentation:** https://docs.aws.amazon.com/vpc/
- **AWS Networking Deep Dive:** https://aws.amazon.com/vpc/faqs/
- **IP Subnetting Calculator:** https://www.subnet-calculator.com/
- **Architecture Guide:** See `architecture.md`

---

**Last Updated:** October 30, 2025  
**Next:** Read `troubleshooting.md` for common issues
