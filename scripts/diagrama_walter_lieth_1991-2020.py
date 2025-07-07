#!/usr/bin/env python3
"""
Generate a Walter-Lieth climate diagram (1991-2020).

Usage
-----
python diagrama_walter_lieth_1991-2020.py           # afișează interactiv
python diagrama_walter_lieth_1991-2020.py -o figura.png
"""

import argparse, os, sys
import numpy as np, pandas as pd, matplotlib.pyplot as plt


def build_diagram(df: pd.DataFrame) -> plt.Figure:
    # ── Extragem seriile lunare ────────────────────────────────────────────────
    t_medie = df.loc["T medie"].values.astype(float)
    t_max   = df.loc["T maxima"].values.astype(float)
    t_min   = df.loc["T minima"].values.astype(float)
    precip  = df.loc["Precipitatii"].values.astype(float)

    months = np.arange(1, 13)
    labels = ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"]

    # ── Limite axe (actualizate) ───────────────────────────────────────────────
    temp_min_lim, temp_max_lim = -10, 35          # ### MOD  ↑35 °C
    frac_0 = (0 - temp_min_lim) / (temp_max_lim - temp_min_lim)

    precip_max_lim = 100                          # ### MOD  ↑100 mm
    precip_min_lim = -(frac_0 * precip_max_lim) / (1 - frac_0)

    # ── Figură & axe ───────────────────────────────────────────────────────────
    fig, ax_t = plt.subplots(figsize=(11, 6))
    ax_p = ax_t.twinx()

    p_color = "#9ecde6"

    # 1) Precipitații (fill + contur)
    ax_p.fill_between(months, 0, precip, color=p_color, alpha=0.6, zorder=0)
    ax_p.plot(months, precip, color=p_color, lw=2, label="Precipitații", zorder=1)

    # 2) Temperaturile
    ax_t.plot(months, t_min,   color="grey",   lw=1.6, ls="--",               label="T minima", zorder=3)
    ax_t.plot(months, t_medie, color="black",  lw=2.2,                         label="T medie",  zorder=4)
    ax_t.plot(months, t_max,   color="sienna", lw=3,   ls=(0, (5, 5)),         label="T maxima", zorder=3.5)

    # 3) Linia roșie de zero
    ax_t.axhline(0, color="red", lw=1.2, zorder=5)

    # ── Config axe & gradații ─────────────────────────────────────────────────
    ax_t.set_ylim(temp_min_lim, temp_max_lim)
    ax_p.set_ylim(precip_min_lim, precip_max_lim)

    ax_t.set_yticks(np.arange(temp_min_lim, temp_max_lim + 5, 5))     # ### MOD
    ax_p.set_yticks([0, 20, 40, 60, 80, 100])                         # ### MOD
    ax_p.set_yticklabels([str(v) for v in ax_p.get_yticks()])

    ax_t.set_xticks(months); ax_t.set_xticklabels(labels)

    ax_t.set_ylabel("Temperatura aerului (°C)")
    ax_p.set_ylabel("Precipitații (mm)")
    ax_t.grid(True, which="both", ls=":", lw=0.5, zorder=0)

    # ── Legendă & titlu ───────────────────────────────────────────────────────
    h_t, l_t = ax_t.get_legend_handles_labels()
    h_p, l_p = ax_p.get_legend_handles_labels()
    ax_t.legend(h_p + h_t, l_p + l_t,
                title="Legendă", loc="upper left", frameon=True)

    fig.suptitle("Diagrama Walter-Lieth (1991-2020)",
                 fontsize=14, fontweight="bold")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig


def main():
    ap = argparse.ArgumentParser(description="Walter-Lieth diagram generator")
    ap.add_argument("-i", "--input",
                    default="Date-climatologice-1991-2020.xlsx",
                    help="Excel file with climatological data (default: %(default)s)")
    ap.add_argument("-o", "--output",
                    help="Output image file (png, svg, pdf …). "
                         "If omitted, the diagram is shown interactively.")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        sys.exit(f"Nu am găsit fișierul: {args.input}")

    df = pd.read_excel(args.input, engine="openpyxl").set_index("Indicator")
    fig = build_diagram(df)

    if args.output:
        fig.savefig(args.output, dpi=300, bbox_inches="tight")
        print(f"Figura salvată în {args.output}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
