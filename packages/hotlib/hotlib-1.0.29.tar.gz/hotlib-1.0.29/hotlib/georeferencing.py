# Standard library imports
import os
from glob import glob
from pathlib import Path

from .utils import get_bounding_box


def georeference(input_path: str, output_path: str, is_mask=False) -> None:
    """Perform georeferencing and remove the fourth band from images (if any).

    Here, the EPSG:4326 coordinate reference system (aka WGS 84) is used. 

    Args:
        input_path: Path of the directory where the input data are stored.
        output_path: Path of the directory where the output data will go.
        is_mask: Whether the image is binary or not.

    Example::

        georeference(
            "data/prediction-dataset/5x5/1-19", 
            "data/georeferenced_input/1-19"
        )
    """
    os.makedirs(output_path, exist_ok=True)

    for path in glob(f"{input_path}/*.png"):
        filename = Path(path).stem
        x_min, y_max, x_max, y_min = get_bounding_box(filename)

        process_image = f"""
            gdal_translate \
                -b 1 {'' if is_mask else '-b 2 -b 3'} \
                -a_ullr {x_min} {y_max} {x_max} {y_min} \
                -a_srs EPSG:4326 \
                {input_path}/{filename}.png \
                {output_path}/{filename}.tif
        """
        os.system(process_image)
