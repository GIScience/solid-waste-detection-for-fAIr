import csv
import shutil
import sys
from pathlib import Path


sources = [Path(sys.argv[1]), Path(sys.argv[2])]
output = Path(sys.argv[3])

if output.exists():
    shutil.rmtree(output)

for split in ("train", "val", "test"):
    for class_name in ("background", "waste"):
        class_dir = output / split / class_name
        class_dir.mkdir(parents=True)

count = 0
for source_number, source in enumerate(sources, start=1):
    for split in ("train", "val", "test"):
        for class_name in ("background", "waste"):
            for image in (source / split / class_name).glob("*.png"):
                name = f"{source_number}_{source.name}__{image.name}"
                shutil.copy2(image, output / split / class_name / name)
                count += 1

with (output / "scene_splits.csv").open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["dataset", "scene", "split", "background", "waste"])
    for source in sources:
        with (source / "scene_splits.csv").open(newline="", encoding="utf-8") as source_file:
            for row in list(csv.reader(source_file))[1:]:
                writer.writerow([source.name, *row])

print(f"Merged {count} images")
