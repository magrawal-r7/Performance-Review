# Project POC: 5 Key Tasks

This repository documents the proof-of-concept work completed for five key technical tasks. The implementation is organized into two main folders:

-   `crewai/`: Contains a consolidated solution for Agent Development, Resource Monitoring, and Asynchronous Python tasks.
-   `kubernates/`: Contains the work for the Kubernetes Knowledge Share task, including a Tilt demo.

---

# Project POC: 5 Key Tasks

This repository documents the proof-of-concept work completed for five key technical tasks.

✅ **Primary Deliverable:** The consolidated `crewai/` implementation (Agent Development + Resource Monitoring + Async FastAPI execution).  
Supporting POCs include Kubernetes + Tilt demo and AI Gateway analysis placeholders.

The implementation is organized into two main folders:

- `crewai/`: Consolidated solution for Agent Development, Resource Monitoring, and Asynchronous Python execution.
- `kubernates/`: Kubernetes learning + YAML manifests + sidecar demo + Tilt local dev workflow.

---

## ✅ Task 1: CrewAI Agent + Async FastAPI + Resource Utilization (Primary Deliverable)

This task delivers the **end-to-end working application** that includes:

✅ CrewAI agent development  
✅ Async FastAPI server behavior  
✅ CPU/RAM/App memory monitoring  
✅ Prometheus + Grafana dashboards for visualization  

This is the final combined implementation and serves as the **core POC output** of this repository.

---

### ✅ 1. Agent Development (CrewAI)

#### Agent Architecture:
- **Two-Agent Crew**
  1. **Researcher Agent**: Scans a given topic to extract key bullet points.
  2. **Writer Agent**: Converts bullet points into a clean concise summary.
- **LLM Integration**
  - Uses **Groq LLaMA 3.3 70B**
  - Controlled using `GROQ_API_KEY`
- **Implementation**
  - Agent, Task, and Crew definitions are implemented inside:
    - `crewai/server.py`

---

### ✅ 2. Asynchronous Execution (FastAPI + Job Workflow)

To improve responsiveness, the long running CrewAI `kickoff()` call (blocking) is executed asynchronously using:

✅ `asyncio.to_thread()` — so the API remains responsive while CrewAI runs in background

#### Workflow:
1. `POST /run` submits a topic and immediately returns a `job_id`
2. The job starts in the background
3. `GET /status/{job_id}` allows polling for completion
4. `GET /metrics` exposes Prometheus-compatible metrics

#### Key endpoints:
- `/health` → health + metrics update
- `/run` → submit background CrewAI job
- `/status/{job_id}` → job tracking
- `/metrics` → Prometheus scrape endpoint
- `/utilization` → system CPU/RAM/App memory in JSON

---

### ✅ 3. Resource Monitoring (Grafana Graphing)

This POC includes full observability for CPU + Memory monitoring using:

- **Prometheus** (scrapes metrics from application)
- **Grafana** (visualizes dashboards)
- **Docker Compose** (brings up monitoring stack quickly)

#### Prometheus Metrics Exposed
The application exposes custom Prometheus metrics, such as:

- `crewai_cpu_percent`, `crewai_ram_percent`, `crewai_app_memory_mb`
- `crewai_jobs_total`, `crewai_jobs_running`
- `crewai_jobs_success_total`, `crewai_jobs_failed_total`

Monitoring stack configuration is defined inside:
- `crewai/docker-compose.yml`
- `crewai/prometheus.yml`

---

### ✅ Demo Screenshots

📌 Add screenshots of working output + dashboards here:

<img width="1728" height="1024" alt="image" src="https://github.com/user-attachments/assets/c63611c3-8203-42fb-8ba1-6cb754abda38" />

<img width="1728" height="1024" alt="image" src="https://github.com/user-attachments/assets/fa82679c-a0bd-4859-88dc-7bed5d648a67" />

