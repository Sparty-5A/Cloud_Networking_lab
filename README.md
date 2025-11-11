# ☁️ Cloud Networking Lab - AWS Infrastructure with Pulumi

**Modern Infrastructure as Code using Python, Pydantic, and Pulumi**

[![Pulumi](https://img.shields.io/badge/IaC-Pulumi-8A3391?style=flat-square&logo=pulumi)](https://www.pulumi.com/)
[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![AWS](https://img.shields.io/badge/Cloud-AWS-FF9900?style=flat-square&logo=amazon-aws)](https://aws.amazon.com/)
[![Pydantic](https://img.shields.io/badge/Models-Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![pytest](https://img.shields.io/badge/Tests-pytest-0A9EDC?style=flat-square&logo=pytest)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

---

## 🎯 **Project Overview**

A **portfolio project** demonstrating cloud networking fundamentals and infrastructure automation using modern Python tooling. This project bridges on-premises networks to AWS cloud infrastructure using site-to-site VPN, automated with Pulumi and validated with comprehensive testing.

**Part of a NetDevOps portfolio series - Task 2: Cloud Networking & Hybrid Connectivity**

---

## 🏗️ **Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                         AWS Cloud (us-east-1)                    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    VPC (10.0.0.0/16)                        │ │
│  │                                                              │ │
│  │  ┌──────────────────────┐    ┌──────────────────────┐     │ │
│  │  │  Public Subnet A     │    │  Public Subnet B     │     │ │
│  │  │  10.0.1.0/24         │    │  10.0.2.0/24         │     │ │
│  │  │  us-east-1a          │    │  us-east-1b          │     │ │
│  │  └──────────┬───────────┘    └──────────┬───────────┘     │ │
│  │             │                             │                 │ │
│  │             └─────────────┬───────────────┘                 │ │
│  │                           │                                 │ │
│  │                    ┌──────▼──────┐                         │ │
│  │                    │ Route Tables │                         │ │
│  │                    └──────┬──────┘                         │ │
│  │                           │                                 │ │
│  │         ┌─────────────────┼─────────────────┐              │ │
│  │         │                 │                 │              │ │
│  │    ┌────▼────┐      ┌────▼────┐      ┌────▼────┐         │ │
│  │    │   IGW   │      │ NAT GW  │      │ VPN GW  │         │ │
│  │    └────┬────┘      └────┬────┘      └────┬────┘         │ │
│  └─────────┼──────────────────┼──────────────┼───────────────┘ │
└────────────┼──────────────────┼──────────────┼─────────────────┘
             │                  │              │
             │                  │         IPSec Tunnel
             │                  │         (BGP over VPN)
             │                  │              │
        Internet             Internet          │
                                                │
                                     ┌──────────▼──────────┐
                                     │   On-Premises Lab   │
                                     │   (Future: Ubuntu   │
                                     │    or Nokia SROS)   │
                                     └─────────────────────┘
```

---

## ✨ **Features**

### **Infrastructure as Code**
- ✅ **Python-native** - No DSL, just Python
- ✅ **Type-safe** - Full IDE support and type checking
- ✅ **Modular** - Reusable components
- ✅ **Testable** - Pytest integration

### **Cloud Networking**
- ✅ **VPC** - Multi-AZ with public/private subnets
- ✅ **VPN Gateway** - Site-to-site IPSec connectivity
- ✅ **BGP** - Dynamic routing support
- ✅ **Internet Gateway** - Public internet access
- ✅ **NAT Gateway** - Private subnet internet (optional)

### **Intent-Based Design**
- ✅ **Pydantic Models** - Declarative infrastructure intent
- ✅ **YAML Configuration** - Easy-to-read intent files
- ✅ **Validation** - Automatic configuration validation
- ✅ **Type Safety** - Catch errors before deployment

### **Testing & Verification**
- ✅ **Unit Tests** - Test infrastructure logic
- ✅ **Integration Tests** - Test with mocked AWS
- ✅ **Connectivity Tests** - Verify VPN and routing
- ✅ **Coverage Reports** - Track test coverage

---

## 🚀 **Quick Start**

### **Prerequisites**

```bash
# Required
Python 3.13+
uv (package manager)
AWS Account (Free tier compatible)
Pulumi CLI

# Optional (for testing without AWS)
Docker (for LocalStack)
```

### **Installation**

```bash
# Clone the repository
git clone https://github.com/Sparty-5A/Cloud_Networking_Lab.git
cd Cloud_Networking_Lab

# Install dependencies with uv
uv sync

# Configure AWS credentials
aws configure

# Login to Pulumi (or use local backend)
pulumi login
```

### **Deploy Infrastructure**

```bash
# Navigate to Pulumi directory
cd pulumi

# Create a new stack (dev/staging/prod)
pulumi stack init dev

# Set AWS region
pulumi config set aws:region us-east-1

# Preview changes
pulumi preview

# Deploy infrastructure
pulumi up

# View outputs
pulumi stack output
```

### **Verify Deployment**

```bash
# Run connectivity tests
cd ../scripts
python verify_connectivity.py

# Monitor VPN status
python monitor_vpn.py

# Run full test suite
cd ../tests
pytest -v
```

---

## 📁 **Project Structure**

```
Cloud_Networking_Lab/
│
├── pulumi/                         # Pulumi infrastructure code
│   ├── __main__.py                # Main program entry point
│   ├── vpc.py                     # VPC module
│   ├── vpn.py                     # VPN Gateway module
│   ├── networking.py              # Subnets, routes, gateways
│   ├── Pulumi.yaml                # Project configuration
│   ├── Pulumi.dev.yaml            # Dev stack config
│   └── requirements.txt           # Python dependencies
│
├── models/                         # Pydantic intent models
│   ├── __init__.py
│   ├── aws_intent.py              # AWS network intent models
│   ├── vpc_intent.py              # VPC configuration models
│   └── vpn_intent.py              # VPN configuration models
│
├── tests/                          # Test suite
│   ├── unit/
│   │   ├── test_vpc.py           # VPC unit tests
│   │   ├── test_vpn.py           # VPN unit tests
│   │   └── test_models.py        # Intent model tests
│   ├── integration/
│   │   ├── test_deployment.py    # Integration tests
│   │   └── test_networking.py    # Network connectivity tests
│   ├── conftest.py               # Pytest fixtures
│   └── pytest.ini                # Pytest configuration
│
├── scripts/                        # Verification & monitoring
│   ├── verify_connectivity.py    # Test VPN connectivity
│   ├── monitor_vpn.py            # Monitor VPN status
│   ├── test_latency.py           # Latency testing
│   └── validate_routes.py        # Route validation
│
├── docs/                           # Documentation
│   ├── architecture.md           # Architecture overview
│   ├── setup_guide.md            # Detailed setup guide
│   ├── networking_concepts.md    # Cloud networking concepts
│   ├── pulumi_guide.md           # Pulumi usage guide
│   └── troubleshooting.md        # Common issues & solutions
│
├── examples/                       # Example configurations
│   ├── basic_vpc.yaml            # Simple VPC intent
│   ├── vpc_with_vpn.yaml         # VPC + VPN intent
│   └── multi_az.yaml             # Multi-AZ deployment
│
├── .github/                        # GitHub workflows (future)
│   └── workflows/
│       └── pulumi.yml            # CI/CD pipeline
│
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
├── LICENSE                         # MIT License
└── requirements.txt                # Root dependencies
```

---

## 🎓 **Learning Objectives**

This project demonstrates:

### **Cloud Networking Fundamentals**
- VPC design and subnet planning
- Internet Gateway vs NAT Gateway
- Route table configuration
- Security group design
- Site-to-site VPN setup
- BGP routing over VPN

### **Infrastructure as Code**
- Pulumi Python programming model
- Resource dependency management
- State management
- Stack management (dev/staging/prod)
- Secrets handling

### **DevOps Practices**
- Intent-based configuration
- Infrastructure testing
- CI/CD for infrastructure
- Documentation as code
- Version control for infrastructure

### **Python Engineering**
- Type-safe infrastructure code
- Pydantic for validation
- Testing with pytest
- Modular code design
- AWS SDK (boto3) integration

---

## 🧪 **Testing**

### **Run All Tests**

```bash
cd tests
pytest -v
```

### **Run Specific Test Types**

```bash
# Unit tests only (fast)
pytest tests/unit/ -v

# Integration tests (requires AWS/mocks)
pytest tests/integration/ -v -m integration

# With coverage report
pytest --cov=pulumi --cov=models --cov-report=html
```

### **Test Categories**

- **Unit Tests** - Test individual components in isolation
- **Integration Tests** - Test components working together
- **Connectivity Tests** - Test actual network connectivity
- **Model Tests** - Test Pydantic intent models

---

## 📊 **Monitoring & Verification**

### **Verify VPN Status**

```bash
python scripts/monitor_vpn.py
```

**Output:**
```
VPN Connection Status: available
Tunnel 1: UP (51.123.45.67)
Tunnel 2: DOWN (51.123.45.68)
BGP Status: Established
Routes Learned: 5
```

### **Test Connectivity**

```bash
python scripts/verify_connectivity.py
```

**Output:**
```
✓ VPC reachable
✓ Public subnet A reachable
✓ Public subnet B reachable
✓ VPN tunnel 1: UP (latency: 23ms)
✓ VPN tunnel 2: DOWN
✗ On-prem network unreachable (VPN not configured)
```

### **Validate Routes**

```bash
python scripts/validate_routes.py
```

---

## 🎯 **Use Cases**

### **1. Learning Cloud Networking**
- Understand AWS VPC concepts
- Practice infrastructure automation
- Learn Pulumi and IaC

### **2. Portfolio Project**
- Demonstrate cloud skills
- Show Python proficiency
- Prove infrastructure knowledge

### **3. Lab Environment**
- Test hybrid cloud scenarios
- Experiment with networking
- Learn without impacting production

### **4. Foundation for Expansion**
- Add more AWS services
- Integrate with on-prem lab
- Build multi-region setup

---

## 🔧 **Configuration**

### **Intent-Based Configuration**

Create a YAML file defining your infrastructure intent:

```yaml
# examples/vpc_with_vpn.yaml
network:
  vpc:
    cidr: "10.0.0.0/16"
    enable_dns: true
    enable_dns_hostnames: true
    
  subnets:
    - name: "public-a"
      cidr: "10.0.1.0/24"
      availability_zone: "us-east-1a"
      public: true
      
    - name: "public-b"
      cidr: "10.0.2.0/24"
      availability_zone: "us-east-1b"
      public: true
      
  vpn:
    enabled: true
    customer_gateway:
      ip_address: "YOUR_PUBLIC_IP"
      bgp_asn: 65000
    static_routes:
      - "192.168.1.0/24"
      - "192.168.2.0/24"
```

Load and deploy:

```python
from models.aws_intent import AWSNetworkIntent
import yaml

# Load intent
with open("examples/vpc_with_vpn.yaml") as f:
    config = yaml.safe_load(f)

# Validate with Pydantic
intent = AWSNetworkIntent(**config)

# Deploy with Pulumi
deploy_network(intent)
```

---

## 📚 **Documentation**

- **[Architecture Overview](docs/architecture.md)** - System design and components
- **[Setup Guide](docs/setup_guide.md)** - Detailed installation and configuration
- **[Networking Concepts](docs/networking_concepts.md)** - AWS networking fundamentals
- **[Pulumi Guide](docs/pulumi_guide.md)** - How to use Pulumi effectively
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

---

## 🛠️ **Technologies**

| Technology | Purpose | Why? |
|------------|---------|------|
| **Pulumi** | Infrastructure as Code | Python-native, type-safe, testable |
| **Python 3.13** | Programming Language | Modern, readable, extensive ecosystem |
| **Pydantic** | Data Validation | Type-safe intent models |
| **pytest** | Testing Framework | Industry standard, powerful fixtures |
| **boto3** | AWS SDK | Runtime AWS operations |
| **AWS VPC** | Networking | Isolated cloud network |
| **AWS VPN Gateway** | Connectivity | Site-to-site IPSec VPN |
| **BGP** | Routing Protocol | Dynamic route exchange |

---

## 💰 **Cost Estimation**

**Estimated AWS costs for this lab:**

| Resource | Estimated Cost |
|----------|---------------|
| VPC | Free |
| Subnets | Free |
| Internet Gateway | Free |
| Route Tables | Free |
| VPN Gateway | ~$0.05/hour (~$36/month) |
| NAT Gateway (optional) | ~$0.045/hour + data (~$32/month) |
| Data Transfer | Varies (first 1GB/month free) |

**💡 Tips to Minimize Costs:**
- Destroy resources when not in use: `pulumi destroy`
- Use `t3.micro` instances (free tier eligible)
- Monitor usage with AWS Cost Explorer
- Set up billing alerts

---

## 🚧 **Roadmap**

### **Phase 1: Foundation** ✅
- [x] VPC with multi-AZ subnets
- [x] Internet Gateway
- [x] VPN Gateway configuration
- [x] Basic Pulumi modules
- [x] Pydantic intent models
- [x] Unit tests

### **Phase 2: Connectivity** 🚧
- [ ] Configure on-prem side (Ubuntu VM)
- [ ] Establish IPSec tunnels
- [ ] Configure BGP peering
- [ ] End-to-end connectivity tests
- [ ] Latency monitoring

### **Phase 3: Advanced** 📋
- [ ] NAT Gateway for private subnets
- [ ] VPC Flow Logs
- [ ] CloudWatch monitoring
- [ ] Multi-region deployment
- [ ] Transit Gateway
- [ ] AWS Direct Connect simulation

### **Phase 4: Automation** 📋
- [ ] CI/CD pipeline
- [ ] Automated testing
- [ ] Policy as code
- [ ] Cost optimization
- [ ] Documentation generation

---

## 🤝 **Contributing**

This is a portfolio/learning project, but suggestions and improvements are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📄 **License**

MIT License - see [LICENSE](LICENSE) for details

---

## 🙏 **Acknowledgments**

- **Pulumi** - Modern infrastructure as code platform
- **AWS** - Cloud infrastructure provider
- **Pydantic** - Data validation library
- **Python community** - Amazing ecosystem

---

## 📞 **Contact**

**Project Link:** https://github.com/Sparty-5A/Cloud_Networking_Lab

**Portfolio:** [Link to your portfolio]

**LinkedIn:** [Your LinkedIn]

---

## 🎓 **Part of NetDevOps Portfolio Series**

- **Task 1:** [Nokia SROS Automation](https://github.com/Sparty-5A/NetDevOps_project) - Network automation with Python
- **Task 2:** [Cloud Networking Lab](https://github.com/Sparty-5A/Cloud_Networking_Lab) - AWS infrastructure *(You are here)*
- **Task 3:** SD-WAN & Overlay Networking *(Coming soon)*
- **Task 4:** Observability & Validation *(Coming soon)*

---

**Built for learning and portfolio development**

*"The best way to learn is to build"*
