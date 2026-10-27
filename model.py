"""Analytical M/M/c queueing model (Erlang C)."""
from math import factorial


def mmc_metrics(lam, mu, c):
    """lam = arrivals/min, mu = services/min per server, c = servers.
    Returns dict of steady-state metrics (times in minutes)."""
    a = lam / mu            # offered load
    rho = a / c             # utilization
    if rho >= 1:
        return {"rho": rho, "stable": False, "P_wait": 1.0,
                "Lq": float("inf"), "Wq": float("inf"),
                "L": float("inf"), "W": float("inf")}
    top = (a ** c / factorial(c)) / (1 - rho)
    bottom = sum(a ** k / factorial(k) for k in range(c)) + top
    p_wait = top / bottom
    lq = p_wait * rho / (1 - rho)
    wq = lq / lam
    return {"rho": rho, "stable": True, "P_wait": p_wait,
            "Lq": lq, "Wq": wq, "L": lq + a, "W": wq + 1 / mu}


if __name__ == "__main__":
    print(mmc_metrics(lam=3.0, mu=1.0, c=4))
