import pandas as pd
import streamlit as st

st.set_page_config(page_title="Operational Intelligence", layout="wide")

st.title("Operational Intelligence Platform")
st.write("Cloud Service Health Monitor — Stage C (Analytics & Dashboard)")

DATA_PATH = "data/telemetry.csv"
CPU_THRESHOLD = 50
LATENCY_THRESHOLD = 200

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df.sort_values("timestamp")


df = load_data(DATA_PATH)

st.sidebar.header("Controls")

window = st.sidebar.selectbox(
    "Select time window (minutes)",
    options=[10, 30, 60],
    index=2
)
df_filtered = df.tail(window)

latest_cpu = df_filtered["cpu_usage"].iloc[-1]
avg_cpu = df_filtered["cpu_usage"].mean()
max_cpu = df_filtered["cpu_usage"].max()
latest_memory = df_filtered["memory_usage"].iloc[-1]
avg_memory = df_filtered["memory_usage"].mean()
latest_latency = df_filtered["latency_ms"].iloc[-1]
avg_latency = df_filtered["latency_ms"].mean()
max_latency = df_filtered["latency_ms"].max()

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

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

col1.metric("Latest CPU Usage (%)", f"{latest_cpu:.2f}")
col2.metric("Average CPU Usage (%)", f"{avg_cpu:.2f}")
col3.metric("Peak CPU Usage (%)", f"{max_cpu:.2f}")
col4.metric("Latest Memory Usage (%)", f"{latest_memory:.2f}")
col5.metric("Average Memory Usage (%)", f"{avg_memory:.2f}")
col6.metric("Latest Latency (ms)", f"{latest_latency:.2f}")
col7.metric("Average Latency (ms)", f"{avg_latency:.2f}")
col8.metric("Peak Latency (ms)", f"{max_latency:.2f}")

st.subheader("Telemetry Preview")
st.dataframe(df_filtered.head(20), use_container_width=True)

st.header("Metric Trends")

st.subheader("CPU Usage Over Time")
st.line_chart(df_filtered.set_index("timestamp")["cpu_usage"])

st.subheader("Memory Usage Over Time")
st.line_chart(df_filtered.set_index("timestamp")["memory_usage"])

st.subheader("CPU vs Memory")
scatter_df = df_filtered[["cpu_usage", "memory_usage"]].copy()
st.scatter_chart(scatter_df, x="cpu_usage", y="memory_usage")

st.subheader("Latency Over Time")
st.line_chart(df_filtered.set_index("timestamp")["latency_ms"])

st.header("Anomaly Insights")
st.subheader("High CPU Events")

high_cpu_events = df_filtered[df_filtered["cpu_usage"] > CPU_THRESHOLD]
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

st.subheader("High Latency Events")

high_latency_events = df_filtered[df_filtered["latency_ms"] > LATENCY_THRESHOLD]
high_latency_count = len(high_latency_events)

if high_latency_count > 0:
    last_high_latency_time = high_latency_events["timestamp"].iloc[-1]
else:
    last_high_latency_time = None

st.write(f"Number of high latency events: {high_latency_count}")

if last_high_latency_time is not None:
    st.write(f"Last high latency event: {last_high_latency_time}")
else:
    st.write("Last high latency event: none")

st.dataframe(high_latency_events, use_container_width=True)