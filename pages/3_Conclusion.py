import streamlit as st

st.set_page_config(
    page_title="Pesticides Product Analysis",
    page_icon="🌱",
)


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

# Sidebar with Contact Information (Optional)
st.sidebar.header("Informations")
st.sidebar.text("Joseph")
st.sidebar.text("BEAUMONT")
st.sidebar.text("Promo 2025 - DE1")

st.sidebar.header("Liens")
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/joseph-beaumont/)")
st.sidebar.markdown("[GitHub](https://github.com/Djayos)")
