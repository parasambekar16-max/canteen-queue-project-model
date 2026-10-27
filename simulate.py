"""Discrete-event simulation with time-varying arrival rate."""
import heapq
import numpy as np


def simulate(rates_per_min, bin_len, mu, c, seed=None):
    """rates_per_min: arrival rate for each time bin (piecewise constant).
    bin_len: minutes per bin. mu: service rate per server (per min).
    Returns waits (min) per customer and arrival times."""
    rng = np.random.default_rng(seed)
    horizon = len(rates_per_min) * bin_len
    lam_max = max(rates_per_min)
    # thinning method for non-homogeneous Poisson arrivals
    t, arrivals = 0.0, []
    while True:
        t += rng.exponential(1 / lam_max)
        if t >= horizon:
            break
        if rng.random() < rates_per_min[int(t // bin_len)] / lam_max:
            arrivals.append(t)
    free_at = [0.0] * c
    heapq.heapify(free_at)
    waits = []
    for arr in arrivals:
        earliest = heapq.heappop(free_at)
        start = max(arr, earliest)
        waits.append(start - arr)
        heapq.heappush(free_at, start + rng.exponential(1 / mu))
    return np.array(waits), np.array(arrivals)


def replicate(rates_per_min, bin_len, mu, c, n=200):
    means, pwaits, maxw = [], [], []
    for s in range(n):
        w, _ = simulate(rates_per_min, bin_len, mu, c, seed=s)
        if len(w) == 0:
            continue
        means.append(w.mean())
        pwaits.append((w > 1e-9).mean())
        maxw.append(w.max())
    return {"mean_wait": float(np.mean(means)),
            "P_wait": float(np.mean(pwaits)),
            "max_wait": float(np.mean(maxw))}
