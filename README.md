# Project POC: 5 Key Tasks

This repository documents the proof-of-concept work completed for five key technical tasks. The implementation is organized into two main folders:

-   `crewai/`: Contains a consolidated solution for Agent Development, Resource Monitoring, and Asynchronous Python tasks.
-   `kubernates/`: Contains the work for the Kubernetes Knowledge Share task, including a Tilt demo.

---

## Task 1: Kubernetes (K8s) Knowledge Share

This section covers key learnings and implementation details from the Kubernetes proof-of-concept.

### Key Learnings & Architectural Insights:
-   **Declarative Manifests**: Implemented core Kubernetes objects like Deployments, Services, and Pods using YAML manifests to define the desired state.
-   **Sidecar Pattern**: Demonstrated the sidecar pattern for extending container functionality without modifying the main application. A logging sidecar was used to read logs from a shared volume.
-   **Local Development with Tilt**: Implemented a `Tiltfile` to enable a fast, iterative local development workflow for Kubernetes. Tilt automatically builds and deploys changes to a local cluster.

### Implemented Concepts:
-   **Nginx Deployment & Service**: A 2-replica Nginx deployment exposed via a NodePort service. See [kubernates/deployment.yaml](kubernates/deployment.yaml) and [kubernates/service.yaml](kubernates/service.yaml).
-   **Sidecar Demo**: A pod with a main application writing to a log file and a sidecar container tailing that file. See [kubernates/sidecar.yaml](kubernates/sidecar.yaml).
-   **Tilt Demo**: A simple web server with a `Tiltfile` for automated local deployment. See the `kubernates/tilt-demo/` directory.

### Screenshots:

*Add your screenshots of `kubectl` outputs or Tilt UI here.*

```md
![Tilt UI](docs/screenshots/tilt-ui.png)
```

```md
![Kubernetes Pods](docs/screenshots/k8s-pods.png)
```

---

## Task 2: AI Gateway Analysis

This section is for demonstrating the analysis of AI Gateway logs to identify latency patterns and error rates within a specific region.

### Latency Patterns:

*Add screenshots of logs or dashboards showing gateway latency.*

```md
![Gateway Latency Analysis](docs/screenshots/gateway-latency.png)
```

### Error Rates:

*Add screenshots of logs or dashboards showing gateway error rates.*

```md
![Gateway Error Rate Analysis](docs/screenshots/gateway-errors.png)
```

---

## Task 3: Agent Development Status

This section provides a walkthrough of the custom CrewAI agent that was built.

### Agent Architecture:
-   **Two-Agent Crew**:
    1.  **Researcher Agent**: Scans a given topic to extract key bullet points.
    2.  **Writer Agent**: Takes the bullet points and composes a concise summary.
-   **LLM Integration**: The agents are powered by the Groq LLaMA 3 model, configured via a `GROQ_API_KEY`.
-   **Implementation**: The agent, task, and crew definitions can be found in [crewai/server.py](crewai/server.py).

### Demo:
The agent's functionality can be tested via the FastAPI endpoint or the Streamlit UI.

### Screenshots:

*Add a screenshot of the final output from the agent.*

```md
![Agent Output](docs/screenshots/agent-output.png)
```

---

## Task 4: Resource Monitoring (Grafana)

This section covers how CPU/Memory utilization and scaling behavior of the agent application are monitored.

### Monitoring Stack:
-   **Prometheus**: Scrapes metrics from the application's `/metrics` endpoint.
-   **Grafana**: Provides visualization dashboards for the metrics collected by Prometheus.
-   **Docker Compose**: The entire monitoring stack is defined and managed in [crewai/docker-compose.yml](crewai/docker-compose.yml).

### Exposed Metrics:
The application exposes custom Prometheus metrics, including:
-   `crewai_cpu_percent`, `crewai_ram_percent`, `crewai_app_memory_mb`
-   `crewai_jobs_total`, `crewai_jobs_running`, `crewai_jobs_success_total`, `crewai_jobs_failed_total`
-   The metrics are generated in [crewai/server.py](crewai/server.py).

### Screenshots:

*Add screenshots of your Grafana dashboards showing CPU/Memory utilization.*

```md
![Grafana CPU Utilization](docs/screenshots/grafana-cpu.png)
```

```md
![Grafana Memory Utilization](docs/screenshots/grafana-memory.png)
```

---

## Task 5: Technical Deep Dive: Asynchronous Python

This section provides a walkthrough of the `async/await` implementation used to improve application performance.

### Asynchronous Job Execution:
-   **FastAPI Server**: An asynchronous web server built with FastAPI is used to handle requests.
-   **Non-Blocking Operations**: The long-running CrewAI `kickoff()` process, which is blocking, is executed in a separate thread using `asyncio.to_thread()`. This prevents the server from being blocked and allows it to handle other requests concurrently.
-   **Job-Based Workflow**:
    1.  A `POST` request to `/run` immediately returns a `job_id` and starts the agent task in the background.
    2.  The status of the job can be polled via the `/status/{job_id}` endpoint.
-   **Implementation**: The core async logic is in the `run_job` function in [crewai/server.py](crewai/server.py).

### Screenshots:

*Add screenshots of API calls demonstrating the async workflow (e.g., Postman or curl).*

```md
![Async Job Submission](docs/screenshots/async-job-submission.png)
```
