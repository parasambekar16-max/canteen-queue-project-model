"""Read observed data, compare attempts, save tables + charts."""
import pandas as pd
import matplotlib.pyplot as plt
from model import mmc_metrics
from simulate import replicate

df = pd.read_csv("data/observed_arrivals.csv")
BIN = 5  # minutes per observation bin
df["lam_per_min"] = df["arrivals"] / BIN
mu = 60 / df["avg_service_seconds"].mean()   # services/min per server
lam_avg = df["lam_per_min"].mean()
lam_peak = df["lam_per_min"].max()

rows = []
for c in (1, 2, 3):
    # Attempt A: constant average rate (simple M/M/c)
    m = mmc_metrics(lam_avg, mu, c)
    rows.append({"model": "M/M/c avg rate", "servers": c, "lambda": lam_avg,
                 "rho": m["rho"], "P_wait": m["P_wait"], "Wq_min": m["Wq"]})
    # Attempt B: constant PEAK rate (worst case)
    m = mmc_metrics(lam_peak, mu, c)
    rows.append({"model": "M/M/c peak rate", "servers": c, "lambda": lam_peak,
                 "rho": m["rho"], "P_wait": m["P_wait"], "Wq_min": m["Wq"]})
    # Attempt C: time-varying simulation
    s = replicate(list(df["lam_per_min"]), BIN, mu, c)
    rows.append({"model": "Simulation time-varying", "servers": c,
                 "lambda": "varies", "rho": None,
                 "P_wait": s["P_wait"], "Wq_min": s["mean_wait"]})

res = pd.DataFrame(rows)
res.to_csv("outputs/attempts_comparison.csv", index=False)  # open in Excel/Tableau
print(res.round(3).to_string(index=False))

# Chart 1: arrivals over time
plt.figure(figsize=(7, 4))
plt.bar(df["minute_start"], df["arrivals"], width=4)
plt.xlabel("Minutes since lunch start"); plt.ylabel("Arrivals per 5 min")
plt.title("Observed arrivals"); plt.tight_layout()
plt.savefig("outputs/arrivals.png", dpi=150); plt.close()

# Chart 2: mean wait by model and servers
pv = res.pivot(index="servers", columns="model", values="Wq_min")
pv.replace([float("inf")], float("nan")).plot(kind="bar", figsize=(8, 4))
plt.ylabel("Mean wait (min)"); plt.title("Waiting time by attempt")
plt.tight_layout(); plt.savefig("outputs/wait_comparison.png", dpi=150)
print("Saved to outputs/")
