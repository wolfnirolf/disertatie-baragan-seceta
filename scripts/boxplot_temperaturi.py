#!/usr/bin/env python3
"""
Box-plot al temperaturilor medii anuale (medie pe stații)
pentru cele două norme climatologice:

    • 1961-1990  – Temperatura-precipitatii_1961-1990.xlsx
    • 1991-2020  – Temperatura-precipitatii_1991-2020.xlsx

Graficul comprimă cei 30 × 2 ani la distribuții comparabile (mediană, IQR, outlier-e).

Rulare:
    python boxplot_temperaturi.py
    python boxplot_temperaturi.py -o temp_box.png   # salvează imaginea
"""

from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ───────── 1. fișierele Excel (în același folder) ───────────────────────────
HERE   = Path(__file__).resolve().parent
FILE_A = HERE / "Temperatura-precipitatii_1961-1990.xlsx"
FILE_B = HERE / "Temperatura-precipitatii_1991-2020.xlsx"

for f in (FILE_A, FILE_B):
    if not f.exists():
        sys.exit(f"{f.name} nu a fost găsit în {HERE}")

# ───────── 2. funcție extragere temperaturi ─────────────────────────────────
def extract_temp(path: Path) -> np.ndarray:
    """
    Returnează vectorul temperaturilor medii anuale pentru fișierul dat.
    Presupunem că rândul 0 = T medie, conform fișierelor precedente.
    """
    df  = pd.read_excel(path, engine="openpyxl")
    df  = df.set_index(df.columns[0])              # prima coloană drept index
    ser = pd.to_numeric(df.iloc[0], errors="coerce")  # rând 0 = T medie
    return ser.dropna().values

temp_1961_1990 = extract_temp(FILE_A)
temp_1991_2020 = extract_temp(FILE_B)

# ───────── 3. box-plot ──────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))

box = ax.boxplot(
        [temp_1961_1990, temp_1991_2020],
        patch_artist=True,
        tick_labels=["1961-1990", "1991-2020"],
        widths=0.6)

# culori cutii
colors = ["#d9534f", "#f0ad4e"]   # roșu cărămiziu & portocaliu cald
for patch, col in zip(box["boxes"], colors):
    patch.set_facecolor(col)
    patch.set_alpha(0.8)

# mediane vizibile
for median in box["medians"]:
    median.set(color="black", linewidth=2)

ax.set_ylabel("Temperaturi Medii Anuale (°C)")
ax.set_title("Distribuția Temperaturilor Medii Anuale\n(1961-1990 vs. 1991-2020)",
             fontsize=13, fontweight="bold")
ax.grid(axis="y", linestyle=":", linewidth=0.5, alpha=0.6)

fig.tight_layout()

# ───────── 4. afișare / salvare ─────────────────────────────────────────────

# Salvare automată și afișare
fig.tight_layout()
fig.savefig("boxplot_temperaturi.png", dpi=300, bbox_inches="tight")
print("✅ Grafic salvat: boxplot_temperaturi.png")
plt.show()