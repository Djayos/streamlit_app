import streamlit as st
import pandas as pd
import geopandas as gpd
import altair as alt
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Pesticides Product Analysis",
    page_icon="🌱",
)

# Sidebar
st.sidebar.header("Informations")
st.sidebar.text("Joseph")
st.sidebar.text("BEAUMONT")
st.sidebar.text("Promo 2025 - DE1")

st.sidebar.header("Liens")
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/joseph-beaumont/)")
st.sidebar.markdown("[GitHub](https://github.com/Djayos)")

st.title("🌱 Pesticides Product Analysis: Presentation Page 🌱")

st.subheader("Introduction")
st.write("""
Welcome to the Pesticides Product Consumption Analysis Streamlit Page. This platform is designed to provide a comprehensive exploration into the regional distribution, trends, and consumption patterns of pesticide products across France. Our data-driven approach aids in unveiling both overarching trends and detailed nuances, spanning from 2018 to 2021.
""")

st.subheader("Why Pesticides?")
st.write("""
Pesticides are essential for maintaining high agricultural yields and controlling pests. However, their widespread use has significant environmental implications. Pesticides can disrupt local ecosystems, potentially leading to biodiversity loss, and may pose risks to human health through water and soil contamination. By understanding our consumption patterns and the products in high demand, we can navigate towards more sustainable agricultural practices.
""")

st.subheader("Key Insights")
st.write("""
- **Regional Analysis**: France's consumption of pesticides varies across regions, with certain areas showcasing higher demand.
- **Product Trends**: The market sees a diverse range of pesticides, with specific products dominating in terms of demand and distribution.
- **Environmental Perspective**: Recognizing the widespread use of pesticides underscores the urgency to advocate for sustainable alternatives and practices that mitigate their environmental impact.
""")

st.subheader("Objectives")
st.write("""
With this application, our primary goals are:
1. **Understand Consumption Patterns**: Analyze the distribution and trends of pesticide products across different regions and years.
2. **Identify Key Players**: Highlight the most popular or widely distributed products, aiding stakeholders in making informed decisions.
3. **Promote Sustainable Practices**: By unveiling consumption insights, we aim to encourage more environmentally conscious choices in the agricultural sector.
""")

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

    
    df_commune = pd.read_csv("csv/communes-departement-region.csv", delimiter=",")
    df_AMMnumber = pd.read_csv("csv/produits_Windows-1252.csv", delimiter=";",encoding="Windows-1252")
    geo_data = gpd.read_file("json/departements.geojson")
    
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

st.title("🪴Basic Analysis of Pesticides Products🪴")

# Introduction
st.write("""
This platform provides a comprehensive exploration into the regional distribution, trends, and consumption patterns of pesticides products. With a combination of detailed charts and interactive maps, users can delve into the nuances of product consumption across various postal areas and departments in France.
Whether you're looking to understand the overarching trends or zoom into specific regions, this dashboard offers tools and visualizations to cater to a wide range of analytical needs.
Scroll down to embark on this data-driven journey and uncover insights into the world of pesticides in France!
""")

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

st.title("🌲Advanced Product Analysis🌲")

st.write("""
Here, we dive deep into the distribution, popularity, and trends of pesticides products across different departments and years.
By leveraging the interactive features of this dashboard, you can gain insights into product demands, identify key market players, and understand regional disparities in product consumption.
Navigate through the various plots and use the interactive elements to tailor the analysis to your specific interests.
""")

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



# Conclusion Title
st.title("Conclusion")


## 1. Overview and Regional Analysis
st.subheader("1. Overview and Regional Analysis")
st.write("""
- France's consumption of pesticides is spread across multiple regions, with some exhibiting higher demand than others.
- Detailed analytics revealed patterns of consumption across various postal areas and departments, shedding light on regional disparities in product demand.
""")

## 2. Product Trends and Distributions
st.subheader("2. Product Trends and Distributions")
st.write("""
- A diverse range of pesticides is in use, with a few products dominating the market.
- Trends showcased the evolution of product consumption over the years, providing insights into market dynamics and product preferences.
""")

## 3. Deep Dive into Product Functions and Popularity
st.subheader("3. Deep Dive into Product Functions and Popularity")
st.write("""
- Advanced analytics enabled the identification of top market players and products, providing clarity on which products are preferred and widely distributed.
- A histogram view of product functions revealed the most prevalent types in the market, aiding stakeholders in understanding product utility.
""")

# Environmental Perspective
st.subheader("Environmental Perspective")
st.write("""
The widespread use of pesticides in France, as revealed by this analysis, carries environmental implications. Pesticides can disrupt ecosystems, leading to biodiversity loss and potential harm to human health through water and soil contamination. By understanding our consumption patterns and the products in high demand, there's an opportunity to advocate for sustainable alternatives or practices that mitigate environmental impact. This analysis serves as a foundation for informed decision-making towards a greener future.
""")

# Closing Remarks
st.write("""
Harnessing data-driven insights can guide us towards more environmentally conscious choices. As we work towards sustainability, understanding our current consumption patterns is the first step towards positive change.
""")


