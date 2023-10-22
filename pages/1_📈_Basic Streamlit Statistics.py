
import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(
    page_title="Pesticides Product Analysis",
    page_icon="🌱",
)

st.title("🪴Basic Analysis of Pesticides Products🪴")

# Introduction
st.write("""
This platform provides a comprehensive exploration into the regional distribution, trends, and consumption patterns of pesticides products. With a combination of detailed charts and interactive maps, users can delve into the nuances of product consumption across various postal areas and departments in France.
Whether you're looking to understand the overarching trends or zoom into specific regions, this dashboard offers tools and visualizations to cater to a wide range of analytical needs.
Scroll down to embark on this data-driven journey and uncover insights into the world of pesticides in France!
""")

#SideBar
st.sidebar.header("Informations")
st.sidebar.text("Joseph")
st.sidebar.text("BEAUMONT")
st.sidebar.text("Promo 2025 - DE1")

st.sidebar.header("Liens")
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/joseph-beaumont/)")
st.sidebar.markdown("[GitHub](https://github.com/Djayos)")


@st.cache_data
def load_data():
    years = ["2021", "2020", "2019", "2018"]
    regions = [
        "AUVERGNE RHONE ALPES",
        "BOURGOGNE FRANCHE COMTE",
        "BRETAGNE",
        "CENTRE VAL DE LOIRE",
        "CORSE",
        "GRAND EST",
        "GUADELOUPE",
        "GUYANE",
        "HAUTS DE FRANCE",
        "ILE DE FRANCE",
        "INDETERMINE",
        "LA REUNION",
        "MARTINIQUE",
        "MAYOTTE",
        "NORMANDIE",
        "NOUVELLE AQUITAINE",
        "OCCITANIE",
        "PAYS DE LA LOIRE",
        "PROVENCE ALPES COTE D AZUR"
    ]
    
    directory_path = "csv"
    dfs = []
    
    for year in years:
        for region in regions:
            file_name = f"BNVD_TRACABILITE_20221016_ACHAT_CP_PRODUIT_{region}_{year}.csv"
            file_path = os.path.join(directory_path, file_name)
            try:
                df_region = pd.read_csv(file_path, delimiter=";")
                dfs.append(df_region)
            except FileNotFoundError:
                st.warning(f"File {file_name} not found.")
                continue

    df = pd.concat(dfs, ignore_index=True)
    
    df_commune = pd.read_csv("csv\communes-departement-region.csv", delimiter=",")
    df_AMMnumber = pd.read_csv("csv\produits_Windows-1252.csv", delimiter=";",encoding="Windows-1252")
    geo_data = gpd.read_file("json\departements.geojson")
    
    # remove kg lines
    df = df[df['conditionnement'] != 'kg']

    # removing lines where code_postal_acheteur is 0
    df = df[df['code_postal_acheteur'] != 0]
    # Convert the column to string
    df['code_postal_acheteur'] = df['code_postal_acheteur'].astype(str)
    # Ensure each entry has 5 characters, padding with zeros where necessary
    df['code_postal_acheteur'] = df['code_postal_acheteur'].apply(lambda x: x.zfill(5))

    # remove lines where quantite_produit is nan or 'nc'
    df['quantite_produit'] = df['quantite_produit'].astype(str)
    df = df[~df['quantite_produit'].str.contains('[a-zA-Z]')]
    df['quantite_produit'] = df['quantite_produit'].astype(float)
    df['quantite_produit'] = df['quantite_produit'].astype(int)
    
    # place year column in str format
    df['annee'] = df['annee'].astype(str)

    # create a new column with the departement code
    df['department_code'] = df['code_postal_acheteur'].astype(str).str[:2]

    # create dictinnary with the departement code and the region
    department_names = df_commune[['code_departement', 'nom_departement']].drop_duplicates().set_index('code_departement').to_dict()['nom_departement']
    
    df2 = df.merge(df_AMMnumber[['numero AMM', 'nom produit', 'fonctions']], left_on='amm', right_on='numero AMM', how='left')
    
    return df, df_commune, df_AMMnumber, geo_data, department_names, df2

