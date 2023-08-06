# Standard library imports
import os
from glob import glob
from pathlib import Path
from typing import Optional

from ..georeferencing import georeference
from .clip_labels import clip_labels
from .fix_labels import fix_labels


def preprocess(
    input_path: str,
    mask_path: str,
    rasterize=False,
    image_path: Optional[str] = None,
) -> None:
    """Fully preprocess the input data.

    Args:
        input_path: Path of the directory where the input data are stored.
        mask_path: Path of the directory where the GeoJSON masks will go.
        rasterize: Whether to include the raster masks or not.
        image_path: Path of the directory where the georereferenced images will go.
            This argument is optional. No georeferenced images will be produced if
            this argument is skipped.

    Example::

        preprocess(
            "data/inputs_v2",
            "data/masks_v2",
            rasterize=True
        )
    """
    for path in glob(f"{input_path}/*"):
        sub_dir = Path(path).stem
        if image_path:
            georeference(path, f"{image_path}/{sub_dir}")

        fix_labels(
            f"{path}/labels.geojson",
            f"{path}/corrected_labels.geojson",
        )
        clip_labels(path, f"{mask_path}/{sub_dir}", rasterize)
        os.remove(f"{path}/corrected_labels.geojson")
