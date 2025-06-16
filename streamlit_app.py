# streamlit_app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="NH Site Mapping", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_excel("NH_site_data_comprehensive.xlsx")

df = load_data()

st.title("📍 New Hampshire Site Mapping Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
categories = df["Category"].unique().tolist()
regions = df["Location"].apply(lambda x: x.split(",")[-1].strip()).unique().tolist()

selected_cats = st.sidebar.multiselect("Select Category", categories, default=categories)
selected_regs = st.sidebar.multiselect("Select Region (City/Town)", regions, default=regions)

filtered = df[df["Category"].isin(selected_cats) & df["Location"].apply(lambda x: any(reg in x for reg in selected_regs))]

# Search bar
search = st.sidebar.text_input("Search by organization name or program")
if search:
    filtered = filtered[filtered["Organization Name"].str.contains(search, case=False) |
                        filtered["Programs Offered"].str.contains(search, case=False)]

# Display data
st.subheader(f"Showing {len(filtered)} Organizations")
st.dataframe(filtered, use_container_width=True)

# Download filtered data
csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button(label="📥 Download filtered data as CSV", data=csv, file_name="nh_sites_filtered.csv", mime="text/csv")

# Show map if location field is address-like
if st.sidebar.checkbox("Show Map", value=False):
    import folium
    from streamlit_folium import st_folium

    m = folium.Map(location=[43.5, -71.5], zoom_start=7)
    for _, row in filtered.iterrows():
        # Minimal geocoding: city centers; you could expand with geopy
        folium.Marker(location=[43.5, -71.5], popup=row["Organization Name"]).add_to(m)
    st.subheader("Geographical Overview")
    st_folium(m, width=700, height=450)
