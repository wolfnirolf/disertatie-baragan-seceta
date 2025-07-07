import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
#  Fișiere sursă (schimbă doar dacă le muți)
# --------------------------------------------------
F_6190 = Path("Date-climatologice-sezon-rece-extins_1961-1990.xlsx")
F_9120 = Path("Date-climatologice-sezon-rece-extins_1991-2020.xlsx")

# --------------------------------------------------
#  Citește fișierul: rândul 1 = "Luna 10 11 12 1 2 3"
# --------------------------------------------------
def load_file(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, header=1)         # header=1 -> rândul „Luna …”
    df.rename(columns={df.columns[0]: "Indicator"}, inplace=True)
    # convertează capetele de coloană la int (10,11…)
    new_cols = []
    for c in df.columns:
        try:
            new_cols.append(int(c))
        except (ValueError, TypeError):
            new_cols.append(c)
    df.columns = new_cols
    df.set_index("Indicator", inplace=True)
    return df

df_6190 = load_file(F_6190)
df_9120 = load_file(F_9120)

# --------------------------------------------------
#  Luni: octombrie – martie
# --------------------------------------------------
luni           = [10, 11, 12, 1, 2, 3]
etichete_luni  = ["Octombrie", "Noiembrie", "Decembrie", "Ianuarie", "Februarie", "Martie"]
x              = range(len(luni))
width          = 0.35

temp_6190 = df_6190.loc["Temperatura",  luni].values
temp_9120 = df_9120.loc["Temperatura",  luni].values
prec_6190 = df_6190.loc["Precipitatii", luni].values
prec_9120 = df_9120.loc["Precipitatii", luni].values

# --------------------------------------------------
#  Figură şi axe
# --------------------------------------------------
fig, ax1 = plt.subplots(figsize=(10, 5))         # axă temperatură (stânga)
ax2 = ax1.twinx()                                # axă precipitaţii (dreapta)

# --- limite
y1min, y1max = -5, 15
ax1.set_ylim(y1min, y1max)
y2min, y2max = 0, max(prec_6190.max(), prec_9120.max()) + 10
ax2.set_ylim(y2min, y2max)

# --- conversie precipitaţii -> coordonate ax1
def scale_p(val):
    return y1min + (val - y2min) * (y1max - y1min) / (y2max - y2min)

prec_6190_scaled = [scale_p(p) for p in prec_6190]
prec_9120_scaled = [scale_p(p) for p in prec_9120]

# --- grid fin
for y in range(y1min, y1max + 1):
    ax1.axhline(y, ls=":",  lw=0.5, color="#D2B48C", zorder=0)   # temperatură
for y in range(10, int(y2max)+1, 10):
    ax1.axhline(scale_p(y), ls="--", lw=0.5, color="lightgray", zorder=0)  # precipitaţii

# --- temperatură (în faţă)
ax1.plot(x, temp_6190, marker='o', ls='--', label="Temp. 1961-1990",
         color="orange", zorder=3)
ax1.plot(x, temp_9120, marker='o', ls='-',  label="Temp. 1991-2020",
         color="red",    zorder=3)
ax1.set_ylabel("Temperatura medie (°C)", color="red")
ax1.set_xticks(x)
ax1.set_xticklabels(etichete_luni)

# --- precipitaţii (bare în fundal, pe ax1 dar scalate)
ax1.bar([i - width/2 for i in x], prec_6190_scaled, width,
        label="Prec. 1961-1990", color="#4682B4", zorder=1)
ax1.bar([i + width/2 for i in x], prec_9120_scaled, width,
        label="Prec. 1991-2020", color="#1E3F66", zorder=1)
ax2.set_ylabel("Precipitații medii (mm/lună)", color="blue")

# --- legendă
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles, labels, loc="upper right", title="Legenda")

# --- titlu & export
plt.title("Analiza regimului climatic în Câmpia Bărăganului – sezon rece extins (octombrie-martie)")
plt.tight_layout()
plt.savefig("sezon_rece_extins_Baragan.png", dpi=300)
plt.show()
