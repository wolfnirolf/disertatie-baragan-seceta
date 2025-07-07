import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# 1. Încarcă fișierul
df = pd.read_excel("Temp-medii-pe-anotimp_1961-2020.xlsx")
df.columns = df.columns.str.strip()
df = df.set_index("An")

# 2. Setup figură
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Evoluția temperaturilor sezoniere și trendurile pe termen lung – Câmpia Bărăganului (1961–2020)", fontsize=14)
plt.subplots_adjust(wspace=0.15)

# 3. Configuri
sezoane    = ["Iarna", "Primăvara", "Vara", "Toamna"]
culori     = ["#274472", "#1B5E20", "#7B1FE0", "#4E342E"]
pozitii    = {(0, 0): "Iarna", (0, 1): "Primăvara", (1, 0): "Vara", (1, 1): "Toamna"}
ghidaj_y   = {"Iarna": -4, "Primăvara": 8, "Vara": 20, "Toamna": 9}
xticks_maj = [1961, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020]
all_years  = list(range(1961, 2021))
xticks_min = [y for y in all_years if y not in xticks_maj and y != 2014]

def brighten(hexcol, factor=0.1):
    rgb = np.array(mcolors.to_rgb(hexcol))
    return tuple((1 - factor) * rgb + factor)

# 4. Plot
for (i, j), sezon in pozitii.items():
    ax = axs[i, j]
    y = df[sezon]
    x = df.index
    col = brighten(culori[i * 2 + j], 0.1) if sezon == "Toamna" else culori[i * 2 + j]

    # Temperatură medie
    ax.plot(x, y, lw=1.8, color=col, label="Temperatură medie")

    # Trend
    mask = ~y.isna()
    z = np.polyfit(x[mask], y[mask], 1)
    ax.plot(x, np.poly1d(z)(x), ls="--", lw=2, color="#C62828", label="Trend")

    # Limite axă
    y_base, y_top = ax.get_ylim()
    x_base, x_top = ax.get_xlim()

    # Linii verticale (ghidaj ani)
    for year in xticks_maj:
        ax.vlines(year, ymin=y_base, ymax=y_top, color="#dddddd", linestyle='-', linewidth=0.8, zorder=0)

    # Linii orizontale punctate personalizate (de la praguri)
    start_y = ghidaj_y.get(sezon, 0)
    step = 1  # pas fin pentru temperaturi
    for yval in np.arange(start_y, y_top, step):
        if abs(yval) > 1e-2:  # evită suprapunere cu axa X (0)
            ax.hlines(yval, xmin=x_base, xmax=x_top, color="#dddddd", linestyle='--', linewidth=0.8, zorder=0)

    # Mini-segmente între ani
    for yr in xticks_min:
        ax.plot([yr, yr], [-0.02, 0.02], transform=ax.get_xaxis_transform(), color="gray", lw=0.5)

    # 2014
    if 2014 in x:
        txt = ax.text(2014, 0.02, "2014 - lipsă date",
                      rotation=90, ha="center", va="bottom",
                      color="gray", fontsize=8,
                      transform=ax.get_xaxis_transform())

        fig.canvas.draw()
        bbox = txt.get_window_extent(fig.canvas.get_renderer())
        y_text_top = ax.transData.inverted().transform((0, bbox.y1))[1]
        pad = (y_top - y_base) * 0.01

        ax.vlines(2014, ymin=y_text_top + pad, ymax=y_top, linestyle="--", linewidth=1, color="gray")

        if not pd.isna(y.loc[2014]):
            ax.hlines(y=y.loc[2014], xmin=2013.5, xmax=2014.5, linestyle=':', color='gray', linewidth=1)

    # Axa X, Y, titlu, legendă
    ax.set_xticks(xticks_maj)
    ax.set_xticklabels(xticks_maj, rotation=45)
    ax.set_ylabel("°C")
    ax.set_title(sezon)
    ax.legend(loc="upper center", fontsize=9, ncol=2, frameon=False)

# 5. Finalizare
plt.tight_layout(rect=(0, 0.03, 1, 0.95))
plt.savefig("temperaturi_sezoniere_1961-2020.png", dpi=300)
plt.show()
