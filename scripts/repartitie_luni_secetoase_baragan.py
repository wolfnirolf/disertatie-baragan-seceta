import pandas as pd
import matplotlib.pyplot as plt

# Nume luni în limba română
luni_romana = ['Ianuarie', 'Februarie', 'Martie', 'Aprilie', 'Mai', 'Iunie',
               'Iulie', 'August', 'Septembrie', 'Octombrie', 'Noiembrie', 'Decembrie']

# Încarcă fișierul Excel
df = pd.read_excel("Date_6statii_cu_scor_hellmann_lunar.xlsx")

# Creează coloana Interval
df['Interval'] = pd.cut(df['An_numeric'], bins=[1960, 1990, 2020], labels=['1961–1990', '1991–2020'])

# Marcare luni secetoase (1 sau 2)
df['este_secetoasa'] = df['hellmann_score_lunar'].isin([1, 2])

# Calculează procentul lunilor secetoase
monthly_dry_ratio = df.groupby(['Interval', 'Luna_numeric'])['este_secetoasa'].mean().reset_index()
monthly_dry_ratio['Procent_secetos'] = monthly_dry_ratio['este_secetoasa'] * 100
monthly_dry_ratio['Luna'] = monthly_dry_ratio['Luna_numeric'].apply(lambda x: luni_romana[x - 1])

# Pivot pentru plotare
pivot_data = monthly_dry_ratio.pivot(index='Luna', columns='Interval', values='Procent_secetos')
pivot_data = pivot_data.reindex(luni_romana)

# Plot
plt.figure(figsize=(12, 6))
colors = ['#1f77b4', '#ff7f0e']
for i, col in enumerate(pivot_data.columns):
    plt.plot(pivot_data.index, pivot_data[col], label=col, color=colors[i], marker='o', linewidth=2)

plt.title("Repartiția lunară a lunilor secetoase în Câmpia Bărăganului\n(Clasificare Hellmann)", fontsize=13)
plt.ylabel("Procent luni secetoase (%)", fontsize=11)
plt.xlabel("Luna", fontsize=11)
plt.ylim(0, 100)
plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(rotation=45)
plt.legend(title='', loc='upper right')
plt.tight_layout()
plt.savefig("grafic_repartitie_luni_secetoase_baragan.png", dpi=300)
print("Grafic salvat ca 'repartitie_luni_secetoase_baragan.png'")
