# from Scripts.cut import field_cut_tif,get_shp_field
from .Scripts import cut
# from Scripts.water_extract import GF1_wfv,landset8,GF1,band_merge
from .Scripts import water_extract
from .Scripts import down
from .Scripts import transform
import os
import shutil


class CTool():
    def __init__(self) -> None:
        pass
    
    # 获取字段列表
    @classmethod
    def getShpField(cls,shpPath):
        return cut.get_shp_field(shpPath)

    # 裁剪
    @classmethod
    def cutTif(cls,shpPath,tifPath,outDir,fieldName):
        cut.field_cut_tif(shpPath, tifPath, outDir,fieldName)

    # 水体提取
    @classmethod
    def extract(cls,tifDir,samplePath,tempDir,outDir,type):
        if type == "sentinel2" or type == "GF1_wfv":
            if not os.path.exists(tempDir):
                os.mkdir(tempDir)
            else:
                shutil.rmtree(tempDir)
                os.mkdir(tempDir)
            water_extract.GF1_wfv(tifDir,samplePath,tempDir,outDir)

        elif type == "Landset8" :
            classs = os.listdir(tifDir)
            for idx, folder in enumerate(classs):
                ori_landsat = os.path.join(tifDir, folder)
                path1=water_extract.band_merge(ori_landsat, outDir)

                water_extract.landset8(path1, samplePath,  tempDir,outDir)

        elif type == "div_deal":
            if not os.path.exists(tempDir):
                os.mkdir(tempDir)
            else:
                shutil.rmtree(tempDir)
                os.mkdir(tempDir)
            water_extract.GF1(tifDir, samplePath, tempDir,outDir)

        else:
            print("输入参数有误，请退出重新执行")

    # 遥感影像下载
    @classmethod
    def downloadData(cls,shpPath,type,username,password ,start_date,end_date,cloud_max,output_dir):
        # type 暂时只支持landsat8
        down.landsat8_download(shpPath,type,username,password ,start_date,end_date,cloud_max,output_dir)

    # 投影转换
    @classmethod
    def transform(cls,inDir,OutDir):
        transform.prj_change(inDir,OutDir)