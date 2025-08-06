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

# service_account = 'changsome.1@gmail.com'
# private_key = 'global-flood-mapping-db762f1c1e40.json'
load_dotenv("ee_key.env") # take environment variables from .env.

service_account = os.getenv("EE_SERVICE_ACCOUNT")
private_key = os.getenv("PRIVATE_KEY")
# service_account, private_key
# changsome.1@gmail.com, global-flood-mapping-db762f1c1e40.json
credentials = ee.ServiceAccountCredentials(service_account, private_key)
ee.Initialize(credentials)

print(ee. String('GEE initialized').getInfo())

# if not ee.data._initialized:
#     ee.Authenticate()
#     ee.Initialize()

# basemap
m = geemap.Map()

# button
if st.button("▶ flood detection"):
    with st.spinner("processing..."):
        m, flood_area = run_flood_analysis()
        st.success(f"✅ flooded area: {flood_area['VV']:.2f} Km2")

# show st map 
m.to_streamlit(height=600)

