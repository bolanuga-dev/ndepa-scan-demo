# LagosPay Sandbox (`ndepa-scan-demo`)

Mock fintech workload for validating [`ndepa-scan`](https://github.com/bolanuga-dev/ndepa-scan) (`v1.2.9+`) static Kubernetes policy evaluation and dynamic eBPF runtime egress monitoring under the Nigeria Data Protection Act (NDPA).

## Repository Contents

```text
ndepa-scan-demo/
|-- docker-compose.yml          # Optional single-host Docker Compose deployment
|-- k8s/
|   `-- fintech-sandbox.yaml    # Kubernetes Namespace + Deployment (lagospay-sandbox)
`-- simulator/
    |-- Dockerfile              # python:3.12-slim container image definition
    `-- egress_worker.py        # Simulates outbound TCP/443 connections every 5s
```

## Prerequisites

* Linux host with kernel eBPF tracepoint support (`sys_enter_connect`) and `sudo` privileges
* `ndepa-scan` (`v1.2.9` or newer) installed on the target node (for example, `/usr/local/bin/ndepa-scan`)
* Kubernetes cluster (`containerd` or Docker runtime) with `kubectl` configured, or Docker Engine with `docker compose`

---

## Option A: Kubernetes Validation (Recommended)

### 1. Clone and Deploy the Sandbox

```bash
git clone https://github.com/bolanuga-dev/ndepa-scan-demo.git
cd ndepa-scan-demo
kubectl apply -f k8s/fintech-sandbox.yaml
kubectl get pods -n lagospay-sandbox -o wide
```

> **Multi-Node Scheduling Note:** `ndepa-scan trace` hooks `sys_enter_connect` on the **local node's kernel**. Check the `NODE` column and run `sudo ndepa-scan trace` on that exact node.
>
> If tracing on a control-plane node (`master-node`) that carries a `NoSchedule` taint, pin the workload to that node:

```bash
kubectl patch deployment lagospay-payment-api -n lagospay-sandbox \
  -p '{"spec":{"template":{"spec":{"nodeSelector":{"kubernetes.io/hostname":"master-node"},"tolerations":[{"key":"node-role.kubernetes.io/control-plane","operator":"Exists","effect":"NoSchedule"},{"key":"node-role.kubernetes.io/master","operator":"Exists","effect":"NoSchedule"}]}}}}'
kubectl get pods -n lagospay-sandbox -o wide
```

### 2. Run Static Policy Compliance Scan

Pass the target YAML file directly to `ndepa-scan` (a file path is required, not a directory):

```bash
ndepa-scan ./k8s/fintech-sandbox.yaml
```

**Expected Output:** Flags `3` Section 39 Container Security violations on `payment-worker` in `lagospay-payment-api` (`allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`, and `runAsNonRoot: true`).

### 3. Run Dynamic eBPF Runtime Egress Tracer

On the node hosting the `Running` `lagospay-payment-api` pod, run `sudo ndepa-scan trace` with `--line-buffered` `grep` to isolate workload egress from control-plane and host traffic:

```bash
sudo ndepa-scan trace | grep --line-buffered -E "8\.8\.8\.8:443|1\.1\.1\.1:443"
```

**Expected Output (repeating every ~5 seconds):**

```text
Starting eBPF dynamic egress tracer...
[Egress Detected] PID: <pid> | Process: python3 | Dest: 8.8.8.8:443
[Egress Detected] PID: <pid> | Process: python3 | Dest: 1.1.1.1:443
```

Press `Ctrl+C` to stop the tracer cleanly.

### 4. Tear Down Sandbox

```bash
kubectl delete namespace lagospay-sandbox
```

---

## Option B: Single-Host Docker Compose Validation

```bash
git clone https://github.com/bolanuga-dev/ndepa-scan-demo.git
cd ndepa-scan-demo
docker compose up -d --build
```

In a second terminal on the host, run the eBPF tracer:

```bash
sudo ndepa-scan trace | grep --line-buffered -E "8\.8\.8\.8:443|1\.1\.1\.1:443"
```

Tear down when finished:

```bash
docker compose down
```
