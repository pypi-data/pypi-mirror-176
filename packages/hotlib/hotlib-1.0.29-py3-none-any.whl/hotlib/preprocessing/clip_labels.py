import os
from glob import glob

from ..utils import get_bounding_box, get_prefix


def clip_labels(input_path: str, output_path: str, rasterize=False) -> None:
    """Rasterize the GeoJSON labels for each of the aerial images.

    For each of the OAM images, the corresponding GeoJSON files are
    clipped first. Then, the clipped GeoJSON files are converted to TIFs.

    Args:
        input_dir: Name of the directory where the input data are stored.
        sub_dir: Name of the sub-directory under the input directory.
        out_dir: Name of the directory where the output data will go.
    """
    os.makedirs(output_path, exist_ok=True)

    for path in glob(f"{input_path}/*.png"):
        filename = get_prefix(path)
        x_min, y_max, x_max, y_min = get_bounding_box(filename)

        clip_labels = f"""
            ogr2ogr \
                -clipsrc {x_min} {y_max} {x_max} {y_min} \
                -f GeoJSON \
                {output_path}/{filename}.geojson \
                {input_path}/labels.geojson
        """
        os.system(clip_labels)

        if rasterize:
            rasterize_labels = f"""
                gdal_rasterize \
                    -ot Byte \
                    -burn 255 \
                    -ts 256 256 \
                    -te {x_min} {y_max} {x_max} {y_min} \
                    {output_path}/{filename}.geojson \
                    {output_path}/{filename}.tif \
                    -a_ullr {x_min} {y_max} {x_max} {y_min} \
                    -a_srs EPSG:4326
            """
            os.system(rasterize_labels)
