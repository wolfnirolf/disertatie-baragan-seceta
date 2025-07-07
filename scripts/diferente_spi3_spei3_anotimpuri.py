import pandas as pd
import matplotlib.pyplot as plt

# === 1. Încarcă datele
df = pd.read_excel("Rezultate_SPI3_SPEI3_6statii.xlsx")

# === 2. Adaugă coloana „Anotimp”
def map_anotimp(luna):
    if luna in [12, 1, 2]:
        return "Iarnă"
    elif luna in [3, 4, 5]:
        return "Primăvară"
    elif luna in [6, 7, 8]:
        return "Vară"
    elif luna in [9, 10, 11]:
        return "Toamnă"

df["Anotimp"] = df["Luna"].apply(map_anotimp)

# === 3. Diferența SPI - SPEI și medie pe anotimp
df["Dif_SPI_SPEI"] = df["SPI-3"] - df["SPEI-3"]
df_grouped = df.groupby("Anotimp")["Dif_SPI_SPEI"].mean().reindex(["Primăvară", "Vară", "Toamnă", "Iarnă"])

# === 4. Creare grafic
plt.figure(figsize=(10, 6))
bars = plt.bar(df_grouped.index, df_grouped.values, color="#005288", width=0.5)
plt.axhline(0, color="gray", linestyle="--", linewidth=1.2)

# === 5. Afișare valori personalizate
for i, bar in enumerate(bars):
    val = bar.get_height()
    anotimp = df_grouped.index[i]

    if anotimp == "Vară":
        plt.text(bar.get_x() + bar.get_width() + 0.05, val / 2,
                 f"{val:.2f}", ha='left', va='center', fontsize=9, color="#003049")
    elif anotimp == "Iarnă":
        plt.text(bar.get_x() - 0.05, val / 2,
                 f"{val:.2f}", ha='right', va='center', fontsize=9, color="#003049")
    else:
        plt.text(bar.get_x() + bar.get_width()/2,
                 val + 0.015 if val >= 0 else val - 0.025,
                 f"{val:.2f}", ha='center', va='center', fontsize=9, color="#003049")

# === 6. Stil grafic
plt.title("Diferența medie SPI-3 – SPEI-3 pe anotimpuri (1961–2020)", fontsize=14)
plt.ylabel("Diferență medie SPI–SPEI", fontsize=12)
plt.xlabel("Anotimp", fontsize=12)
plt.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.4)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.tight_layout()

# === 7. Salvare
plt.savefig("grafic_diferente_spi3_spei3_anotimpuri.png", dpi=300)
plt.show()
