import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.cache_data.clear()


st.set_page_config(page_title="NH Site Mapping", layout="wide")

@st.cache_data
def load_data():
    return pd.read_excel("NH_site_data_comprehensive.xlsx")

df = load_data()

st.title("\U0001F4CD New Hampshire Site Mapping Dashboard")

# App mode selection
app_mode = st.sidebar.selectbox('Contents', ['01 Organizations', '02 Organization Explorer'])

if app_mode == '01 Organizations':
    st.header("\U0001F4C8 Organization Overview")

    categories = df["Category"].dropna().unique().tolist()
    selected_cats = st.multiselect("Select Category", categories, default=categories)

    filtered = df[df["Category"].isin(selected_cats)]

    st.subheader(f"Showing {len(filtered)} Organizations")
    st.dataframe(filtered, use_container_width=True)

    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("\U0001F4E5 Download filtered data as CSV", csv, "nh_sites_filtered.csv", "text/csv")

    if st.checkbox("Show Map", value=False):
        st.subheader("Geographical Overview")

        geolocator = Nominatim(user_agent="nh_site_mapper")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

        m = folium.Map(location=[43.5, -71.5], zoom_start=7)
        cluster = MarkerCluster().add_to(m)

        colors = {
            "High School": "blue",
            "Community College": "green",
            "Youth-serving Organization": "purple",
            "Workforce Intermediary": "orange",
            "Apprenticeship Program": "red",
            "Training Program": "darkred",
            "Charter / STEM High School": "cadetblue",
            "Community College System": "darkgreen"
        }

        for _, row in filtered.iterrows():
            location = geocode(row["Location"])
            if location:
                folium.Marker(
                    location=[location.latitude, location.longitude],
                    popup=f"{row['Organization Name']}<br>{row['Programs Offered']}",
                    tooltip=row["Organization Name"],
                    icon=folium.Icon(color=colors.get(row["Category"], "gray"))
                ).add_to(cluster)

        st_folium(m, width=900, height=550)

elif app_mode == '02 Organization Explorer':
    st.header("\U0001F50D Explore Individual Organizations")

    categories = df["Category"].dropna().unique().tolist()
    selected_category = st.selectbox("Select Category", ["--"] + categories)

    sub_df = df[df["Category"] == selected_category] if selected_category != "--" else df

    if selected_category != "--":
        selected_org = st.selectbox("Select Organization", ["--"] + sub_df["Organization Name"].tolist())
        if selected_org != "--":
            org_row = sub_df[sub_df["Organization Name"] == selected_org].iloc[0]
            st.markdown("---")
            st.subheader(f"Details for: {selected_org}")
            st.markdown(f"**Contact Info:** {org_row['Contact Info']}")
            st.markdown(f"**Programs Offered:** {org_row['Programs Offered']}")
            st.markdown(f"**Location:** {org_row['Location']}")
            st.markdown(f"**Description:** {org_row['Description']}")