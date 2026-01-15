import os
os.environ["CREWAI_TELEMETRY_ENABLED"] = "false"

import time
import uuid
import psutil
import asyncio
from typing import Dict, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from crewai import Agent, Task, Crew, LLM

app = FastAPI(title="CrewAI Async Server")

process = psutil.Process(os.getpid())

# ----------------------------
# Prometheus Metrics
# ----------------------------
CPU_PERCENT = Gauge("crewai_cpu_percent", "CPU usage percent (system)")
RAM_PERCENT = Gauge("crewai_ram_percent", "RAM usage percent (system)")
APP_MEM_MB = Gauge("crewai_app_memory_mb", "App memory usage in MB")

JOBS_TOTAL = Counter("crewai_jobs_total", "Total jobs submitted")
JOBS_RUNNING = Gauge("crewai_jobs_running", "Currently running jobs")
JOBS_SUCCESS = Counter("crewai_jobs_success_total", "Successful jobs")
JOBS_FAILED = Counter("crewai_jobs_failed_total", "Failed jobs")

# ----------------------------
# In-memory job store
# ----------------------------
jobs: Dict[str, Dict] = {}


class RunRequest(BaseModel):
    topic: str


def update_metrics():
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory().percent
    mem_mb = process.memory_info().rss / (1024 * 1024)

    CPU_PERCENT.set(cpu)
    RAM_PERCENT.set(ram)
    APP_MEM_MB.set(mem_mb)


def build_crew(topic: str):
    groq_llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7
    )

    researcher = Agent(
        role="Researcher",
        goal="Give key points in bullet form about the topic",
        backstory="You are a sharp research assistant.",
        llm=groq_llm,
        verbose=False
    )

    writer = Agent(
        role="Writer",
        goal="Convert the key points into a short clean summary",
        backstory="You write clear and simple summaries.",
        llm=groq_llm,
        verbose=False
    )

    task1 = Task(
        description=f"Give 6 bullet points about: {topic}",
        expected_output="6 bullet points",
        agent=researcher
    )

    task2 = Task(
        description="Convert the bullet points into a simple 6-8 line paragraph summary.",
        expected_output="Short paragraph summary",
        agent=writer
    )

    return Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        verbose=False
    )


async def run_job(job_id: str, topic: str):
    JOBS_RUNNING.inc()
    jobs[job_id]["status"] = "running"
    jobs[job_id]["started_at"] = time.time()

    try:
        # ✅ Run blocking CrewAI in thread so FastAPI stays responsive
        def blocking_kickoff():
            crew = build_crew(topic)
            return crew.kickoff()

        result = await asyncio.to_thread(blocking_kickoff)

        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = str(result)
        jobs[job_id]["ended_at"] = time.time()
        jobs[job_id]["runtime_seconds"] = round(jobs[job_id]["ended_at"] - jobs[job_id]["started_at"], 2)

        JOBS_SUCCESS.inc()

    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["ended_at"] = time.time()
        JOBS_FAILED.inc()

    finally:
        JOBS_RUNNING.dec()


@app.get("/health")
def health():
    update_metrics()
    return {"status": "ok"}


@app.post("/run")
async def run(req: RunRequest):
    update_metrics()

    job_id = str(uuid.uuid4())
    JOBS_TOTAL.inc()

    jobs[job_id] = {
        "job_id": job_id,
        "topic": req.topic,
        "status": "queued",
        "result": None,
        "error": None,
        "runtime_seconds": None,
    }

    # ✅ fire-and-forget background task
    asyncio.create_task(run_job(job_id, req.topic))

    return {"job_id": job_id, "status": "queued"}


@app.get("/status/{job_id}")
def status(job_id: str):
    update_metrics()

    if job_id not in jobs:
        return {"error": "job_id not found"}

    return jobs[job_id]


@app.get("/metrics")
def metrics():
    update_metrics()
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/utilization")
def utilization():
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory().percent
    mem_mb = process.memory_info().rss / (1024 * 1024)

    # update prometheus gauges also ✅
    CPU_PERCENT.set(cpu)
    RAM_PERCENT.set(ram)
    APP_MEM_MB.set(mem_mb)

    return {
        "cpu_percent": round(cpu, 2),
        "ram_percent": round(ram, 2),
        "app_mem_mb": round(mem_mb, 2)
    }
