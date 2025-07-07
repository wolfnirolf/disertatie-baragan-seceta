import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === 1. Încarcă datele din fișier Excel ===================
excel_file = "Date-climatologice-sezoane-extinse.xlsx"
df = pd.read_excel(excel_file, sheet_name="Foaie1")

# Ordonăm după sezon și perioadă (rece/cald, 1961–1990 / 1991–2020)
df = df.sort_values(by=["Sezon", "Perioada"], ascending=[True, True])

# Extragem valorile în ordinea corectă (rece → cald)
temp_1961_1990 = df[df["Perioada"] == "1961-1990"]["Temperatura"].values[::-1]
temp_1991_2020 = df[df["Perioada"] == "1991-2020"]["Temperatura"].values[::-1]
prec_1961_1990 = df[df["Perioada"] == "1961-1990"]["Precipitatii"].values[::-1]
prec_1991_2020 = df[df["Perioada"] == "1991-2020"]["Precipitatii"].values[::-1]

labels = ["Sezon rece", "Sezon cald"]
x = np.arange(len(labels))
width = 0.35

# === 2. Figură și axe ======================================
fig, ax_precip = plt.subplots(figsize=(8, 6))
ax_temp = ax_precip.twinx()
ax_temp.patch.set_alpha(0)  # fundal transparent

# === 3. Desenăm graficele ==================================
# Bare (precipitații)
ax_precip.bar(x - width/2, prec_1961_1990, width, label="Prec. 1961-1990", color="#add8e6")
ax_precip.bar(x + width/2, prec_1991_2020, width, label="Prec. 1991-2020", color="#00008b")

# Linii (temperaturi)
ax_temp.plot(x, temp_1961_1990, label="Temp. 1961-1990", color="brown", linestyle="--", marker="o")
ax_temp.plot(x, temp_1991_2020, label="Temp. 1991-2020", color="red", linestyle="--", marker="o")

# === 4. Anotări pentru temperaturi ==========================
# Perioada 1991–2020: deasupra, ușor spre stânga
for i, (tx, ty) in enumerate(zip(x, temp_1991_2020)):
    ax_temp.annotate(f"{ty:.1f}°C", (tx, ty),
                     xytext=(-12, 6), textcoords="offset points",
                     ha="right", va="bottom", fontsize=8,
                     color="red",
                     bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.6))

# Perioada 1961–1990: dedesubt, diferențiat
for i, (tx, ty) in enumerate(zip(x, temp_1961_1990)):
    offset_x = -12 if ty < 10 else 12
    align = "right" if ty < 10 else "left"
    ax_temp.annotate(f"{ty:.1f}°C", (tx, ty),
                     xytext=(offset_x, -10), textcoords="offset points",
                     ha=align, va="top", fontsize=8,
                     color="brown",
                     bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.6))

# === 5. Stilizare generală ================================
ax_temp.yaxis.set_label_position("left")
ax_temp.yaxis.tick_left()
ax_precip.yaxis.set_label_position("right")
ax_precip.yaxis.tick_right()

ax_temp.set_ylabel("Temperatura medie °C", color="darkred")
ax_precip.set_ylabel("Precipitaţii mm", color="navy")
ax_temp.set_ylim(0, 22)
ax_precip.set_ylim(0, 320)
ax_temp.set_xticks(x)
ax_temp.set_xticklabels(labels)
ax_temp.grid(True, which="both", axis="y", linestyle=":", linewidth=0.5, color="lightgray")

plt.title("Analiza comparativă a regimului climatic în Câmpia Bărăganului\n"
          "Sezoane extinse (1961–2020)", fontsize=12)

# === 6. Legendă ============================================
h1, l1 = ax_temp.get_legend_handles_labels()
h2, l2 = ax_precip.get_legend_handles_labels()
ax_temp.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=9, frameon=True)

# === 7. Salvare grafic =====================================
plt.tight_layout()
plt.savefig("grafic_climat_sezoane_extinse_Campie_Baragan.png", dpi=300, bbox_inches="tight")
plt.show()
