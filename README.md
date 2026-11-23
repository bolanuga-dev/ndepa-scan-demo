# ndepa-scan Mock Fintech Sandbox (`v1.2.9`)

Zero-risk testbed simulating a Nigerian fintech payment service (`LagosPay`) handling BVN/NIN data with both compliant domestic database calls and unauthorized cross-border egress.

---

## Option 1: Single-Node Docker Compose Setup (60 Seconds)

### 1. Start the Sandbox
```bash
git clone https://github.com/bolanuga-dev/ndepa-scan-demo.git
cd ndepa-scan-demo
docker compose up -d --build
