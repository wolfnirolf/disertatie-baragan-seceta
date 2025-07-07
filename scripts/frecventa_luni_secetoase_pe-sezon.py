#!/usr/bin/env python3
"""Generare grafic – Frecvența lunilor secetoase pe anotimpuri (Câmpia Bărăganului)
   * Indicator Hellmann, 1961‑2020
   * Subplot‑uri în ordinea: Iarna, Primăvara, Vara, Toamna (stânga‑dreapta / sus‑jos)
   * Gap vizual în 2014 (lipsă date)
   * Spaţiu suplimentar deasupra liniei de 100 % (axe y extinsă la 110 %)
   * Linia de trend: roşu‑purpuriu (vizibilă)

   Salvare: grafic_frecventa_anotimpuri_baragan.png (DPI 300)
"""

from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# Paletă culori (linie, umplere) & trend line
# -----------------------------------------------------------------------------
CULOARE = {
    "Iarna":     ("royalblue",  "#87CEFA"),   # linie, fill
    "Primăvara": ("forestgreen", "#90EE90"),
    "Vara":      ("darkorange",  "#FFD580"),
    "Toamna":    ("sienna",      "#D2B48C"),
}
TREND_COLOR = "#c2185b"        # roşu‑purpuriu saturat, foarte vizibil
TREND_WIDTH = 2.5

# -----------------------------------------------------------------------------
# 1. Citirea / pregătirea datelor
# -----------------------------------------------------------------------------

def citeste_date(path: str | Path = "Calcul_frecventa_luni-secetoase_pe-anotimp_pas2.xlsx") -> pd.DataFrame:
    """Returnează un *DataFrame* cu anii 1961‑2020 + procente lunilor secetoase.
    Anul **2014** este setat la *NaN* pentru toate anotimpurile → gap vizual.
    """

    df = pd.read_excel(path)

    # verificare coloane
    expected: List[str] = ["An", "Primăvara", "Vara", "Toamna", "Iarna"]
    missing = [c for c in expected if c not in df.columns]
    if missing:
        raise ValueError(
            "Coloane lipsă în fişierul sursă: " + ", ".join(missing)
        )

    df["An"] = df["An"].astype(int)
    for col in expected[1:]:
        df[col] = df[col].astype(float)

    # serie continuă 1961‑2020
    serie = pd.DataFrame({"An": range(1961, 2021)})
    df_full = serie.merge(df, on="An", how="left")

    # forţăm NaN pe 2014
    mask2014 = df_full["An"] == 2014
    df_full.loc[mask2014, expected[1:]] = np.nan

    return df_full

# -----------------------------------------------------------------------------
# 2. Desenarea subplot‑urilor
# -----------------------------------------------------------------------------

def deseneaza(df: pd.DataFrame) -> None:
    plt.figure(figsize=(14, 9))

    # ordinea dorită Iarna, Primăvara, Vara, Toamna
    anotimpuri = ["Iarna", "Primăvara", "Vara", "Toamna"]

    for i, sezon in enumerate(anotimpuri, start=1):
        ax = plt.subplot(2, 2, i)

        x = df["An"].values
        y = (df[sezon] * 100).values  # fracţie → procente

        culoare_lin, culoare_fill = CULOARE[sezon]

        # serie principală (NaN‑urile rup linia)
        ax.plot(
            x,
            y,
            "o-",
            color=culoare_lin,
            linewidth=2.2,
            label=f"% luni secetoase – {sezon}",
        )

        # umplere până la zero (doar date valide)
        ax.fill_between(
            x,
            0,
            y,
            where=~np.isnan(y),
            step="mid",
            color=culoare_fill,
            alpha=0.4,
        )

        # linia de trend
        ok = ~np.isnan(y)
        if ok.sum() >= 2:
            coef = np.polyfit(x[ok], y[ok], 1)
            trend = np.poly1d(coef)
            ax.plot(
                x,
                trend(x),
                "--",
                color=TREND_COLOR,
                linewidth=TREND_WIDTH,
                label=f"Trend: y = {coef[0]:+.02f}x + {coef[1]:.1f}",
            )

        # axă Y: 0‑110 (spaţiu >100 %) sau 15 % peste maxim dacă depăşeşte 100
        ymax = np.nanmax(y)
        ytop = 110 if ymax <= 100 else ymax * 1.15
        ax.set_ylim(0, ytop)

        # cosmetizare
        ax.set_title(sezon)
        ax.set_ylabel("% luni secetoase")
        ax.grid(True, linestyle=":", linewidth=0.7)
        ax.legend()

    # titlu general & layout
    plt.suptitle(
        "Frecvenţa lunilor secetoase pe anotimpuri în Câmpia Bărăganului\n"
        "(Indicatori Hellmann, 1961‑2020)",
        fontsize=14,
    )

    plt.tight_layout(rect=[0, 0.03, 1, 0.94])

    out = Path("grafic_frecventa_luni_secetoase_pe-anotimpuri.png")
    plt.savefig(out, dpi=300)
    print(f"[✔] Grafic salvat: {out.resolve()}")
    plt.show()

# -----------------------------------------------------------------------------
# 3. Punct de intrare
# -----------------------------------------------------------------------------

def main() -> None:
    df = citeste_date()
    deseneaza(df)


if __name__ == "__main__":
    main()
