
import sys
from osgeo import gdal, osr
def gdal_read_geotiff(sFilename_in):
    pDriver = gdal.GetDriverByName('GTiff')
    pDriver.Register()
    pDataset = gdal.Open(sFilename_in, gdal.GA_ReadOnly)

    if pDataset is None:
        print("Couldn't open this file: " + sFilename_in)
        sys.exit("Try again!")
    else:       
        pProjection = pDataset.GetProjection()

        pDataset.GetMetadata()
       
        ncolumn = pDataset.RasterXSize
        nrow = pDataset.RasterYSize
        nband = pDataset.RasterCount

        pGeotransform = pDataset.GetGeoTransform()
        dOriginX = pGeotransform[0]
        dOriginY = pGeotransform[3]
        dPixelWidth = pGeotransform[1]
        pPixelHeight = pGeotransform[5]

        pBand = pDataset.GetRasterBand(1)

        # Data type of the values
        gdal.GetDataTypeName(pBand.DataType)
        # Compute statistics if needed
        if pBand.GetMinimum() is None or pBand.GetMaximum()is None:
            pBand.ComputeStatistics(0)

        dMissing_value = pBand.GetNoDataValue()
       
        aData_out = pBand.ReadAsArray(0, 0, ncolumn, nrow)
    
        #we will use one of them to keep the consistency
        pSpatialRef = osr.SpatialReference(wkt=pProjection)
        #there are many information in a raster data, we will use some standard way to output them
        #beblow is an example for ArcGIS ASCII file
        #NCOLS xxx
        #NROWS xxx
        #XLLCENTER xxx
        #YLLCENTER xxx
        #CELLSIZE xxx
        #NODATA_VALUE xxx
        #row 1
        #row 2
        #...
        #row n
        #close file

        pDataset = None
        pBand = None
        
        

        return aData_out, dPixelWidth, dOriginX, dOriginY, nrow, ncolumn, dMissing_value,  pSpatialRef, pGeotransform