df, df_commune, df_AMMnumber, geo_data, department_names, df2 = load_data()


# 1. Displaying Statistics
total_products = df['amm'].nunique()
total_quantity_purchased = df['quantite_produit'].sum()
total_transactions = df.shape[0]
regions_covered = df['code_postal_acheteur'].nunique()
year_range = f"{df['annee'].min()} - {df['annee'].max()}"


st.write(f"**- Total Products**: {total_products}")
st.write(f"**- Total Quantity Purchased**: {total_quantity_purchased}")
st.write(f"**- Total Transactions**: {total_transactions}")
st.write(f"**- Year Range**: {year_range}")


# 2. Displaying the first Data Visualization

# Summing the product quantity for each postal area
st.subheader("Trend of Product Purchases Across Postal Areas")
st.write("""This line chart showcases the quantity of products purchased across different postal areas. Areas with higher peaks suggest greater purchasing activity, offering insights into regional demand.""")
postal_purchase = df.groupby('code_postal_acheteur')['quantite_produit'].sum().reset_index()
st.line_chart(postal_purchase.set_index('code_postal_acheteur'))

# Grouping by region and summing the product quantity
st.subheader("Product Purchases by Region")
st.write("""The bar chart offers a clear view of the total quantity of products purchased by each region. It's a direct measure of which regions are the biggest consumers of pesticides products.""")
region_purchase = df.groupby('code_postal_acheteur')['quantite_produit'].sum().sort_values(ascending=False).reset_index()
st.bar_chart(region_purchase.set_index('code_postal_acheteur'))

# altair chart for postal area and product quantity
st.subheader("Diversity of Product Purchases in Postal Areas")
st.write("""The scatter plot below visualizes the relationship between the number of unique products and the total quantity purchased in different postal areas. Each point represents a postal area. The X-axis shows the number of unique products, and the Y-axis displays the total quantity purchased. This plot gives insights into whether areas with a diverse range of products also purchase in larger quantities.""")
postal_data = df.groupby('code_postal_acheteur').agg({'quantite_produit': 'sum', 'amm': 'nunique'}).reset_index()

scatter_plot = alt.Chart(postal_data).mark_circle(size=60).encode(
    x='amm:Q',
    y='quantite_produit:Q',
    tooltip=['code_postal_acheteur', 'amm', 'quantite_produit']
).interactive()

st.altair_chart(scatter_plot, use_container_width=True)


# heatmap for departement area and product quantity

# Sum the quantite_produit for each department_code
department_data = df.groupby('department_code')['quantite_produit'].sum().reset_index()

# Calculate the centroid for each department in the geo_data
geo_data['longitude'] = geo_data.centroid.x
geo_data['latitude'] = geo_data.centroid.y

# Merge the geo_data with department_data
merged_data = geo_data.merge(department_data, left_on="code", right_on="department_code")

# Normalize the quantite_produit to be between 0 and 1
max_quantity = merged_data['quantite_produit'].max()
min_quantity = merged_data['quantite_produit'].min()
merged_data['normalized_quantity'] = (merged_data['quantite_produit'] - min_quantity) / (max_quantity - min_quantity)

def get_color(value):
    red = int(value * 255)
    blue = 255 - red
    return (red, 0, blue)

merged_data['color'] = merged_data['normalized_quantity'].apply(get_color)
st.subheader("Distribution of Pesticides Product Purchases by Department")
st.write("""This map visualizes the quantity of pesticides products purchased across different departments in France. Each department is represented by a circle, with the color intensity indicating the total quantity of products purchased. A shift from blue to red indicates an increase in the quantity, where blue represents low purchase volumes and red indicates high volumes. This visualization provides insights into regional demand patterns, helping to identify areas with the highest consumption of these products.""")
st.map(merged_data, color='color')