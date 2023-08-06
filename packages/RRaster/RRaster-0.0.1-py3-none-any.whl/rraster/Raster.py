from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import rasterio as rio
from rasterio.warp import reproject, Resampling
from typing import List, Union


class Raster(object):
    """
    Wrapper around rasterio functions to have simpler syntax and match the logic used by the R Raster library.
    A raster can either be read from disk or created from a numpy array with an affine transformation and nodata
    value specification.

    Attributes:
        arr: array containing the raster data
        nodata: The no data value of the raster.
        transform: The affine transformation of the raster.
        profile: All other associated raster metadata.
    """

    def __init__(self, rst: Union[np.ndarray, str, Path], band: Union[int, List[int]] = 1, **kwargs):

        # Instantiate from raster on disk.
        if isinstance(rst, (str, Path)):
            rst = Path(rst)
            if not rst.exists():
                raise FileNotFoundError(f'Error! The provided raster ({rst}) does not exist.')

            with rio.open(rst) as tmp:
                self.arr = tmp.read(band)
                self.nodata = tmp.nodata
                self.transform = tmp.transform
                self.profile = tmp.profile
                self.arr = self.arr.astype(np.float32)
                self.arr[self.arr == self.nodata] = np.nan

        # Instantiate from np array.
        elif isinstance(rst, np.ndarray):

            assert all([x in kwargs for x in ['nodata', 'transform']]), "'nodata' and 'transform' must both be kwargs" \
                                                                        "when creating a raster from an array."
            self.arr = rst
            self.nodata = kwargs['nodata']
            self.transform = kwargs['transform']
            self.profile = {'crs': kwargs['crs'] if 'crs' in kwargs else None,
                            'height': kwargs['height'] if 'height' in kwargs else self.arr.shape[0],
                            'width': kwargs['width'] if 'width' in kwargs else self.arr.shape[1],
                            'count': kwargs['count'] if 'count' in kwargs else 1,  # TODO: Use better logic here.
                            'dtype': kwargs['dtype'] if 'dtype' in kwargs else 'float32'}
            self.profile.update(kwargs)
        else:
            raise TypeError('Error! "rst" must be a np.array, str or Path object')

        # Map str of data types to actual data types
        self.dt_map = {
            'float32': np.float32,
            'float64': np.float64,
            'int8': np.int8,
            'int16': np.int16
        }

    def plot(self):
        """
        Simple display of the raster using matplotlib.
        """
        # Copy raster so we can filter out nodata values without changing the array already in memory.
        tmp = self.arr.copy()
        tmp = tmp.astype(np.float32)
        tmp[tmp == self.nodata] = np.nan

        plt.imshow(tmp)
        plt.colorbar()
        plt.show()

    def write(self, save_name: Union[str, Path], **kwargs):
        """
        Write raster to disk.
        :param save_name: Desired path and filename of
        :param kwargs: Additional kwargs to pass to rio.open function.
        :return: None, saves raster to disk.
        """

        count = kwargs.pop('count') if 'count' in kwargs else self.profile['count']
        nodata = kwargs.pop('nodata') if 'nodata' in kwargs else self.nodata

        out_dst = rio.open(
            save_name,
            'w',
            driver='GTiff',
            height=kwargs.pop('height') if 'height' in kwargs else self.profile['height'],
            width=kwargs.pop('width') if 'width' in kwargs else self.profile['width'],
            count=count,
            dtype=kwargs.pop('dtype') if 'dtype' in kwargs else self.profile['dtype'],
            nodata=nodata,
            transform=kwargs.pop('transform') if 'transform' in kwargs else self.transform,
            crs=kwargs.pop('crs') if 'crs' in kwargs else self.profile['crs'],
            **kwargs
        )

        dt = self.dt_map[kwargs['dtype']] if 'dtype' in kwargs else np.float32

        arr = np.nan_to_num(self.arr, nan=nodata)
        if count == 1:
            out_dst.write(arr.astype(dt)[np.newaxis])
        else:
            out_dst.write(arr.astype(dt))

        out_dst.close()

    def crop(self, other):
        raise NotImplementedError('This function has not been implemented yet!')

    def reproject(self, other: Raster, method: str = 'bilinear', crs=None):
        """
        :param other: Raster object with the desired CRS and spatial resolution. The source raster will be
        transformed to match this raster's projection.
        :param method: The reprojection method to use. Must be one of 'bilinear', 'nearest', or 'cubic'.
        :param crs: The CRS of the source raster. If CRS is none, it is assumed that it is WGS84 (EPSG:4326).
        """
        if crs is None:
            crs = {'init': 'EPSG:4326'}

        assert method in ['nearest', 'bilinear', 'cubic'], 'Error! method must be one of "nearest", "bilinear", ' \
                                                           'or "cubic". '
        methods = {
            'nearest': Resampling.nearest,
            'bilinear': Resampling.bilinear,
            'cubic': Resampling.cubic
        }

        dst = np.zeros_like(other.arr, dtype=np.float32)
        arr, transform = reproject(
            self.arr,
            dst,
            src_transform=self.transform,
            src_crs=self.profile['crs'] if self.profile['crs'] is not None else crs,
            dst_transform=other.transform,
            dst_crs=other.profile['crs'],
            dst_nodata=np.nan,
            resampling=methods[method])

        profile = self.profile.copy()
        profile['width'] = other.profile['width']
        profile['height'] = other.profile['height']
        profile['transform'] = transform
        profile['crs'] = other.profile['crs']

        return Raster(rst=arr, **profile)

    def __add__(self, other: Union[Raster, int, float]):
        if isinstance(other, Raster):
            assert self.arr.shape == other.arr.shape, f'Error! Rasters have different shapes. Raster 1 has shape ' \
                                                      f'{self.arr.shape} and raster 2 has shape {other.arr.shape}'
            tmp = self.arr + other.arr
        else:
            tmp = self.arr + other
        return Raster(tmp, **self.profile)

    def __mul__(self, other: Union[Raster, int, float]):
        if isinstance(other, Raster):
            assert self.arr.shape == other.arr.shape, f'Error! Rasters have different shapes. Raster 1 has shape ' \
                                                      f'{self.arr.shape} and raster 2 has shape {other.arr.shape}'
            tmp = self.arr * other.arr
        else:
            tmp = self.arr * other
        return Raster(tmp, **self.profile)

    def __sub__(self, other: Union[Raster, int, float]):
        if isinstance(other, Raster):
            assert self.arr.shape == other.arr.shape, f'Error! Rasters have different shapes. Raster 1 has shape ' \
                                                      f'{self.arr.shape} and raster 2 has shape {other.arr.shape}'
            tmp = self.arr - other.arr
        else:
            tmp = self.arr - other
        return Raster(tmp, **self.profile)

    def __truediv__(self, other: Union[Raster, int, float]):
        if isinstance(other, Raster):
            assert self.arr.shape == other.arr.shape, f'Error! Rasters have different shapes. Raster 1 has shape ' \
                                                      f'{self.arr.shape} and raster 2 has shape {other.arr.shape}'
            tmp = self.arr / other.arr
        else:
            tmp = self.arr / other
        return Raster(tmp, **self.profile)

    def __repr__(self):
        return f"raster of size {self.profile['height']} x {self.profile['width']}\ncrs: {self.profile['crs']}\n" \
               f"number of bands: {self.profile['count']} "


class RasterStack(object):
    """
    Class to handle multiple Raster objects.

    Attributes:
        rasters: List of Raster objects (all rasters should share nodata, affine and transform attributes).
        nodata: The no data value of the raster objects.
        transform: Affine transformation for all rasters.
        profile: All other raster metadata.
    """

    def __init__(self, *args):
        assert all([isinstance(x, (str, Path, Raster)) for x in args]), 'Error! All rasters must be the same format.'
        if not isinstance(args[0], Raster):
            args = [Raster(x) for x in args]

        self.rasters = args
        self.nodata = self.rasters[0].nodata
        self.transform = self.rasters[0].transform
        self.profile = self.rasters[0].profile

    def reduce(self, fun, axis=0):
        """
        :param fun: A numpy function to apply to the stack of rasters (e.g. np.mean)
        :param axis: The axis to apply the function across. In most cases should be zero.
        """
        arr = np.array([x.arr for x in self.rasters])
        tmp = fun(arr, axis=axis)
        return Raster(tmp, **self.profile)
