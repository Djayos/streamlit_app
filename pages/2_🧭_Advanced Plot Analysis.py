import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Pesticides Product Analysis",
    page_icon="🌱",
)

st.title("🌲Advanced Product Analysis🌲")

st.write("""
Here, we dive deep into the distribution, popularity, and trends of pesticides products across different departments and years.
By leveraging the interactive features of this dashboard, you can gain insights into product demands, identify key market players, and understand regional disparities in product consumption.
Navigate through the various plots and use the interactive elements to tailor the analysis to your specific interests.
""")

# SideBar
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
    
    dfs = []
    
    for year in years:
        for region in regions:
            file_name = f"BNVD_TRACABILITE_20221016_ACHAT_CP_PRODUIT_{region}_{year}.csv"
            file_path = f"csv/{file_name}"  # Construct the path directly
            try:
                df_region = pd.read_csv(file_path, delimiter=";")
                dfs.append(df_region)
            except FileNotFoundError:
                st.warning(f"File {file_name} not found.")
                continue

    df = pd.concat(dfs, ignore_index=True)

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


st.subheader("Product Quantity Distribution by Year")
st.write("""
This pie chart visualizes the distribution of pesticides product quantities for the selected department over four years (2021, 2020, 2019, and 2018). 
It provides insights into the annual purchase volumes and allows stakeholders to understand the temporal trends in pesticides product demand within the chosen department.
""")
# Dropdown for department selection
sorted_department_names = dict(sorted(department_names.items(), key=lambda x: str(x[0])))
dropdown_options = [f"{code} - {name}" for code, name in sorted_department_names.items()]
selected_department = st.selectbox("Select a Department", dropdown_options)
selected_code = selected_department.split(" - ")[0]

# Filter the dataframe based on the selected department code
filtered_df = df[df['code_postal_acheteur'].astype(str).str.startswith(selected_code)]

# Group by year and sum the product quantities
yearly_data = filtered_df.groupby('annee')['quantite_produit'].sum()

# Plot pie chart
fig, ax = plt.subplots(figsize=(14, 8))
yearly_data.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90, legend=True)
ax.set_ylabel('')
ax.set_title(f"Product Quantity Distribution in {selected_department} by Year")
st.pyplot(fig)


st.subheader("Top Product Rankings")
st.write("""
The table below lists the top pesticides products based on the selected ranking metric. 
Users can choose between different metrics to rank the products: total quantity sold, average quantity per transaction, or the total number of transactions. 
This dynamic ranking provides insights into the most popular or widely distributed products, helping stakeholders identify key products in the market.
""")

ranking_metric = st.radio(
    "Select Ranking Metric",
    options=["By Total Quantity", "By Average Quantity per Transaction", "By Number of Transactions"]
)

top_n = st.radio(
    "Select Number of Top AMMs to Display",
    options=[3, 5, 8]
)

if ranking_metric == "By Total Quantity":
    ranking_df = df2.groupby(['nom produit', 'fonctions'])['quantite_produit'].sum().reset_index()
    ranking_df = ranking_df.sort_values(by='quantite_produit', ascending=False).head(top_n)
elif ranking_metric == "By Average Quantity per Transaction":
    ranking_df = df2.groupby(['nom produit', 'fonctions'])['quantite_produit'].mean().reset_index()
    ranking_df = ranking_df.sort_values(by='quantite_produit', ascending=False).head(top_n)
elif ranking_metric == "By Number of Transactions":
    ranking_df = df2.groupby(['nom produit', 'fonctions']).size().reset_index(name='number_of_transactions')
    ranking_df = ranking_df.sort_values(by='number_of_transactions', ascending=False).head(top_n)

st.write(ranking_df)



st.subheader("Year-wise Product Quantity Breakdown for a Department")
st.write("""
This stacked bar chart visualizes the breakdown of pesticides product quantities by year for a selected department.
By adjusting the year range, users can focus on specific periods to understand the evolution of product consumption.
""")

# Dropdown for department selection
sorted_department_names = dict(sorted(department_names.items(), key=lambda x: str(x[0])))
dropdown_options = [f"{code} - {name}" for code, name in sorted_department_names.items()]
selected_department = st.selectbox("Select a Department for Year-wise Breakdown", dropdown_options, key='yearwise_breakdown_selectbox')
selected_code = selected_department.split(" - ")[0]

# Filter the dataframe based on the selected department code
filtered_df = df2[df2['code_postal_acheteur'].astype(str).str.startswith(selected_code)]

# Group by product and year, then sum the product quantities
product_yearly_data = filtered_df.groupby(['nom produit', 'annee'])['quantite_produit'].sum().unstack().fillna(0)
product_yearly_data.columns = product_yearly_data.columns.astype(str)

# Slider to select the range of years
selected_years = st.slider("Select Year Range", min_value=2018, max_value=2021, value=(2018, 2021), step=1)
selected_years = [str(year) for year in selected_years]

# Filter the data based on the selected years
product_yearly_data = product_yearly_data.loc[:, selected_years[0]:selected_years[1]]

# Sort by the total quantity over the selected years and keep only the top 30
product_yearly_data = product_yearly_data.iloc[product_yearly_data.sum(axis=1).argsort()[-30:][::-1]]

# Plot the stacked bar chart
fig, ax = plt.subplots(figsize=(14, 8))
product_yearly_data.plot(kind='bar', stacked=True, ax=ax)
ax.set_title(f"Year-wise Product Quantity Breakdown in {selected_department}")
ax.set_ylabel("Total Quantity of Product")
ax.set_xlabel("Product")
plt.xticks(rotation=70)
st.pyplot(fig)






st.subheader("Distribution of Product Functions")
st.write("""
This histogram illustrates the distribution of different pesticides product functions. 
By adjusting the threshold, users can focus on products that exceed a certain frequency, helping to identify the most common or prevalent product functions in the dataset.
""")
# Threshold input
threshold = st.number_input("Set a threshold for minimum number of products in a category:", min_value=0, value=10)

# Group by "fonctions" column
category_counts = df2['fonctions'].value_counts()

# Filter categories based on threshold
filtered_categories = category_counts[category_counts >= threshold]

# Plot
fig, ax = plt.subplots(figsize=(12, 8))
filtered_categories.plot(kind='bar', ax=ax)
ax.set_title("Distribution of Product Categories")
ax.set_xlabel("Product Categories")
ax.set_ylabel("Number of Products")
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)