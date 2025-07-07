
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Încarcă datele
df = pd.read_excel("Date-6statii-precipitatii.xlsx")
df.rename(columns={"An_numeric": "An", "Luna_numeric": "Luna"}, inplace=True)

# Clasificare scor Hellmann
def scor_hellmann(p):
    if p < 5:
        return 1
    elif p < 10:
        return 2
    elif p < 20:
        return 3
    elif p < 40:
        return 4
    elif p < 60:
        return 5
    elif p < 100:
        return 6
    else:
        return 7

df["Scor_Hellmann"] = df["precip_total"].apply(scor_hellmann)

# Deviație standard anuală
dev_std_anual = df.groupby("An")["Scor_Hellmann"].std()

# Adaugă 2014 cu NaN pentru gap
if 2014 not in dev_std_anual.index:
    dev_std_anual.loc[2014] = np.nan
dev_std_anual = dev_std_anual.sort_index()

# Trend fără 2014
x = dev_std_anual.dropna().index.values
y = dev_std_anual.dropna().values
slope, intercept = np.polyfit(x, y, 1)
trend = slope * dev_std_anual.index.values + intercept

# Plot final
plt.figure(figsize=(10, 5))
plt.plot(dev_std_anual.index, dev_std_anual.values,
         color="#f87600", marker='o', linewidth=2.2, label="Deviație standard")
plt.plot(dev_std_anual.index, trend,
         linestyle='--', color="#002147", linewidth=1.5,
         label=f"Trend: y = {slope:.4f}x + {intercept:.2f}")

# Evidențiază 2014
plt.axvline(x=2014, color='gray', linestyle='--', alpha=0.6)
plt.text(2014, plt.ylim()[1]*0.97, "2014\n(lipsă date)", rotation=90,
         color='gray', fontsize=9, ha='center', va='top')

# Stil
plt.title("Evoluția variabilității lunare a scorurilor Hellmann în Câmpia Bărăganului (1961–2020)", fontsize=13)
plt.xlabel("Anul", fontsize=11)
plt.ylabel("Deviație standard (lună+stație)", fontsize=11)
plt.xticks(fontsize=9, fontweight='bold')
plt.yticks(fontsize=9, fontweight='bold')
plt.grid(True, linestyle=":", alpha=0.4)
plt.legend()
plt.tight_layout()

# Salvare imagine
plt.savefig("grafic_evolutie_hellmann_deviatie_standard_final.png", dpi=300)
plt.show()
