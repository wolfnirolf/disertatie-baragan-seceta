#!/usr/bin/env python3
"""
Climogramă anuală 1991-2020
– bare precipitaţii (#5bc0de) | axă dreapta: 0-800 mm
– linie temperatură  (#d9534f) | axă stânga : 9.5-14 °C
– 2014: lipseşte → NaN ⇒ bară omisă + linie întreruptă + etichetă
"""

from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

HERE  = Path(__file__).resolve().parent
EXCEL = HERE / "Temperatura-precipitatii_1991-2020.xlsx"
if not EXCEL.exists():
    sys.exit(f"{EXCEL.name} nu a fost găsit în {HERE}")

# 1. Citire flexibilă (prima coloană devine index)
df_raw   = pd.read_excel(EXCEL, engine="openpyxl")
firstcol = df_raw.columns[0]
df       = df_raw.set_index(firstcol).apply(pd.to_numeric, errors="coerce")

years = df.columns.astype(int)      # 1991 … 2020 (include 2014)
temp  = df.iloc[0].values
prec  = df.iloc[1].values

# 2. Plot
fig, ax_t = plt.subplots(figsize=(12, 6))
ax_p      = ax_t.twinx()
ax_p.set_zorder(1); ax_t.set_zorder(2); ax_t.patch.set_visible(False)

mask = ~np.isnan(prec)
ax_p.bar(years[mask], prec[mask],
         width=0.6, color="#5bc0de", alpha=.8,
         label="Precipitaţii 1991-2020", zorder=1)

ax_t.plot(years, temp,
          color="#d9534f", lw=2.2, ls="--", marker="o",
          label="Temp 1991-2020", zorder=3)

# 3. Limite scări FIXE
ax_t.set_ylim(9.5, 14)
ax_p.set_ylim(0, 800)

# 4. Etichetă pentru anul 2014 (lipsă date)
if 2014 in years:
    idx = np.where(years == 2014)[0][0]
    ax_p.text(years[idx], ax_p.get_ylim()[1]*0.94,
              "(2014 – lipsă date)",
              ha="center", va="top", rotation=90, fontsize=9)

# 5. Estetică
ax_t.set_xlabel("An")
ax_t.set_ylabel("Temperatura medie (°C)",  color="#d9534f")
ax_p.set_ylabel("Precipitaţii anuale (mm)", color="#5bc0de")
ax_t.tick_params(axis="y", colors="#d9534f")
ax_p.tick_params(axis="y", colors="#5bc0de")
ax_t.grid(True, ls=":", lw=.5, alpha=.6)

ax_t.set_title("Climogramă multianuală 1991-2020\n(Temperatură vs. Precipitaţii)",
               fontsize=14, fontweight="bold")

h1,l1=ax_t.get_legend_handles_labels()
h2,l2=ax_p.get_legend_handles_labels()
ax_t.legend(h1+h2, l1+l2, loc="upper left", frameon=False)

fig.tight_layout()

# 6. Afişare / salvare

# Salvare automată și afișare
fig.tight_layout()
fig.savefig("climograma_1991-2020.png", dpi=300, bbox_inches="tight")
print("✅ Grafic salvat: climograma_1991-2020.png")
plt.show()