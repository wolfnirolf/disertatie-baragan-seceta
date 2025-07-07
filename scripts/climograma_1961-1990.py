#!/usr/bin/env python3
"""
Climogramă anuală 1961-1990
– bare precipitaţii (albastru #5bc0de)   |   axă dreapta: 0-800 mm
– linie temperatură  (roşu  #d9534f)     |   axă stânga : 9.5-14 °C
Fişierul Excel trebuie să stea în acelaşi director cu scriptul.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === 1. Citire date ==========================================
HERE = Path(__file__).resolve().parent
EXCEL = HERE / "Temperatura-precipitatii_1961-1990.xlsx"
if not EXCEL.exists():
    raise FileNotFoundError(f"Fișierul {EXCEL.name} nu a fost găsit în {HERE}")

df_raw = pd.read_excel(EXCEL, engine="openpyxl")
firstcol = df_raw.columns[0]
df = df_raw.set_index(firstcol).apply(pd.to_numeric, errors="coerce")

years = df.columns.astype(int)
temp = df.iloc[0].values  # temperatura medie anuală
prec = df.iloc[1].values  # precipitații totale anuale

# === 2. Figură & 2 axe ========================================
fig, ax_t = plt.subplots(figsize=(12, 6))
ax_p = ax_t.twinx()

ax_p.set_zorder(1)            # precipitații fundal
ax_t.set_zorder(2)            # temperatură prim-plan
ax_t.patch.set_visible(False)

# === 3. Desenează datele =====================================
mask = ~np.isnan(prec)
ax_p.bar(years[mask], prec[mask],
         width=0.6, color="#5bc0de", alpha=0.8,
         label="Precipitaţii 1961-1990")

ax_t.plot(years, temp,
          color="#d9534f", linestyle="--", marker="o", linewidth=2.2,
          label="Temp 1961-1990")

# === 4. Setări scală & estetică ==============================
ax_t.set_ylim(9.5, 14)
ax_p.set_ylim(0, 800)

ax_t.set_xlabel("An")
ax_t.set_ylabel("Temperatura medie (°C)", color="#d9534f")
ax_p.set_ylabel("Precipitaţii anuale (mm)", color="#5bc0de")

ax_t.tick_params(axis="y", colors="#d9534f")
ax_p.tick_params(axis="y", colors="#5bc0de")
ax_t.grid(True, linestyle=":", linewidth=0.5, alpha=0.6)

ax_t.set_title("Climogramă multianuală 1961-1990\n(Temperatură vs. Precipitaţii)",
               fontsize=14, fontweight="bold")

# Legendă comună
h1, l1 = ax_t.get_legend_handles_labels()
h2, l2 = ax_p.get_legend_handles_labels()
ax_t.legend(h1 + h2, l1 + l2, loc="upper left", frameon=False)

# === 5. Afișare și salvare automată ==========================
fig.tight_layout()
output_path = HERE / "Climograma_1961-1990.png"
fig.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"✅ Grafic salvat: {output_path.name}")

plt.show()