<img width="3456" height="2048" alt="image" src="https://github.com/user-attachments/assets/74728bb6-80f2-48a0-b0b5-f658436318f6" />

<img width="1728" height="1024" alt="Screenshot 2026-01-15 at 8 08 50 PM" src="https://github.com/user-attachments/assets/15acf5e8-69bb-49ff-80b1-450b7e811428" />


<img width="1728" height="1024" alt="Screenshot 2026-01-15 at 8 09 22 PM" src="https://github.com/user-attachments/assets/03162cb0-a00d-4cc6-9a40-76c56deed9be" />

<img width="1728" height="1059" alt="image" src="https://github.com/user-attachments/assets/b77325af-9232-4e17-a1f7-555f93fc26d9" />


## ✅ Task 2:Kubernetes POC (Manifests + Tilt Demo)

This folder contains a hands-on Kubernetes POC covering core primitives (Pod/Deployment/Service), ConfigMap/Secret usage patterns, the sidecar pattern, and a Tilt-based local dev loop.

## What’s included

### 1)Tilt demo (local dev loop)
The Tilt demo builds a tiny NGINX image serving a local `index.html`, deploys it to Kubernetes, and port-forwards it.

Files:
- Tilt config: [tilt-demo/Tiltfile](tilt-demo/Tiltfile)
- K8s manifests: [tilt-demo/k8s.yaml](tilt-demo/k8s.yaml)
- Image build: [tilt-demo/Dockerfile](tilt-demo/Dockerfile)
- Web content: [tilt-demo/index.html](tilt-demo/index.html)

Run:

```bash
cd tilt-demo

tilt up
```

Then open the forwarded URL shown by Tilt (configured as `port_forwards=8080`).

### 📸 Screenshots

![Screenshot 1](https://github.com/user-attachments/assets/8fd9c9ea-a7df-4928-bea8-bcc56643fdf2)

![Screenshot 2](https://github.com/user-attachments/assets/d2a284c3-b992-46a3-8e12-8c201c5327fd)

```

### 2) NGINX Deployment + Service
- **Deployment**: 2 replicas of `nginx:latest`.
  - File: [deployment.yaml](deployment.yaml)
- **Service**: `NodePort` service exposing port 80.
  - File: [service.yaml](service.yaml)

Run:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get pods
kubectl get svc
```
---

### 3) ConfigMap (Mount NGINX config)
This demo mounts a ConfigMap into `/etc/nginx/conf.d` to serve a custom response.

- ConfigMap with `custom.conf`:
  - File: [nginx-config.yaml](nginx-config.yaml)
- Pod that mounts the config:
  - File: [nginx-config-pod.yaml](nginx-config-pod.yaml)

Run:

```bash
kubectl apply -f nginx-config.yaml
kubectl apply -f nginx-config-pod.yaml
kubectl get pod nginx-configmap-pod
kubectl port-forward pod/nginx-configmap-pod 8081:80
```


---


### 4) Secret env var (references `db-secret`)
The pod in [pod-secret.yaml](pod-secret.yaml) references a Secret named `db-secret` via env vars.

Note: this folder currently contains the **pod** that consumes `db-secret`, but not a manifest defining the `db-secret` Secret.

Create it (example):

```bash
kubectl create secret generic db-secret \
  --from-literal=DB_USER=admin \
  --from-literal=DB_PASS='pass123'

kubectl apply -f pod-secret.yaml
kubectl exec -it secret-demo -- env | egrep 'DB_USER|DB_PASS'
```

---

### 5) Sidecar pattern demo (shared logs)
A single Pod with:
- **app container** writing logs to `/var/log/app.log`
- **sidecar container** tailing the same file
- shared volume: `emptyDir` mounted into both containers

File: [sidecar.yaml](sidecar.yaml) (same as [sidecar-demo.yaml](sidecar-demo.yaml))

Run:

```bash
kubectl apply -f sidecar.yaml
kubectl logs -f sidecar-demo -c sidecar
```
---





