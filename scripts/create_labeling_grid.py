
import math
import shutil
import sys
from pathlib import Path

import geopandas as gpd
import rasterio
from shapely.geometry import box


TILE_SIZE = 5
STYLE = Path(__file__).with_name("labeling_grid.qml")


def create_grid(tif: Path, target: Path) -> None:
    scene_id = tif.stem
    scene_dir = target / scene_id
    scene_dir.mkdir(parents=True, exist_ok=True)

    with rasterio.open(tif) as image:
        footprint = gpd.GeoSeries([box(*image.bounds)], crs=image.crs)

    grid_crs = footprint.estimate_utm_crs() if footprint.crs.is_geographic else footprint.crs
    min_x, min_y, max_x, max_y = footprint.to_crs(grid_crs).total_bounds
    cols = math.ceil((max_x - min_x) / TILE_SIZE)
    rows = math.ceil((max_y - min_y) / TILE_SIZE)
    cells = [
        (row, col, box(
            min_x + col * TILE_SIZE,
            min_y + row * TILE_SIZE,
            min_x + (col + 1) * TILE_SIZE,
            min_y + (row + 1) * TILE_SIZE,
        ))
        for row in range(rows)
        for col in range(cols)
    ]

    grid = gpd.GeoDataFrame(
        {
            "tile_id": range(len(cells)),
            "scene_id": [scene_id] * len(cells),
            "row": [cell[0] for cell in cells],
            "col": [cell[1] for cell in cells],
            "filename": [f"{scene_id}_{i:06d}.png" for i in range(len(cells))],
            "label": [None] * len(cells),
        },
        geometry=[cell[2] for cell in cells],
        crs=grid_crs,
    )

    shutil.copy2(tif, scene_dir / tif.name)
    grid.to_file(scene_dir / f"{scene_id}_tiles.gpkg", layer="tiles", driver="GPKG")
    shutil.copy2(STYLE, scene_dir / f"{scene_id}_tiles.qml")
    print(f"{scene_id}: {len(grid)} tiles")


source = Path(sys.argv[1])
target = Path(sys.argv[2])
tifs = [source] if source.is_file() else sorted([*source.glob("*.tif"), *source.glob("*.tiff")])

for tif in tifs:
    create_grid(tif, target)
