import pandas as pd
import matplotlib.pyplot as plt

# === Încărcare fișiere Excel (header pe rândul 4)
df_6190 = pd.read_excel("Date-climatologice-sezon-cald-extins_1961-1990.xlsx", header=3)
df_9120 = pd.read_excel("Date-climatologice-sezon-cald-extins_1991-2020.xlsx", header=3)
df_6190.set_index("Luna", inplace=True)
df_9120.set_index("Luna", inplace=True)

# === Luni aprilie–septembrie
luni = [4, 5, 6, 7, 8, 9]
etichete_luni = ["Aprilie", "Mai", "Iunie", "Iulie", "August", "Septembrie"]
x = range(len(luni))
width = 0.35

# === Extragere valori
temp_6190 = df_6190.loc["Temperatura", luni].values
temp_9120 = df_9120.loc["Temperatura", luni].values
prec_6190 = df_6190.loc["Precipitatii", luni].values
prec_9120 = df_9120.loc["Precipitatii", luni].values

# === Inițializare figură
fig, ax1 = plt.subplots(figsize=(10, 5))

# Limite temperatură
y1min, y1max = 10, 25
ax1.set_ylim(y1min, y1max)

# Axa dreaptă (precipitații)
ax2 = ax1.twinx()
y2min, y2max = 0, max(prec_6190.max(), prec_9120.max()) + 10
ax2.set_ylim(y2min, y2max)

# === Funcție scalare precipitații pentru a fi desenate pe ax1
def scale_precip_to_ax1(val):
    return y1min + (val - y2min) * (y1max - y1min) / (y2max - y2min)

prec_6190_scaled = [scale_precip_to_ax1(p) for p in prec_6190]
prec_9120_scaled = [scale_precip_to_ax1(p) for p in prec_9120]

# === Linii orizontale fine
for y in range(y1min, y1max + 1):
    ax1.axhline(y, color="#D2B48C", linestyle=":", linewidth=0.5, zorder=0)  # maro deschis

for y in range(10, int(y2max) + 1, 10):
    y_scaled = scale_precip_to_ax1(y)
    ax1.axhline(y_scaled, color="lightgray", linestyle="--", linewidth=0.5, zorder=0)

# === Temperatură – linii
ax1.plot(x, temp_6190, marker='o', linestyle='--',
         label="Temp. 1961–1990", color="orange", zorder=3)
ax1.plot(x, temp_9120, marker='o', linestyle='-',
         label="Temp. 1991–2020", color="red", zorder=3)
ax1.set_ylabel("Temperatura medie (°C)", color="red")
ax1.set_xticks(x)
ax1.set_xticklabels(etichete_luni)

# === Precipitații – bare (pe axa stângă, dar scalate)
ax1.bar([i - width/2 for i in x], prec_6190_scaled, width=width,
        label="Prec. 1961–1990", color="#4682B4", zorder=1)
ax1.bar([i + width/2 for i in x], prec_9120_scaled, width=width,
        label="Prec. 1991–2020", color="#1E3F66", zorder=1)

# === Legendă
ax2.set_ylabel("Precipitații medii (mm/lună)", color="blue")
l1, lab1 = ax1.get_legend_handles_labels()
ax1.legend(l1, lab1, loc="upper left", title="Legenda")

# === Titlu și salvare
plt.title("Analiza regimului climatic în Câmpia Bărăganului – sezon cald extins (aprilie–septembrie)")
plt.tight_layout()
plt.savefig("sezon_cald_extins_Bragan.png", dpi=300)
plt.show()
