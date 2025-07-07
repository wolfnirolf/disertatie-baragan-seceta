#!/usr/bin/env python3
"""
Box-plot al precipitaţiilor anuale (medii pe staţii)
perioade climatologice:
   • 1961-1990  – fişier: Temperatura-precipitatii_1961-1990.xlsx
   • 1991-2020  – fişier: Temperatura-precipitatii_1991-2020.xlsx

Rulare:
    python boxplot_precipitatii.py              # afişează interactiv
    python boxplot_precipitatii.py -o box.png    # salvează imaginea
"""

from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ────────────────── 1. fişiere ───────────────────────────────────────────────
HERE   = Path(__file__).resolve().parent
FILE_A = HERE / "Temperatura-precipitatii_1961-1990.xlsx"
FILE_B = HERE / "Temperatura-precipitatii_1991-2020.xlsx"

for f in (FILE_A, FILE_B):
    if not f.exists():
        sys.exit(f"{f.name} nu a fost găsit în {HERE}")

# ────────────────── 2. funcţie extragere precipitaţii ────────────────────────
def extract_precip(path: Path) -> np.ndarray:
    """Returnează vectorul precipitaţiilor anuale (Σ P) din fişier."""
    df  = pd.read_excel(path, engine="openpyxl")
    # prima coloană drept index (indiferent de antet)
    df  = df.set_index(df.columns[0])
    ser = pd.to_numeric(df.iloc[1], errors="coerce")   # rând 1 = Σ P
    return ser.dropna().values

prec_1961_1990 = extract_precip(FILE_A)
prec_1991_2020 = extract_precip(FILE_B)

# ────────────────── 3. box-plot ──────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))

box = ax.boxplot(
        [prec_1961_1990, prec_1991_2020],
        patch_artist=True,
        tick_labels=["1961-1990", "1991-2020"],   # ← fără warning
        widths=0.6)

# culori box-uri
colors = ["blue", "red"]
for patch, col in zip(box["boxes"], colors):
    patch.set_facecolor(col)
    patch.set_alpha(0.8)

# mediane mai vizibile
for median in box["medians"]:
    median.set(color="yellow", linewidth=2)

ax.set_ylabel("Precipitaţii Medii Anuale (mm)")
ax.set_title("Distribuţia Precipitaţiilor Medii Anuale\n(1961-1990 vs. 1991-2020)",
             fontsize=13, fontweight="bold")
ax.grid(axis="y", linestyle=":", linewidth=0.5, alpha=0.6)

fig.tight_layout()

# ────────────────── 4. afişare / salvare ─────────────────────────────────────

# Salvare automată și afișare
fig.tight_layout()
fig.savefig("boxplot_precipitatii.png", dpi=300, bbox_inches="tight")
print("✅ Grafic salvat: boxplot_precipitatii.png")
plt.show()