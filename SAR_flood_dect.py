import streamlit as st
import geemap.foliumap as geemap
import ee
from flood_analysis import run_flood_analysis
import os
from dotenv import load_dotenv

st.title("Glabal HAZAMA Web App")
st.set_page_config(layout="wide")

st.markdown('#### this is a test demo for HAZAMA')



# ee.Authenticate()

load_dotenv("ee_key.env") # take environment variables from .env.

service_account = os.getenv("EE_SERVICE_ACCOUNT")
private_key = os.getenv("PRIVATE_KEY")
credentials = ee.ServiceAccountCredentials(service_account, private_key)
ee.Initialize(credentials)

print(ee. String('GEE initialized').getInfo())


# basemap
m = geemap.Map()

# button
if st.button("▶ flood detection"):
    with st.spinner("processing..."):
        m, flood_area = run_flood_analysis()
        st.success(f"✅ flooded area: {flood_area['VV']:.2f} Km2")

# show st map 
m.to_streamlit(height=600)

