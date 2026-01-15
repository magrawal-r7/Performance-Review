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

```md
![Agent Output](docs/screenshots/agent-output.png)
