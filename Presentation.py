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