import streamlit as st
import geemap.foliumap as geemap
import ee
from flood_analysis import run_flood_analysis

st.title("Glabal HAZAMA Web App")
st.set_page_config(layout="wide")

st.markdown('#### this is a test demo for HAZAMA')


# ee.Authenticate()
if not ee.data._initialized:
    ee.Authenticate()
    ee.Initialize()

# basemap
m = geemap.Map()

# button
if st.button("▶ flood detection"):
    with st.spinner("processing..."):
        m, flood_area = run_flood_analysis()
        st.success(f"✅ flooded area: {flood_area['VV']:.2f} Km2")

# show st map 
m.to_streamlit(height=600)

