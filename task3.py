# -*- coding: utf-8 -*-
"""Task3

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1l1Jaw5oaN5Tp8oYNplIMSQN5tilPA7t3
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import seaborn as sns

"""LOAD THE DATASET"""

df=pd.read_csv("/content/customer_data.csv")

print("Dataset Shape:", df.shape)

print("Missing Values:", df.isnull().sum().sum())

print("Duplicates:", df.duplicated().sum())

print(df.info())

print(df.describe())

"""DATA PREPROCESSING"""

scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[['Age', 'Annual Income', 'Spending Score']])

"""# Step 3: Determine optimal clusters using Elbow Method"""

wcss = []
k_values = range(1, 11)
for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(df_scaled)
    wcss.append(kmeans.inertia_)

plt.plot(k_values, wcss, marker='o')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.title('Elbow Method for Optimal Clusters')
plt.show()

"""# Applying K-Means Clustering"""

optimal_clusters = 3
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(df_scaled)

"""Visualization using PCA"""

pca = PCA(n_components=2)
pca_components = pca.fit_transform(df_scaled)
df['PCA1'] = pca_components[:, 0]
df['PCA2'] = pca_components[:, 1]

plt.scatter(df['PCA1'], df['PCA2'], c=df['Cluster'], cmap='viridis', edgecolors='k')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.title('Customer Clusters Visualization')
plt.colorbar(label='Cluster')
plt.show()

# Pair Plot
sns.pairplot(df[['Age', 'Annual Income', 'Spending Score', 'Cluster']], hue='Cluster', palette='viridis')
plt.show()

# Centroid Visuals
centroids = kmeans.cluster_centers_
centroids_pca = pca.transform(centroids)
plt.scatter(df['PCA1'], df['PCA2'], c=df['Cluster'], cmap='viridis', edgecolors='k', alpha=0.5)
plt.scatter(centroids_pca[:, 0], centroids_pca[:, 1], c='red', marker='X', s=200, label='Centroids')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.title('Customer Clusters with Centroids')
plt.legend()
plt.show()