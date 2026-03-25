import pandas as pd
import streamlit as st

st.set_page_config(page_title="Operational Intelligence", layout="wide")

st.title("Operational Intelligence Platform")
st.write("Cloud Service Health Monitor — Stage C (Analytics & Dashboard)")

DATA_PATH = "data/telemetry.csv"
CPU_THRESHOLD = 50

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df.sort_values("timestamp")

df = load_data(DATA_PATH)
latest_cpu = df["cpu_usage"].iloc[-1]
avg_cpu = df["cpu_usage"].mean()
max_cpu = df["cpu_usage"].max()
latest_memory = df["memory_usage"].iloc[-1]
avg_memory = df["memory_usage"].mean()

if latest_cpu > CPU_THRESHOLD: 
    status = "High Load" 
else: 
    status = "Normal"


st.subheader("System Status")

if status == "High Load":
    st.error(f"⚠️ System under high load (CPU > {CPU_THRESHOLD}%)")
else:
    st.success("✅ System operating normally")

st.caption("Current status is based on the latest CPU reading. Historical high CPU events are shown below.")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Latest CPU Usage (%)", f"{latest_cpu:.2f}")
col2.metric("Average CPU Usage (%)", f"{avg_cpu:.2f}")
col3.metric("Peak CPU Usage (%)", f"{max_cpu:.2f}")
col4.metric("Latest Memory Usage (%)", f"{latest_memory:.2f}")
col5.metric("Average Memory Usage (%)", f"{avg_memory:.2f}")

st.subheader("Telemetry Preview")
st.dataframe(df.head(20), use_container_width=True)

st.subheader("CPU Usage Over Time")
st.line_chart(df.set_index("timestamp")["cpu_usage"])

st.subheader("High CPU Events")

high_cpu_events = df[df["cpu_usage"] > CPU_THRESHOLD]
high_cpu_count = len(high_cpu_events)
if high_cpu_count > 0:
    last_high_cpu_time = high_cpu_events["timestamp"].iloc[-1]
else:
    last_high_cpu_time = None

st.write(f"Number of high CPU events: {high_cpu_count}")
if last_high_cpu_time is not None:
    st.write(f"Last high CPU event: {last_high_cpu_time}")
else:
    st.write("Last high CPU event: none")
st.dataframe(high_cpu_events, use_container_width=True)

st.subheader("Memory Usage Over Time")
st.line_chart(df.set_index("timestamp")["memory_usage"])

st.subheader("CPU vs Memory")

scatter_df = df[["cpu_usage", "memory_usage"]].copy()
st.scatter_chart(scatter_df, x="cpu_usage", y="memory_usage")