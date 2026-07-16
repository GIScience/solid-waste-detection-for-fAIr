import json
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import country_converter as coco
import geopandas as gpd
from pyproj import CRS, Geod
from shapely.geometry import shape


API = "https://api.openaerialmap.org/meta"
UCDB_LAYER = "GHS_UCDB_THEME_GENERAL_CHARACTERISTICS_GLOBE_R2024A"
MAX_GSD_M = 0.06
MIN_AREA_KM2 = 1.0
GEOD = Geod(ellps="WGS84")


def resolution_m(item):
    properties = item.get("properties", {})
    if "resolution_in_meters" in properties:
        return properties["resolution_in_meters"]

    gsd = item["gsd"]
    if CRS.from_wkt(item["projection"]).is_geographic:
        lon, lat = shape(item["geojson"]).centroid.coords[0]
        return GEOD.inv(lon, lat, lon + gsd, lat)[2]
    return gsd


def query_oam():
    page = 1
    while True:
        url = f"{API}?{urlencode({'page': page, 'limit': 1000})}"
        with urlopen(url) as response:
            data = json.load(response)
        yield from data["results"]
        print(f"OAM page {page}")
        if page * data["meta"]["limit"] >= data["meta"]["found"]:
            break
        page += 1


ucdb_path = Path(sys.argv[1])
output = Path(sys.argv[2])
output.mkdir(parents=True, exist_ok=True)

records = []
for item in query_oam():
    geometry = shape(item["geojson"])
    gsd_m = resolution_m(item)
    area_km2 = abs(GEOD.geometry_area_perimeter(geometry)[0]) / 1_000_000
    if gsd_m <= MAX_GSD_M and area_km2 >= MIN_AREA_KM2:
        records.append(
            {
                "oam_id": item["_id"],
                "title": item.get("title"),
                "provider": item.get("provider"),
                "platform": item.get("platform"),
                "sensor": item.get("properties", {}).get("sensor"),
                "acquired": item.get("acquisition_start"),
                "gsd_cm": round(gsd_m * 100, 3),
                "area_km2": round(area_km2, 3),
                "bbox": json.dumps(item["bbox"]),
                "download": item["uuid"],
                "geometry": geometry,
            }
        )

scenes = gpd.GeoDataFrame(records, crs="EPSG:4326")
urban = gpd.read_file(ucdb_path, layer=UCDB_LAYER).to_crs("EPSG:4326")
urban = urban[
    [
        "ID_UC_G0",
        "GC_UCN_MAI_2025",
        "GC_CNT_GAD_2025",
        "GC_CNT_UNN_2025",
        "GC_UCA_KM2_2025",
        "GC_POP_TOT_2025",
        "geometry",
    ]
].rename(
    columns={
        "ID_UC_G0": "ucdb_id",
        "GC_UCN_MAI_2025": "city",
        "GC_CNT_GAD_2025": "country",
        "GC_CNT_UNN_2025": "country_un",
        "GC_UCA_KM2_2025": "ucdb_area_km2",
        "GC_POP_TOT_2025": "ucdb_population",
    }
)
country_un = urban.pop("country_un").replace({"China, Taiwan Province of China": "China"})
urban["continent"] = coco.convert(names=country_un, to="continent_7")

matches = gpd.sjoin(scenes, urban, predicate="intersects").drop(columns="index_right")
matches = matches.drop_duplicates("oam_id")
matches.to_file(output / "oam_urban_scenes.gpkg", layer="scenes", driver="GPKG")
matches.drop(columns="geometry").to_csv(output / "oam_urban_scenes.csv", index=False)
print(f"Selected {len(matches)} scenes")
