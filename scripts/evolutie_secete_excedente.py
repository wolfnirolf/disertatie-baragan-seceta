import pandas as pd
import matplotlib.pyplot as plt

# Încarcă fișierul Excel
file_path = "Rezultate_SPI3_SPEI3_6statii.xlsx"  # Asigură-te că e în același folder
df = pd.read_excel(file_path)

# Clasificare categorii pe baza SPI-3
def clasificare_spi3(val):
    if val <= -1.5:
        return "Secetă Severă"
    elif -1.5 < val <= -1.0:
        return "Secetă Moderată"
    elif val >= 1.0:
        return "Excedent Pluviometric"
    else:
        return "Normal"

df["Categorie"] = df["SPI-3"].apply(clasificare_spi3)

# Grupare: număr de cazuri pe an și categorie
count_data = df.groupby(["An", "Categorie"]).size().unstack(fill_value=0)

# Adaugă anul 2014 cu valori NaN pentru gap
if 2014 not in count_data.index:
    count_data.loc[2014] = [None] * count_data.shape[1]
count_data = count_data.sort_index()

# Culori pentru categorii
culori = {
    "Secetă Severă": "#D62828",
    "Secetă Moderată": "#F77F00",
    "Excedent Pluviometric": "#005288"
}

# Plot
plt.figure(figsize=(14, 6))
for categorie in ["Secetă Severă", "Secetă Moderată", "Excedent Pluviometric"]:
    if categorie in count_data.columns:
        plt.plot(count_data.index, count_data[categorie],
                 label=categorie, marker='o', linewidth=1.5,
                 color=culori[categorie])

# Evidențiere an 2014
plt.axvline(x=2014, color='gray', linestyle='--', alpha=0.6)
plt.text(2014, plt.ylim()[1]*0.95, '2014\n(lipsă date)', rotation=90,
         color='gray', fontsize=9, ha='center', va='top')

# Stilizare
plt.title("Evoluția Secetelor și Excedentului Pluviometric pe Ani (1961–2020)", fontsize=14)
plt.xlabel("An", fontsize=12)
plt.ylabel("Număr de Sezoane", fontsize=12)
plt.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.4)
plt.legend(title="Categorie")
plt.tight_layout()

# Salvare imagine
plt.savefig("grafic_evolutie_secete_excedente.png", dpi=300)
plt.show()
