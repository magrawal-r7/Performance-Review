import os
os.environ["CREWAI_TELEMETRY_ENABLED"] = "false"  # ✅ FIX telemetry signal issue

import time
import psutil
import streamlit as st
from prometheus_client import start_http_server, Gauge
from crewai import Agent, Task, Crew, LLM


# ----------------------------
# Streamlit Config
# ----------------------------
st.set_page_config(page_title="CrewAI Resource Monitor", page_icon="📊", layout="wide")
st.title("📊 CrewAI Agent App + Resource Utilization (Grafana Ready)")
st.caption("Shows final response + Prometheus metrics at /metrics")

process = psutil.Process(os.getpid())


# ----------------------------
# Prometheus Setup (✅ No duplicates)
# ----------------------------
@st.cache_resource
def start_metrics_server():
    start_http_server(8000)  # http://localhost:8000/metrics
    return True

@st.cache_resource
def init_prometheus_metrics():
    CPU_PERCENT = Gauge("crewai_cpu_percent", "CPU usage percent (system)")
    RAM_PERCENT = Gauge("crewai_ram_percent", "RAM usage percent (system)")
    APP_MEM_MB = Gauge("crewai_app_memory_mb", "App memory usage in MB")
    return CPU_PERCENT, RAM_PERCENT, APP_MEM_MB

start_metrics_server()
CPU_PERCENT, RAM_PERCENT, APP_MEM_MB = init_prometheus_metrics()


def update_metrics():
    cpu = psutil.cpu_percent(interval=0.2)
    ram = psutil.virtual_memory().percent
    mem_mb = process.memory_info().rss / (1024 * 1024)

    CPU_PERCENT.set(cpu)
    RAM_PERCENT.set(ram)
    APP_MEM_MB.set(mem_mb)

    return cpu, ram, mem_mb


# ----------------------------
# CrewAI Setup
# ----------------------------
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


# ----------------------------
# UI
# ----------------------------
api_key_found = bool(os.getenv("GROQ_API_KEY"))

st.sidebar.title("⚙️ Settings")
st.sidebar.write("✅ GROQ_API_KEY Found" if api_key_found else "❌ GROQ_API_KEY Missing")
st.sidebar.markdown("---")
st.sidebar.write("✅ Metrics Endpoint:")
st.sidebar.code("http://localhost:8000/metrics")

topic = st.text_input("Enter topic", placeholder="Example: AI, Kubernetes, DevOps")

run_btn = st.button("✅ Run Agents")

# show current utilization
cpu, ram, mem_mb = update_metrics()
c1, c2, c3 = st.columns(3)
c1.metric("CPU % (system)", f"{cpu:.1f}%")
c2.metric("RAM % (system)", f"{ram:.1f}%")
c3.metric("App Memory (MB)", f"{mem_mb:.1f} MB")

st.markdown("---")
st.markdown("## 🧾 Final Result")

if run_btn:
    if not api_key_found:
        st.error("❌ GROQ_API_KEY not found. Please export it first.")
    elif not topic.strip():
        st.warning("⚠️ Please enter a topic.")
    else:
        start = time.time()

        with st.spinner("⏳ Running agents... please wait"):
            crew = build_crew(topic)
            result = crew.kickoff()

        runtime = round(time.time() - start, 2)

        st.success("✅ Completed!")
        st.write("### ✅ Topic")
        st.write(topic)

        st.write("### ⏱️ Runtime (seconds)")
        st.write(runtime)

        st.write("### ✅ Response")
        st.write(str(result))
else:
    st.info("Click ✅ Run Agents to generate output.")
