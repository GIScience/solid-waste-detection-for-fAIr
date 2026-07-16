from pathlib import Path
import sys

import geopandas as gpd
import rasterio
from PIL import Image
from rasterio.windows import from_bounds


root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    "data/research_area_candidates/labeling_grids/all_to_label"
)
class_names = {"0": "background", "1": "waste"}

for gpkg in sorted(root.glob("*/*.gpkg")):
    scene_dir = gpkg.parent
    tif = next(scene_dir.glob("*.tif"))
    labels = gpd.read_file(gpkg, layer="tiles", where="label IS NOT NULL")

    with rasterio.open(tif) as image:
        labels = labels.to_crs(image.crs)
        for tile in labels.itertuples():
            output = scene_dir / "labeled_tiles" / class_names[str(tile.label)] / tile.filename
            output.parent.mkdir(parents=True, exist_ok=True)

            window = from_bounds(*tile.geometry.bounds, transform=image.transform)
            crop = image.read(window=window.round_offsets().round_lengths())
            crop = crop[0] if crop.shape[0] == 1 else crop[:3].transpose(1, 2, 0)
            Image.fromarray(crop).save(output)

    print(f"{scene_dir.name}: {len(labels)} crops")
