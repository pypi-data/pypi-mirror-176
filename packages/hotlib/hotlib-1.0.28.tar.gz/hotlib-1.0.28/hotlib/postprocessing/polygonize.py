import os

from .get_polygons import get_polygons
from .merge_polygons import merge_polygons


def polygonize(input_path: str, output_path: str) -> None:
    """Vectorize raster tiles.

    Args:
        input_path: Path of the directory where the TIF files are stored.
        output_path: Path of the output file.

    Example::

        vectorize("data/masks_v2/4", "labels.geojson")
    """
    get_polygons(input_path, "temp-labels.geojson", kernel_opening=1)
    merge_polygons("temp-labels.geojson", output_path, distance_threshold=0.5)
    os.remove("temp-labels.geojson")