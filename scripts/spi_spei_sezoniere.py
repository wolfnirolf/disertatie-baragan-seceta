import pandas as pd
import matplotlib.pyplot as plt
import os

# === 1. Încarcă datele
df = pd.read_excel("Rezultate_SPI3_SPEI3_6statii.xlsx")

# === 2. Atribuie anotimpul
def map_luna_la_anotimp(luna):
    if luna in [12, 1, 2]:
        return "Iarnă"
    elif luna in [3, 4, 5]:
        return "Primăvară"
    elif luna in [6, 7, 8]:
        return "Vară"
    else:
        return "Toamnă"

df["Anotimp"] = df["Luna"].apply(map_luna_la_anotimp)

# === 3. Setări stil
culori = {"SPI-3": "#F57C00", "SPEI-3": "#005288"}
etichete = {"SPI-3": "#5e0000", "SPEI-3": "#003049"}
output_dir = "grafice_spi_spei_sezoniere_custom"
os.makedirs(output_dir, exist_ok=True)

# === 4. Stații speciale pentru ajustări
sp_primavara = {
    "SPI-3_top": ["Buzau", "Focsani"],
    "SPEI-3_bottom": ["Calarasi", "Fetesti", "Harsova", "Medgidia", "Tulcea"],
    "SPI-3_bottom": ["Calarasi", "Fetesti", "Medgidia", "Tulcea"]
}

sp_toamna = {
    "SPEI-3_bottom": "ALL",
    "SPI-3_bottom": "ALL"
}

# === 5. Generează grafice
for anotimp in ["Primăvară", "Vară", "Toamnă", "Iarnă"]:
    df_sezon = df[df["Anotimp"] == anotimp]
    medii = df_sezon.groupby("Statie")[["SPI-3", "SPEI-3"]].mean().round(2)
    statii = medii.index.tolist()
    x = range(len(statii))

    plt.figure(figsize=(14, 6))
    b1 = plt.bar([i - 0.2 for i in x], medii["SPEI-3"], width=0.4, label="SPEI-3", color=culori["SPEI-3"])
    b2 = plt.bar([i + 0.2 for i in x], medii["SPI-3"], width=0.4, label="SPI-3", color=culori["SPI-3"])

    # === 6. Afișează etichete numerice
    for i, st in enumerate(statii):
        for idx, ind in zip([-0.2, 0.2], ["SPEI-3", "SPI-3"]):
            val = medii.loc[st, ind]
            xpos = i + idx
            color = etichete[ind]

            # Ajustări speciale
            if anotimp == "Primăvară":
                if ind == "SPI-3" and st in sp_primavara["SPI-3_top"]:
                    ha, va, dy = 'center', 'bottom', 0.005
                elif ind == "SPEI-3" and st in sp_primavara["SPEI-3_bottom"]:
                    ha, va, dy = 'center', 'top', -0.008
                elif ind == "SPI-3" and st in sp_primavara["SPI-3_bottom"]:
                    ha, va, dy = 'center', 'top', -0.008
                else:
                    ha, va, dy = 'center', 'bottom' if val >= 0 else 'top', 0.01 * (1 if val >= 0 else -1)
            elif anotimp == "Toamnă":
                if sp_toamna[ind + "_bottom"] == "ALL":
                    ha, va, dy = 'center', 'top', -0.008
                else:
                    ha, va, dy = 'center', 'bottom' if val >= 0 else 'top', 0.01 * (1 if val >= 0 else -1)
            else:
                ha, va, dy = 'center', 'bottom' if val >= 0 else 'top', 0.01 * (1 if val >= 0 else -1)

            plt.text(xpos, val + dy, f"{val:.2f}", ha=ha, va=va, fontsize=8, color=color)

    # === 7. Stil grafic
    plt.axhline(0, color='gray', linestyle='--', linewidth=1)
    plt.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.4)
    plt.title(f"Compararea valorilor medii SPEI-3 și SPI-3 în {anotimp} (1961–2020)", fontsize=13)
    plt.ylabel("Valori medii (1961–2020)", fontsize=11)
    plt.xlabel("Stații", fontsize=11)
    plt.xticks(x, statii, rotation=45, ha='right')
    plt.legend(title="Indicator", loc="upper left")
    plt.tight_layout()

    out_path = os.path.join(output_dir, f"grafic_{anotimp.lower()}.png")
    plt.savefig(out_path, dpi=300)
    plt.close()

print(f"✅ Graficele au fost salvate în folderul: {output_dir}")
