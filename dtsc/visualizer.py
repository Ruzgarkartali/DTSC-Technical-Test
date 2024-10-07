from typing import List
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

def plot_numericals(region, trackcat, data: pd.DataFrame, c=None,anomalies=None):
    # Créer une figure avec 1 ligne et 2 colonnes
    fig, axs = plt.subplots(1, 2, figsize=(10, 4), dpi=80)

    # Scatter Plot
    filtered_data = data[data["Region"] == region]
    filtered_data = filtered_data[filtered_data["TrackCat"] == trackcat]

    plt.suptitle(f"{trackcat} in {region}", fontsize=14)
    axs[0].scatter(filtered_data["Kilometer"], filtered_data["Devices"], c=c)
    axs[0].set_title(f"Chart of number of devices depending on rail kilometers")
    axs[0].set_xlabel("Kilometers")
    axs[0].set_ylabel("Number of devices")
    #axs[0].tight_layout()

    # Evolution Plot
    axs[1].plot(filtered_data["Year"], filtered_data["Kilometer"], '-b', label='Kilometers')
    axs[1].plot(filtered_data["Year"], filtered_data["Devices"], '-g', label='Number of devices')
    
    if anomalies is not None:
        axs[1].plot(anomalies["Year"], anomalies["Kilometer"], 'ro', label='Anomalies (Kilometers)')
        axs[1].plot(anomalies["Year"], anomalies["Devices"], 'ro', label='Anomalies (Devices)')
    
    axs[1].set_title(f"Evolution of kilometers and number of devices")
    axs[1].set_xlabel("Year")
    axs[1].set_ylabel("Value")
    axs[1].set_xticks(range(2006, 2023, 3))
    axs[1].legend()
    #axs[1].tight_layout()

    # Ajustement des espaces entre les sous-graphiques
    plt.tight_layout()
    plt.show()

def plot_numericals_colored(data):
    fig, axs = plt.subplots(1, 2, figsize=(16, 6))

    # --- Coloring according to region ---
    palette_region = sns.color_palette("husl", n_colors=data['Region'].nunique())
    region_colors = {region: palette_region[i] for i, region in enumerate(data['Region'].unique())}

    for region, color in region_colors.items():
        axs[0].scatter(data[data['Region'] == region]['Kilometer'],
                    data[data['Region'] == region]['Devices'],
                    color=color, label=region)

    axs[0].set_title('Number of devices depending on Kilometers by Region')
    axs[0].set_xlabel('Kilometers')
    axs[0].set_ylabel('Devices')
    axs[0].legend()
    axs[0].grid(True)

    # --- Coloring according to TrackCat ---
    palette_trackcat = sns.color_palette("husl", n_colors=data['TrackCat'].nunique())
    trackcat_colors = {trackcat: palette_trackcat[i] for i, trackcat in enumerate(data['TrackCat'].unique())}

    for trackcat, color in trackcat_colors.items():
        axs[1].scatter(data[data['TrackCat'] == trackcat]['Kilometer'],
                    data[data['TrackCat'] == trackcat]['Devices'],
                    color=color, label=trackcat)

    axs[1].set_title('Number of devices depending on Kilometers by Track Category')
    axs[1].set_xlabel('Kilometers')
    axs[1].set_ylabel('Devices')
    axs[1].legend()
    axs[1].grid(True)

    plt.tight_layout()
plt.show()






def compareRegions(norm_data, data: pd.DataFrame):
    regions = data["Region"].unique()  
    trackcats = data["TrackCat"].unique()  


    fig, axs = plt.subplots(len(trackcats), 3, figsize=(20, 8), dpi=80)
    fig.suptitle("Comparative analysis of kilometers and number of devices, between regions ")

    for j, trackcat in enumerate(trackcats):
        for i, feature in enumerate(["Kilometer", "Devices"]):
            axs[j, i].set_title(f"{feature} in {trackcat}")
            axs[j, i].set_xlabel("Year")
            axs[j, i].set_ylabel(f"{feature}")
            axs[j, i].set_xticks(range(2006, 2023, 3))

            for region in regions:
                region_data = norm_data.loc[(norm_data["Region"] == region) & (norm_data["TrackCat"] == trackcat)]
                axs[j, i].plot(
                    region_data["Year"],
                    region_data[feature],
                    label=region
                )
            axs[j, i].legend()

 
        axs[j, 2].set_title(f"Ratio (Kilometer/Devices) in {trackcat}")
        axs[j, 2].set_xlabel("Year")
        axs[j, 2].set_ylabel("Ratio")
        axs[j, 2].set_xticks(range(2006, 2023, 3))

        for region in regions:
            region_data = data.loc[(data["Region"] == region) & (data["TrackCat"] == trackcat)]
            axs[j, 2].plot(
                region_data["Year"],
                region_data["Kilometer"] / region_data["Devices"],
                label=region
            )
        axs[j, 2].legend()

    plt.tight_layout()
    plt.show()

def plot_pca(pca_df):
    region_colors = dict(zip(pca_df['Region'].unique(), mcolors.TABLEAU_COLORS))
    trackcat_colors = dict(zip(pca_df['TrackCat'].unique(), mcolors.TABLEAU_COLORS))

    fig, axs = plt.subplots(1, 2, figsize=(16, 6))

    for region in pca_df['Region'].unique():
        subset = pca_df[pca_df['Region'] == region]
        axs[0].scatter(subset['PC1'], subset['PC2'], label=region, color=region_colors[region])

    axs[0].set_title('PCA - Colored by Region')
    axs[0].set_xlabel('PC1')
    axs[0].set_ylabel('PC2')
    axs[0].legend(title='Region')
    axs[0].grid(True)

    for trackcat in pca_df['TrackCat'].unique():
        subset = pca_df[pca_df['TrackCat'] == trackcat]
        axs[1].scatter(subset['PC1'], subset['PC2'], label=trackcat, color=trackcat_colors[trackcat])

    axs[1].set_title('PCA - Colored by TrackCat')
    axs[1].set_xlabel('PC1')
    axs[1].set_ylabel('PC2')
    axs[1].legend(title='TrackCat')
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()

