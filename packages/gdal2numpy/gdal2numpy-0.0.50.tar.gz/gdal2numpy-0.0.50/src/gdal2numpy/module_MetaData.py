# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2022 Valerio for Gecosistema S.r.l.
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
#
# Name:        module_MetaData.py
# Purpose:
#
# Author:      Luzzi Valerio, Lorenzo Borelli
#
# Created:
# -------------------------------------------------------------------------------
import os
import numpy as np
from osgeo import osr, ogr
from osgeo import gdal, gdalconst
from .filesystem import forceext, justext


def GetRasterShape(filename):
    """
    GetRasterShape
    """
    ds = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if ds:
        m, n = ds.RasterYSize, ds.RasterXSize
        return m, n
    return 0, 0


def GetNoData(filename):
    """
    GetNoData
    """
    ds = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if ds:
        band = ds.GetRasterBand(1)
        no_data = band.GetNoDataValue()
        data, band, ds = None, None, None
        return no_data
    return None


def GetPixelSize(filename):
    """
    GetPixelSize
    """
    if isinstance(filename, str) and os.path.isfile(filename) and filename.lower().endswith(".tif"):
        ds = gdal.Open(filename, gdalconst.GA_ReadOnly)
        if ds:
            _, px, _, _, _, py = ds.GetGeoTransform()
        ds = None
        return px, np.abs(py)
    else:
        return None, None


def SamePixelSize(filename1, filename2, decimals=-1):
    """
    SamePixelSize
    """
    size1 = GetPixelSize(filename1)
    size2 = GetPixelSize(filename2)
    if decimals >= 0:
        size1 = [round(item, decimals) for item in size1]
        size2 = [round(item, decimals) for item in size2]
    return size1 == size2


def GetSpatialRef(filename):
    """
    GetSpatialRef
    """
    srs = None
    if isinstance(filename, osr.SpatialReference):
        srs = filename

    elif isinstance(filename, int):
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(filename)

    elif isinstance(filename, str) and filename.lower().startswith("epsg:"):
        code = int(filename.split(":")[1])
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(code)

    elif isinstance(filename, str) and filename.upper().startswith("+proj"):
        proj4text = filename
        srs = osr.SpatialReference()
        srs.ImportFromProj4(proj4text)

    elif isinstance(filename, str) and filename.upper().startswith("PROJCS["):
        wkt = filename
        srs = osr.SpatialReference()
        srs.ImportFromWkt(wkt)

    elif isinstance(filename, str) and os.path.isfile(filename) and filename.lower().endswith(".shp"):
        ds = ogr.OpenShared(filename)
        if ds:
            srs = ds.GetLayer().GetSpatialRef()
        ds = None

    elif isinstance(filename, str) and os.path.isfile(filename) and filename.lower().endswith(".tif"):
        ds = gdal.Open(filename, gdalconst.GA_ReadOnly)
        if ds:
            wkt = ds.GetProjection()
            srs = osr.SpatialReference()
            srs.ImportFromWkt(wkt)
        ds = None
    else:
        srs = osr.SpatialReference()

    return srs


def SameSpatialRef(filename1, filename2):
    """
    SameSpatialRef
    """
    srs1 = GetSpatialRef(filename1)
    srs2 = GetSpatialRef(filename2)
    if srs1 and srs2:
        return srs1.IsSame(srs2)
    return None


def Rectangle(minx, miny, maxx, maxy):
    """
    Rectangle - create ogr polygon from bbox
    """
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint_2D(minx, miny)
    ring.AddPoint_2D(maxx, miny)
    ring.AddPoint_2D(maxx, maxy)
    ring.AddPoint_2D(minx, maxy)
    ring.AddPoint_2D(minx, miny)
    # Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    return poly


