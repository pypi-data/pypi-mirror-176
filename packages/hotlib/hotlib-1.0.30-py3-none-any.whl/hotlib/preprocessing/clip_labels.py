# Standard library imports
import os
from glob import glob
from pathlib import Path

# Third-party imports
import geopandas
from osgeo import gdal
from shapely.geometry import box
from tqdm import tqdm

from ..utils import get_bounding_box


def clip_labels(input_path: str, output_path: str, rasterize=False) -> None:
    """Rasterize the GeoJSON labels for each of the aerial images.

    For each of the OAM images, the corresponding GeoJSON files are
    clipped first. Then, the clipped GeoJSON files are converted to TIFs.

    The EPSG:3857 projected coordinate system is used
    ('WGS 84 / Pseudo-Mercator', coordinates in meters).

    Args:
        input_path: Path of the directory where the input data are stored.
        output_path: Path of the directory where the output data will go.
        rasterize: Whether to rasterize the clipped labels.
    """
    os.makedirs(output_path, exist_ok=True)

    for path in tqdm(
        glob(f"{input_path}/*.png"), desc=f"Clipping labels for {Path(input_path).stem}"
    ):
        filename = Path(path).stem
        geojson_file_all_labels = f"{input_path}/labels_epsg3857.geojson"
        clipped_geojson_file = f"{output_path}/{filename}.geojson"
        raster_file = f"{output_path}/{filename}.tif"

        # Bounding box as a tuple
        x_min, y_min, x_max, y_max = get_bounding_box(filename)
        # Bounding box as a polygon
        bounding_box_polygon = box(x_min, y_min, x_max, y_max)

        # Read all labels into a GeoDataFrame, clip it and write to GeoJSON
        gdf_all_labels = geopandas.read_file(geojson_file_all_labels)
        gdf_clipped = gdf_all_labels.clip(bounding_box_polygon)
        if len(gdf_clipped) > 0:
            gdf_clipped.to_file(clipped_geojson_file)
        else:
            schema = {"geometry": "Polygon", "properties": {"id": "int"}}
            crs = "EPSG:3857"
            gdf_clipped.to_file(clipped_geojson_file, schema=schema, crs=crs)

        if rasterize:
            # Rasterize clipped labels
            _ = gdal.Rasterize(
                destNameOrDestDS=raster_file,
                srcDS=clipped_geojson_file,
                format="GTiff",
                outputType=gdal.GDT_Byte,
                outputBounds=[x_min, y_min, x_max, y_max],
                width=256,
                height=256,
                burnValues=[255],
            )
            # Close raster dataset
            _ = None
