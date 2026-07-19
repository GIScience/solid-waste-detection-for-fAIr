import csv
import random
import shutil
import sys
from collections import defaultdict
from pathlib import Path


source = Path(sys.argv[1])
output = Path(sys.argv[2])

if output.exists():
    shutil.rmtree(output)
for split in ("train", "val", "test"):
    for class_name in ("background", "waste"):
        (output / split / class_name).mkdir(parents=True)

scenes = defaultdict(list)
for split in ("train", "val", "test"):
    for class_name in ("background", "waste"):
        for image in (source / split / class_name).glob("*.png"):
            scene = image.stem.rsplit("_", 1)[0]
            scenes[scene].append((image, class_name))

scene_names = sorted(scenes)
random.Random(42).shuffle(scene_names)
n_train = round(len(scene_names) * 0.70)
n_val = round(len(scene_names) * 0.15)
scene_splits = {
    scene: "train" if i < n_train else "val" if i < n_train + n_val else "test"
    for i, scene in enumerate(scene_names)
}

rows = []
for scene in sorted(scene_names):
    split = scene_splits[scene]
    counts = {"background": 0, "waste": 0}
    for image, class_name in scenes[scene]:
        shutil.copy2(image, output / split / class_name / image.name)
        counts[class_name] += 1
    rows.append([scene, split, counts["background"], counts["waste"]])

with (output / "scene_splits.csv").open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["scene", "split", "background", "waste"])
    writer.writerows(rows)

print(f"Created {sum(len(images) for images in scenes.values())} images from {len(scenes)} scenes")
