import streamlit as st

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
