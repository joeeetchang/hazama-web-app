import streamlit as st
import ee
import geemap.foliumap as geemap

st.set_page_config(layout="wide")
st.title("Global Flood Database")

# ee.Authenticate()
if not ee.data._initialized:
    ee.Authenticate()
    ee.Initialize()

Map = geemap.Map()
Map.setOptions('SATELLITE')

gfd = ee.ImageCollection('GLOBAL_FLOOD_DB/MODIS_EVENTS/V1')
# event list
event_list = gfd.limit(913).map(
    lambda img: img.set('label', ee.String('event ID: ')
                        .cat(img.get('id'))
                        .cat(' | ')
                        .cat(ee.Date(img.get('system:time_start')).format('YYYY-MM-dd'))
                        .cat(' ~ ')
                        .cat(ee.Date(img.get('system:time_end')).format('YYYY-MM-dd')))
)

#image list label
event_list = event_list.aggregate_array('label').getInfo()

selected_label = st.selectbox("select flood event", event_list)
selected_id = float(selected_label.split("event ID: ")[1].split(" | ")[0])

# loading image
event_img = gfd.filterMetadata('id', 'equals', selected_id).first()

# put image to center
Map.centerObject(event_img, 9)

Map.addLayer(
    event_img.select('flooded').selfMask(),
    {'min': 0, 'max': 1, 'palette': ['001133']},
    'Flooded Extent')

Map.addLayer(
    event_img.select('duration').selfMask(),
    {'min': 0, 'max': 4, 'palette': ['c3effe', '1341e8', '051cb0', '001133']},
    'Flood Duration')

# historical flood plain
#flood_sum = gfd.select('flooded').sum()
#Map.addLayer(
    #flood_sum.selfMask(),
    #{'min': 0, 'max': 10, 'palette': ['c3effe', '1341e8', '051cb0', '001133']},
    #'Historical Flood Plain')

# permenant water body
jrc = gfd.select('jrc_perm_water').sum().gte(1)
Map.addLayer(
    jrc.selfMask(),
    {'min': 0, 'max': 1, 'palette': ['C3EFFE']},
    'JRC Permanent Water')

Map.add_legend(title="Flooded", colors=["001133"], labels=["Inundated"])
Map.add_legend(title="Duration (days)", colors=['c3effe', '1341e8', '051cb0', '001133'],
               labels=['1', '2', '3', '4+'])

# info = event_img.getInfo()
# start = info['properties']['system:time_start']
# end = info['properties']['system:time_end']
# region_id = info['properties']['id']
# duration = info['properties']['duration']

# with st.sidebar:
#     st.markdown(f"**🌀 Event ID**: {region_id}")
#     st.markdown(f"**🗓 Start**: {ee.Date(start).format('YYYY-MM-dd').getInfo()}")
#     st.markdown(f"**🗓 End**: {ee.Date(end).format('YYYY-MM-dd').getInfo()}")
#     st.markdown(f"**📊 Duration**: {duration} days")


Map.to_streamlit(height=700)
