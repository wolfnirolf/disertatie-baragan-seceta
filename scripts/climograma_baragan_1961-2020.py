#!/usr/bin/env python3
"""
Climogramă combinată – Câmpia Bărăganului (1961-2020)
Temperatură (stânga) + Precipitaţii (dreapta) + Trend liniar OLS & Sen-Theil
"""

from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress          # pip install scipy
import pymannkendall as mk                  # pip install pymannkendall

# ─── 1. Fişiere ──────────────────────────────────────────────────────────────
HERE   = Path(__file__).resolve().parent
FILE_A = HERE / "Temperatura-precipitatii_1961-1990.xlsx"
FILE_B = HERE / "Temperatura-precipitatii_1991-2020.xlsx"
for f in (FILE_A, FILE_B):
    if not f.exists():
        sys.exit(f"{f.name} nu a fost găsit în {HERE}")

# ─── 2. Funcţie citire ───────────────────────────────────────────────────────
def load(path: Path):
    df = pd.read_excel(path, engine="openpyxl")
    df = df.set_index(df.columns[0]).apply(pd.to_numeric, errors="coerce")
    years = df.columns.astype(int)
    temp  = df.iloc[0].values
    prec  = df.iloc[1].values
    return years, temp, prec

y1,t1,p1 = load(FILE_A)
y2,t2,p2 = load(FILE_B)

years = np.concatenate([y1,y2])
temp  = np.concatenate([t1,t2])
prec  = np.concatenate([p1,p2])

ord_ = np.argsort(years)
years, temp, prec = years[ord_], temp[ord_], prec[ord_]

# ─── 3. Trend OLS + Sen-Theil ────────────────────────────────────────────────
def ols(x, y):
    mask = ~np.isnan(y)
    res  = linregress(x[mask], y[mask])
    return res, res.slope * x + res.intercept

def sen(y):
    mask = ~np.isnan(y)
    return mk.sens_slope(y[mask]).slope     # numai seria, fără x

ols_t, t_fit = ols(years, temp)
ols_p, p_fit = ols(years, prec)
sen_t = sen(temp)
sen_p = sen(prec)

# ─── 4. Figură ───────────────────────────────────────────────────────────────
fig, ax_t = plt.subplots(figsize=(13,6))          # T = axa stânga
ax_p = ax_t.twinx()                               # P = axa dreapta

# bare precipitaţii (fundal)
mask_p = ~np.isnan(prec)
ax_p.bar(years[mask_p], prec[mask_p], width=.8,
         color="#5bc0de", alpha=.8, label="Precipitaţii (mm)", zorder=1)

# linie temperatură
ax_t.set_zorder(2); ax_t.patch.set_visible(False)
ax_t.plot(years, temp, ls="--", marker="o", lw=2.2,
          color="#d9534f", label="Temperatură (°C)", zorder=3)

# trenduri punctate
ax_t.plot(years, t_fit, ls=":", lw=2, color="firebrick", zorder=4,
          label=f"Trend T: {ols_t.slope*10:+.2f}°C/dec, p={ols_t.pvalue:.3f}; "
                f"Sen={sen_t*10:+.2f}°C/dec")
ax_p.plot(years, p_fit, ls=":", lw=2, color="navy", zorder=4,
          label=f"Trend P: {ols_p.slope:+.1f} mm/an, p={ols_p.pvalue:.3f}; "
                f"Sen={sen_p:+.1f} mm/an")

# scări
ax_t.set_ylim(9.5, 14)
ax_p.set_ylim(0, 800)

# etichete, stil
ax_t.set_xlabel("Ani")
ax_t.set_ylabel("Temperatura medie anuală (°C)", color="#d9534f")
ax_p.set_ylabel("Precipitaţii anuale (mm)",      color="#5bc0de")
ax_t.tick_params(axis='y', colors="#d9534f")
ax_p.tick_params(axis='y', colors="#5bc0de")
ax_t.grid(True, ls=":", lw=.5, alpha=.6)

ax_t.set_title("Evoluţia temperaturilor şi precipitaţiilor\n"
               "în Câmpia Bărăganului (1961-2020)",
               fontsize=14, fontweight="bold")

# legendă combinată
h1,l1 = ax_t.get_legend_handles_labels()
h2,l2 = ax_p.get_legend_handles_labels()
ax_t.legend(h1+h2, l1+l2, loc="upper left", frameon=False)

fig.tight_layout()

# ─── 5. Output ───────────────────────────────────────────────────────────────

# Salvare automată și afișare
fig.tight_layout()
fig.savefig("climograma_baragan_1961-2020.png", dpi=300, bbox_inches="tight")
print("✅ Grafic salvat: climograma_baragan_1961-2020.png")
plt.show()