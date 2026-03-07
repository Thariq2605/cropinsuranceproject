import ee

def get_ndvi(lat, lon):

    ee.Initialize(project="spheric-vine-453603-i2")

    point = ee.Geometry.Point([lon, lat])

    collection = (
        ee.ImageCollection("COPERNICUS/S2")
        .filterBounds(point)
        .first()
    )

    ndvi = collection.normalizedDifference(['B8','B4'])

    return ndvi.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=point,
        scale=10
    ).getInfo()

    return stats.getInfo()


def get_ndvi_heatmap(lat, lon):

    point = ee.Geometry.Point([lon, lat])
    area = point.buffer(500)

    image = (
        ee.ImageCollection("COPERNICUS/S2")
        .filterBounds(area)
        .sort("CLOUDY_PIXEL_PERCENTAGE")
        .first()
    )

    ndvi = image.normalizedDifference(['B8','B4']).rename('NDVI')

    vis = {
        "min": 0,
        "max": 1,
        "palette": ["red","yellow","green"]
    }

    map_id = ndvi.getMapId(vis)

    # create viewer link
    url = f"https://earthengine.google.com/map/{map_id['mapid']}"

    return url