def GetExtent(filename, t_srs=None):
    """
    GetExtent
    """
    s_srs = None
    minx, miny, maxx, maxy = 0, 0, 0, 0
    ext = justext(filename).lower()
    if ext == "tif":
        ds = gdal.Open(filename, gdalconst.GA_ReadOnly)
        if ds:
            "{xmin} {ymin} {xmax} {ymax}"
            m, n = ds.RasterYSize, ds.RasterXSize
            gt = ds.GetGeoTransform()
            minx, px, _, maxy, _, py = gt
            maxx = minx + n * px
            miny = maxy + m * py
            miny, maxy = min(miny, maxy), max(miny, maxy)
            wkt = ds.GetProjection()
            s_srs = osr.SpatialReference()
            s_srs.ImportFromWkt(wkt)
            ds = None

    elif ext in ("shp", "dbf"):

        filename = forceext(filename, "shp")
        driver = ogr.GetDriverByName("ESRI Shapefile")
        ds = driver.Open(filename, 0)
        if ds:
            layer = ds.GetLayer()
            minx, maxx, miny, maxy = layer.GetExtent()
            s_srs = layer.GetSpatialRef()
            ds = None

    if t_srs and not SameSpatialRef(s_srs, t_srs):
        transform = osr.CoordinateTransformation(s_srs, GetSpatialRef(t_srs))
        rect = Rectangle(minx, miny, maxx, maxy)
        rect.Transform(transform)
        if f"{t_srs}" == "4326":
            miny, maxy, minx, maxx = rect.GetEnvelope()
        else:
            minx, miny, maxx, maxy = rect.GetEnvelope()

        miny, maxy = min(miny, maxy), max(miny, maxy)

    return minx, miny, maxx, maxy


def SameExtent(filename1, filename2, decimals=-1):
    """
    SameExtent
    """
    extent1 = GetExtent(filename1)
    extent2 = GetExtent(filename2)
    if decimals >= 0:
        extent1 = [round(item, decimals) for item in extent1]
        extent2 = [round(item, decimals) for item in extent2]
    return extent1 == extent2


def GetMetaData(filename):
    """
    GetMetaData - get metadata from filename
    :param filename: the pathname
    :return: returns a dictionary with metadata
    """
    ds = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if ds:
        m, n = ds.RasterYSize, ds.RasterXSize
        band = ds.GetRasterBand(1)
        gt = ds.GetGeoTransform()
        wkt = ds.GetProjection()
        meta = ds.GetMetadata()
        nodata = band.GetNoDataValue()
        minx, px, _, maxy, _, py = gt
        maxx = minx + n * px
        miny = maxy + m * py
        miny, maxy = min(miny, maxy), max(miny, maxy)
        ds = None
        return {
            "m": m,
            "n": n,
            "px": px,
            "py": py,
            "wkt": wkt,
            "nodata": nodata,
            "extent": [minx, miny, maxx, maxy],
            "metadata": meta
        }
    return {}


def GetTag(filename, tagname, band=0):
    """
    GetTag - get a tag in metadata of the file or of the band if specified
    """
    ds = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if ds:
        if not band:
            metadata = ds.GetMetadata()
        elif 0 < band <= ds.RasterCount:
            metadata = ds.GetRasterBand(band).GetMetadata()
        else:
            metadata = {}
        if tagname in metadata:
            ds = None
            return metadata[tagname]
    ds = None
    return None


def SetTag(filename, tagname, tagvalue="", band=0):
    """
    SetTag - set a tag in metadata of the file or of the band if specified
    """
    ds = gdal.Open(filename, gdalconst.GA_Update)
    if ds:
        if tagname:
            if not band:
                metadata = ds.GetMetadata()
                metadata[tagname] = f"{tagvalue}"
                ds.SetMetadata(metadata)
            elif 0 < band <= ds.RasterCount:
                metadata = ds.GetRasterBand(band).GetMetadata()
                metadata[tagname] = f"{tagvalue}"
                ds.GetRasterBand(band).SetMetadata(metadata)

        ds.FlushCache()
        ds = None
