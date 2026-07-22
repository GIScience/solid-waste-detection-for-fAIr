# YOLO Solid Waste Analysis for Spatial Grid (SWAG)


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repo contains the labels and scripts for the **YOLO Solid Waste Analysis for Spatial Grid (SWAG)** for detecting solid waste piles from UAV imagery.
The model is based on a previous work, that can be found [here](https://doi.org/10.48550/arXiv.2605.02316).

YOLO SWAG (Solid Waste Analysis on spatial Grids) is a pretrained YOLO26x-cls model for 
semantic segmentation of solid waste piles in UAV (drone) imagery. The model classifies 5m x 5m grid cells as either 
"waste" or "background" based on polygon labels, enabling efficient waste detection in OpenAerialMap (OAM) scenes and other aerial datasets.

## How to use the data

The GPKG-files in *./data/labels* are following this naming schema: `{continent}_{country}_{city}_{openaerialmap_id}_tiles.gpkg`.
The original labels from the previous work are included aswell and follow the schema `{openaerialmap_id}_tiles.gpkg`
Download the aerial images from [OpenAerialMap](https://openaerialmap.org/). After that run:

```shell
uv run python scripts/create_labeling_grid.py <path/to/oam_files> <path/to/output/directoy>
```

The content of the output directory can be loaded into QGIS or similar applications for labelling. Tiles containing 
waste piles are labelled with class "1" and background with class "2".

## Training scene distribution

The training scenes cover locations across the World Bank regions shown below.

![World map showing the geographic distribution of OpenAerialMap training scenes](data/images/Overview.png)

## Scene-wise cross-validation

The YOLO classifier was evaluated with 10 scene-held-out cross-validation folds. Each fold keeps all tiles from a scene in the same split, preventing spatial leakage between training, validation, and test data. Results are reported as mean ± standard deviation across folds.

| Split | Top-1 accuracy |
|---|---:|
| Train | 92.60% ± 1.51% |
| Validation | 92.62% ± 1.53% |
| Test | **91.32% ± 3.16%** |

The mean held-out-scene accuracy is 91.3%. The close training and validation performance suggests limited average overfitting, while the larger test variation indicates that some scenes are more challenging than others. Top-5 accuracy was 100% in every fold and is not informative for this task because there are fewer than five classes.

## Examples

![example_senegal](data/images/example_senegal.png)
![example](data/images/example.png)
![example_buildings](data/images/example_buildings.png)
