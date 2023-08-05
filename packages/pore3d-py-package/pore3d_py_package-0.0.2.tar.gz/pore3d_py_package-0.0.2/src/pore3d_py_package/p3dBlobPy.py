import p3dBlob
from p3dBlob import *


################## constants
P3D_FALSE=-1 
P3D_TRUE=1 

P3D_ERROR=0
P3D_MEM_ERROR=None
P3D_SUCCESS=2

BACKGROUND=0
#OBJECT=UCHAR_MAX

CONN4=611
CONN8=612

CONN6=711
CONN18=712
CONN26=713

################## error messages

def py_printErrorMessage(err_code):
  
    string = "Success. \n"
  
    if err_code == 1 or err_code == 0:
        string = "Error on code execution. \n"
        return
  	
    if err_code == -2:
        string = "Input argument IMAGE must be of type BYTE or UINT. \n"
        return
  	
    if err_code == -3:
        string = "Input argument IMAGE must be a 2D or 3D matrix. \n"
        return
   	
    if err_code == 2:
        print (string)

#################
  
#Basic analysis
def py_p3dBasicAnalysis(image_data, dimx,dimy,dimz, resolution = 1.0):
    out_BasicStats = BasicStats()
    err_code = p3dBasicAnalysis(image_data,out_BasicStats,dimx,dimy,dimz, resolution, None)
    py_printErrorMessage(err_code)
    return out_BasicStats

#Anisotrtopy analysis
def py_p3dAnisotropyAnalysis(image_data, dimx,dimy,dimz, resolution = 1.0, details = False):
    out_AnisotropyStats = AnisotropyStats()
    im_dummy_mask = malloc_uchar(dimx*dimy*dimz)
    im_dummy_mask = image_data
    err_code = p3dAnisotropyAnalysis(image_data, None, out_AnisotropyStats, dimx,dimy,dimz,resolution,details , None)
    py_printErrorMessage(err_code)
    return out_AnisotropyStats

#Blob labeling
def py_p3dBlobLabeling_8(image_data, dimx,dimy,dimz, conn3D = CONN6 , rand = 0, skip_borders = 0):
    out_image = malloc_ushort(dimx*dimy*dimz)
    err_code = p3dBlobLabeling_uint(image_data, out_image, dimx,dimy,dimz,conn3D,rand , skip_borders, None)
    py_printErrorMessage(err_code)
    return out_image

#Blob Get max
def py_p3dGetMaxVolumeBlob3D(image_data, dimx,dimy,dimz, conn3D = CONN6):
    out_image = malloc_uchar(dimx*dimy*dimz)
    err_code = p3dGetMaxVolumeBlob3D(image_data, out_image, dimx,dimy,dimz,conn3D, None)
    py_printErrorMessage(err_code)
    return out_image

#Blob Get min
def py_p3dGetMinVolumeBlob3D(image_data, dimx,dimy,dimz, conn3D = CONN6):
    out_image = malloc_uchar(dimx*dimy*dimz)
    err_code = p3dGetMinVolumeBlob3D(image_data, out_image, dimx,dimy,dimz,conn3D, None)
    py_printErrorMessage(err_code)
    return out_image

#ChamferDT
def py_p3dChamferDT(image_data, dimx,dimy,dimz, w1 = 3, w2 = 4, w3 = 5):
    out_image = malloc_ushort(dimx*dimy*dimz)
    err_code = p3dChamferDT(image_data, out_image, dimx,dimy,dimz,w1, w2, w3, None)
    py_printErrorMessage(err_code)
    return out_image

#SquaredEuclideanDT
def py_p3dSquaredEuclideanDT(image_data, dimx,dimy,dimz):
    out_image = malloc_uchar(dimx*dimy*dimz)
    err_code = p3dSquaredEuclideanDT(image_data, out_image, dimx,dimy,dimz, None)
    py_printErrorMessage(err_code)
    return out_image

# MinVolumeFilter
def py_p3dMinVolumeFilter3D(image_data, dimx,dimy,dimz,min_vol = 5):
    out_image = malloc_uchar(dimx*dimy*dimz)
    err_code = p3dMinVolumeFilter3D(image_data, out_image, dimx,dimy,dimz, min_vol, None)
    py_printErrorMessage(err_code)
    return out_image

# Morphometric Analysis
def py_p3dMorphometricAnalysis(image_data, mask_image, dimx,dimy,dimz,resolution = 1.0):
    out_MorphometricStat = MorphometricStats()
    mask_image = malloc_uchar(dimx*dimy*dimz)
    err_code = p3dMorphometricAnalysis(image_data, mask_image, out_MorphometricStat, dimx,dimy,dimz, resolution, None)
    py_printErrorMessage(err_code)
    return out_MorphometricStat

# Texture Analysis
def py_p3dTextureAnalysis(image_data, dimx,dimy,dimz):
    out_TextureStat = TextureStats()
    err_code = p3dTextureAnalysis(image_data, out_MorphometricStat, dimx,dimy,dimz, None)
    py_printErrorMessage(err_code)
    return out_TextureStat

# Blob Analysis
def py_p3dBlobAnalysis(image_data,dimx,dimy,dimz, blob_im = None, star_im = None, resolution = 1.0, conn = 6, max_rot = 1024, skip_borders = 0):
    out_BlobStat = BlobStats()
    if conn == 6 :
        conn = CONN6;
    if conn == 18 :
        conn = CONN18;
    if conn == 26 :
        conn = CONN26;
        
    if skip_borders == 0 :
        borders = P3D_FALSE;
    else :
        borders = P3D_TRUE;
        
    err_code = p3dBlobAnalysis(image_data, out_BlobStat, blob_im, star_im, dimx,dimy,dimz,resolution,conn,max_rot,borders, None)
    py_printErrorMessage(err_code)
    return out_BlobStat

#IDL_VPTR p3d_idlREVEstimation(int, IDL_VPTR*, char* );
#IDL_VPTR p3d_idlBlobAnalysis(int, IDL_VPTR*, char* );
