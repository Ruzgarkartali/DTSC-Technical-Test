import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.decomposition import PCA

def perform_pca(data):
    encoder = OneHotEncoder(sparse_output=False)
    region_encoded = encoder.fit_transform(data[['Region', 'TrackCat']])

    data_encoded = pd.concat([
        data[['Year', 'Kilometer', 'Devices']].reset_index(drop=True),
        pd.DataFrame(region_encoded, columns=encoder.get_feature_names_out(['Region', 'TrackCat']))
    ], axis=1)

    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data_encoded)

    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(data_scaled)

    pca_df = pd.DataFrame(pca_result, columns=['PC1', 'PC2'])
    pca_df['Region'] = data['Region'].values
    pca_df['TrackCat'] = data['TrackCat'].values

    return pca_df