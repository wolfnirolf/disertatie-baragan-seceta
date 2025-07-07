import pandas as pd
import numpy as np
from scipy.stats import gamma, pearson3, norm
from scipy.ndimage import uniform_filter1d

INPUT_FILE = "Date-climatologice-6statii-3Temp-Prec.xlsx"
OUTPUT_FILE = "Rezultate_SPI3_SPEI3_6statii.xlsx"

# 1. Citește datele climatologice
df = pd.read_excel(INPUT_FILE)
df.columns = df.columns.str.strip()

# 2. Adaugă Ra (radiație solară extraterestră medie lunară pentru ~45° lat N)
ra_month = {
    1: 8.4, 2: 10.5, 3: 13.1, 4: 15.2, 5: 16.5, 6: 17.1,
    7: 17.0, 8: 15.9, 9: 13.4, 10: 10.8, 11: 8.8, 12: 7.7
}
df["Ra"] = df["Luna_numeric"].map(ra_month)

# 3. Calculează ETP prin metoda Hargreaves
df["ETP"] = (
    0.0023 * df["Ra"] *
    np.sqrt(np.maximum(0, df["tmax_med"] - df["tmin_med"])) *
    (df["tmed_med"] + 17.8)
)

# 4. Funcții SPI și SPEI cu standardizare statistică
def compute_spi_3(series):
    smoothed = uniform_filter1d(series, size=3, mode='nearest')
    shape, loc, scale = gamma.fit(smoothed[~np.isnan(smoothed)])
    cdf = gamma.cdf(smoothed, shape, loc=loc, scale=scale)
    spi = norm.ppf(np.clip(cdf, 1e-6, 1 - 1e-6))  # transformare normală
    return spi

def compute_spei_3(deficit):
    smoothed = uniform_filter1d(deficit, size=3, mode='nearest')
    shape, loc, scale = pearson3.fit(smoothed[~np.isnan(smoothed)])
    cdf = pearson3.cdf(smoothed, shape, loc=loc, scale=scale)
    spei = norm.ppf(np.clip(cdf, 1e-6, 1 - 1e-6))
    return spei

# 5. Parcurge fiecare stație
rezultate = []

for statie in df["Statie"].unique():
    df_st = df[df["Statie"] == statie].copy()
    df_st = df_st.sort_values(["An_numeric", "Luna_numeric"]).reset_index(drop=True)

    precip = df_st["precip_total"].values
    etp = df_st["ETP"].values
    deficit = precip - etp

    spi_vals = compute_spi_3(precip)
    spei_vals = compute_spei_3(deficit)

    for i in range(len(df_st)):
        rezultate.append({
            "Statie": statie,
            "An": int(df_st.loc[i, "An_numeric"]),
            "Luna": int(df_st.loc[i, "Luna_numeric"]),
            "SPI-3": round(spi_vals[i], 3),
            "SPEI-3": round(spei_vals[i], 3)
        })

# 6. Export în Excel
df_out = pd.DataFrame(rezultate)
df_out.to_excel(OUTPUT_FILE, index=False)

print(f"✅ Calcul SPI-3 și SPEI-3 a fost finalizat și salvat în fișierul: {OUTPUT_FILE}")
