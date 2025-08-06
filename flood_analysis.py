# flood_analysis.py

import ee
import geemap.foliumap as geemap

def run_flood_analysis():
    # Define the region of interest
    geometry = ee.Geometry.Polygon([[
        [106.34954329522984,-6.449380562588049],
        [107.33007308038609,-6.449380562588049],
        [107.33007308038609,-5.900522745264385],
        [106.34954329522984,-5.900522745264385]
    ]])

    # Center map on geometry
    Map = geemap.Map()
    Map.centerObject(geometry, 10)

    # SAR before flood event
    sar_before = (ee.ImageCollection("COPERNICUS/S1_GRD")
        .filterDate('2019-12-20', '2019-12-29')
        .filterBounds(geometry)
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
        .filter(ee.Filter.eq('instrumentMode', 'IW'))
        .filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))
        .select('VV')
        .map(lambda img: img.focalMean(60, 'square', 'meters')
             .copyProperties(img, img.propertyNames()))
    )

    # SAR after flood event
    sar_after = (ee.ImageCollection("COPERNICUS/S1_GRD")
        .filterDate('2019-12-30', '2020-01-03')
        .filterBounds(geometry)
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
        .filter(ee.Filter.eq('instrumentMode', 'IW'))
        .filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))
        .select('VV')
        .map(lambda img: img.focalMean(60, 'square', 'meters')
             .copyProperties(img, img.propertyNames()))
    )

    # Compute difference
    change = sar_before.min().subtract(sar_after.min())

    # Load water mask
    water_mask = (ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1")
        .select('label')
        .filterDate('2018', '2021')
        .filterBounds(geometry)
        .mode()
        .eq(0)
        .Not()
    )

    # Threshold + water mask
    thr = change.gt(5).updateMask(water_mask)
    flooded = thr.updateMask(thr)

    # Flood area calculation
    area_img = flooded.multiply(ee.Image.pixelArea().divide(1e6))
    flood_area = area_img.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=geometry,
        scale=60
    )

    flood_area_km2 = flood_area.getInfo()

    # Add map layers
    Map.addLayer(sar_before.min().clip(geometry), {}, "SAR Before")
    Map.addLayer(sar_after.min().clip(geometry), {}, "SAR After")
    Map.addLayer(change.clip(geometry), {}, "Change")
    Map.addLayer(flooded.clip(geometry), {"palette": ["blue"]}, "Flooded")

    return Map, flood_area_km2
