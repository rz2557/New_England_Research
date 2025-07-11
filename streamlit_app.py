import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.cache_data.clear()
# Page config

st.set_page_config(page_title="NH Site Mapping", layout="wide")
st.title("📍 New Hampshire Site Mapping Dashboard")


def load_general_data():
    return pd.read_excel("NH_site_data_comprehensive.xlsx")


def load_immigrant_data():
    return pd.read_excel("NH_Immigrant_Youth_Support_Services_UPDATED.xlsx")

general_df = load_general_data()
immigrant_df = load_immigrant_data()

# Sidebar structure
app_mode = st.sidebar.selectbox('Contents', ['01 Organizations'])

if app_mode == '01 Organizations':
    org_type = st.sidebar.radio("Select organization type:", ['General Organizations', 'Immigrant Support Organizations'])

    if org_type == 'General Organizations':
        general_mode = st.sidebar.selectbox("View Mode", ['Data', 'Explorer'])

        if general_mode == 'Data':
            st.header("📊 General Organizations – Data View")
            categories = general_df["Category"].dropna().unique().tolist()
            selected_cats = st.multiselect("Select Category", categories, default=categories)

            filtered = general_df[general_df["Category"].isin(selected_cats)]

            st.subheader(f"Showing {len(filtered)} Organizations")
            st.dataframe(filtered, use_container_width=True)

            csv = filtered.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download filtered data as CSV", csv, "general_orgs_filtered.csv", "text/csv")

        elif general_mode == 'Explorer':
            st.header("🔍 General Organizations – Explorer")
            categories = general_df["Category"].dropna().unique().tolist()
            selected_category = st.selectbox("Select Category", ["--"] + categories)

            sub_df = general_df[general_df["Category"] == selected_category] if selected_category != "--" else general_df

            selected_org = st.selectbox("Select Organization", ["--"] + sub_df["Organization Name"].tolist())
            if selected_org != "--":
                org_row = sub_df[sub_df["Organization Name"] == selected_org].iloc[0]
                st.markdown("---")
                st.subheader(f"Details for: {selected_org}")
                st.markdown(f"**Contact Info:** {org_row['Contact Info']}")
                st.markdown(f"**Programs Offered:** {org_row['Programs Offered']}")
                st.markdown(f"**Location:** {org_row['Location']}")
                st.markdown(f"**Description:** {org_row['Description']}")
                st.markdown(f"**Website:** [{org_row['Website']}]({org_row['Website']})")

    elif org_type == 'Immigrant Support Organizations':
        imm_mode = st.sidebar.selectbox("View Mode", ['Data', 'Explorer'])

        if imm_mode == 'Data':
            st.header("🧩 Immigrant Support Organizations – Data View")
            categories = immigrant_df["Category"].dropna().unique().tolist()
            selected_cats = st.multiselect("Select Category", categories, default=categories)

            filtered = immigrant_df[immigrant_df["Category"].isin(selected_cats)]

            st.subheader(f"Showing {len(filtered)} Organizations")
            st.dataframe(filtered, use_container_width=True)

            csv = filtered.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download filtered data as CSV", csv, "immigrant_support_orgs.csv", "text/csv")

        elif imm_mode == 'Explorer':
            st.header("🔍 Immigrant Support Organizations – Explorer")
            categories = immigrant_df["Category"].dropna().unique().tolist()
            selected_category = st.selectbox("Select Category", ["--"] + categories)

            sub_df = immigrant_df[immigrant_df["Category"] == selected_category] if selected_category != "--" else immigrant_df

            selected_org = st.selectbox("Select Organization", ["--"] + sub_df["Organization Name"].tolist())
            if selected_org != "--":
                org_row = sub_df[sub_df["Organization Name"] == selected_org].iloc[0]
                st.markdown("---")
                st.subheader(f"Details for: {selected_org}")
                st.markdown(f"**Contact Info:** {org_row['Contact Info']}")
                st.markdown(f"**Programs Offered:** {org_row['Programs Offered']}")
                st.markdown(f"**Location:** {org_row['Location']}")
                st.markdown(f"**Description:** {org_row['Description']}")
                st.markdown(f"**Website:** [{org_row['Website']}]({org_row['Website']})")
