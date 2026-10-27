import streamlit as st
import pandas as pd
from model import mmc_metrics

st.title("College Canteen Queue Model (M/M/c)")
lam = st.slider("Arrival rate λ (students/min)", 0.5, 10.0, 3.0, 0.1)
mu = st.slider("Service rate μ per counter (students/min)", 0.5, 5.0, 1.0, 0.1)
c = st.slider("Number of counters c", 1, 10, 4)
m = mmc_metrics(lam, mu, c)
if not m["stable"]:
    st.error(f"Unstable: utilization ρ = {m['rho']:.2f} ≥ 1. Add counters.")
else:
    st.metric("Utilization ρ", f"{m['rho']:.2f}")
    st.metric("Probability of waiting", f"{m['P_wait']:.2%}")
    st.metric("Avg queue length", f"{m['Lq']:.2f}")
    st.metric("Avg wait (min)", f"{m['Wq']:.2f}")
rows = [{"counters": k, "avg_wait_min": mmc_metrics(lam, mu, k)["Wq"]}
        for k in range(1, 11) if mmc_metrics(lam, mu, k)["stable"]]
if rows:
    st.line_chart(pd.DataFrame(rows).set_index("counters"))
