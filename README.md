# LagosPay Sandbox (`ndepa-scan-demo`)

Mock fintech workload for validating [`ndepa-scan`](https://github.com/bolanuga-dev/ndepa-scan) (`v1.2.9+`) static Kubernetes policy evaluation and dynamic eBPF runtime egress monitoring under the Nigeria Data Protection Act (NDPA).

## Repository Contents

```text
ndepa-scan-demo/
├── docker-compose.yml          # Optional single-host Docker Compose deployment
├── k8s/
│   └── fintech-sandbox.yaml    # Kubernetes Namespace + Deployment (lagospay-sandbox)
└── simulator/
    ├── Dockerfile              # python:3.12-slim container image definition
    └── egress_worker.py        # Simulates outbound TCP/443 connections every 5s
