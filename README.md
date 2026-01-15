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
<img width="1728" height="1024" alt="image" src="https://github.com/user-attachments/assets/c63611c3-8203-42fb-8ba1-6cb754abda38" />
<img width="1728" height="1024" alt="image" src="https://github.com/user-attachments/assets/fa82679c-a0bd-4859-88dc-7bed5d648a67" />
<img width="3456" height="2048" alt="image" src="https://github.com/user-attachments/assets/74728bb6-80f2-48a0-b0b5-f658436318f6" />
<img width="3456" height="2048" alt="image" src="https://github.com/user-attachments/assets/6eac10fd-d606-4351-8d04-597a5c8a655c" />
<img width="1728" height="1024" alt="Screenshot 2026-01-15 at 8 09 22 PM" src="https://github.com/user-attachments/assets/03162cb0-a00d-4cc6-9a40-76c56deed9be" />
<img width="1728" height="1059" alt="image" src="https://github.com/user-attachments/assets/b77325af-9232-4e17-a1f7-555f93fc26d9" />





