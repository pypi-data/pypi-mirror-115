import p3dFilt as p3dFilt
from p3dFilt import *

################## 

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


################## Handle 8 bit 

#read
def py_p3dReadRaw8(filename, dimx,dimy,dimz):
	"""
    This function reads a RAW image in 8-bit format from the specified file.
 
 Syntax:
 ------
 Result = py_p3dReadRaw8 ( FileName, dimx, dimy, dimz)
 
 Return Value:
 ------------
 Returns a matrix of type BYTE with the dimensions specified in input representing the image read from disk.
 
 Arguments:
 ---------
 Filename: A string with the filename with full path included.
 dimx,dimy,dimz: three variables representing the dimensions of image to read. 
 
 Remarks:
 -------
 Trying to read a RAW image stored in SIGNED format is in principle an error. 
 Also, #using p3dReadRaw8 for a 16-bit RAW image results in a completely wrong output but, again, no error could be detected.
 Attention #must be paid when using this function. Pore3D internally deals only with UNSIGNED format.
	"""
	image_data = malloc_uchar(dimx*dimy*dimz)
	err_code = p3dReadRaw8(filename, image_data,dimx,dimy,dimz, None, None);
	py_printErrorMessage(err_code)
	return image_data

#write
def py_p3dWriteRaw8(image_data, filename, dimx,dimy,dimz):
	#image_data = p3dFilt.malloc_uchar(dimx*dimy*dimz)
	err_code = p3dWriteRaw8(image_data, filename,dimx,dimy,dimz, None, None);
	py_printErrorMessage(err_code)
	return image_data

#Gaussian Filter	
def py_p3dGaussianFilter8(image_data, dimx,dimy,dimz, width =3 ,sigma = 1.0):
	out_image = p3dFilt.malloc_uchar(dimx*dimy*dimz)
	err_code = p3dGaussianFilter3D_8(image_data,out_image,dimx,dimy,dimz, 3,1.0, None, None)
	py_printErrorMessage(err_code)
	return out_image			

# Mean Filter
def py_p3dMeanFilter8(image_data, dimx,dimy,dimz, width =3):
	out_image = p3dFilt.malloc_uchar(dimx*dimy*dimz)
	err_code = p3dMeanFilter3D_8(image_data,out_image, dimx,dimy,dimz, width,None, None)				
	py_printErrorMessage(err_code)
	return out_image
	
# Median Filter
def py_p3dMedianFilter8(image_data, dimx,dimy,dimz, width=3):
	out_image = p3dFilt.malloc_uchar(dimx*dimy*dimz)
	err_code = p3dMedianFilter3D_8(image_data,out_image, dimx,dimy,dimz, width,None, None)				
	py_printErrorMessage(err_code)
	return out_image

# AnisotropicDiffusionFilter
def py_p3dAnisotropicDiffusionFilter8(image_data, dimx,dimy,dimz,m = 1,lambdaP = 0.01,sigma = 0.01,iterP = 20):
	out_image = p3dFilt.malloc_uchar(dimx*dimy*dimz)
	err_code = p3dAnisotropicDiffusionFilter3D_8(image_data,out_image, dimx,dimy,dimz,m,lambdaP,sigma,iterP,None, None)				
	py_printErrorMessage(err_code)
	return out_image

# BilateralFilter
def py_p3dBilateralFilter8(image_data, dimx,dimy,dimz,size,sigma_d,sigma_r,iter):
	out_image = p3dFilt.malloc_uchar(dimx*dimy*dimz)
	err_code = p3dBilateralFilter3D_8(image_data,out_image, dimx,dimy,dimz,size,sigma_d,sigma_r,iter,None, None)				
	py_printErrorMessage(err_code)
	return out_image
	
# BoinHaibelRingRemover 2D only
def py_p3dBoinHaibelRingRemover8(image_data, dimx,dimy,centerX,centerY,winsize,iterations, precision):
	out_image = p3dFilt.malloc_uchar(dimx*dimy)
	err_code = p3dBoinHaibelRingRemover2D_8(image_data,out_image, dimx,dimy,centerX,centerY,winsize,iterations, precision,None)
	py_printErrorMessage(err_code)
	return out_image

# SijbersPostnovRingRemover 2D only 
def py_p3dSijbersPostnovRingRemover8(image_data, dimx,dimy,centerX,centerY,winsize,thresh,iterations, precision):
	out_image = p3dFilt.malloc_uchar(dimx*dimy)
	err_code = p3dSijbersPostnovRingRemover2D_8(image_data,out_image, dimx,dimy,centerX,centerY,winsize,thresh,iterations, precision,None, None,None)				
	py_printErrorMessage(err_code)
	return out_image

# ClearBorderFilter
def py_p3dClearBorderFilter8(image_data, dimx,dimy,dimz,connIn = 6):
	out_image = p3dFilt.malloc_uchar(dimx*dimy)
	conn3D = 711
	if connIn == 6:
		conn3D = 711
	if connIn == 18:
		conn3D = 712
	if connIn == 26:
		conn3D = 713			
	err_code = p3dClearBorderFilter3D(image_data,out_image, dimx,dimy,dimz,conn3D,None)
	py_printErrorMessage(err_code)
	return out_image
	
# AutoThresholding
def py_p3dAutoThresholding8(image_data, dimx,dimy,dimz,methodNum):
	out_image = p3dFilt.malloc_uchar(dimx*dimy*dimz)
	thresh_val = p3dFilt.malloc_uchar(1)
	if methodNum == 1:
		err_code = p3dKittlerThresholding_8(image_data, out_image,dimx,dimy,dimz, thresh_val, None, None)
	elif methodNum == 2:
		err_code = p3dOtsuThresholding_8(image_data, out_image,dimx,dimy,dimz,thresh_val, None, None)	
	elif methodNum == 3:
		err_code = p3dPunThresholding_8(image_data, out_image,dimx,dimy,dimz,thresh_val, None, None)
	elif methodNum == 4:
		err_code = p3dRidlerThresholding_8(image_data, out_image,dimx,dimy,dimz,thresh_val, None, None)
	elif methodNum == 5:
		err_code = p3dKapurThresholding_8(image_data, out_image,dimx,dimy,dimz,thresh_val, None, None)
	elif methodNum == 6:
		err_code = p3dJohannsenThresholding_8(image_data, out_image,dimx,dimy,dimz,thresh_val, None, None)
	elif methodNum == 7:
		err_code = p3dHuangYagerThresholding_8(image_data, out_image,dimx,dimy,dimz,thresh_val, None, None)
	else:
		err_code = p3dOtsuThresholding_8(image_data, out_image,dimx,dimy,dimz, thresh_val, None, None)
	
	py_printErrorMessage(err_code)
	return out_image
		
		
#From16To8
def py_p3dFrom16To8(image_data16, dimx,dimy,dimz):
    out_image8 = p3dFilt.malloc_uchar(dimx*dimy*dimz)
    err_code = p3dFrom16To8(image_data16,out_image8,dimx,dimy,dimz,0,255,None,None)
    py_printErrorMessage(err_code)
    return out_image8
        
# CreateBinaryCircle

# CreateBinaryCylinder

# CreateBinarySphere

# GetRegionByCoords



################## Handle 16 bit

#read
def py_p3dReadRaw16(filename, dimx,dimy,dimz, little_endian = 0, is_signed = 0):
	image_data = p3dFilt.malloc_ushort(dimx*dimy*dimz)
	err_code = p3dReadRaw16(filename, image_data,dimx,dimy,dimz,little_endian, is_signed, None, None);
	py_printErrorMessage(err_code)
	return image_data

#write
def py_p3dWriteRaw16(image_data, filename, dimx,dimy,dimz, little_endian = 0, is_signed = 0):
	#image_data = p3dFilt.malloc_uchar(dimx*dimy*dimz)
	err_code = p3dWriteRaw16(image_data, filename,dimx,dimy,dimz,little_endian, is_signed, None, None);
	py_printErrorMessage(err_code)
	return image_data

def py_p3dAutoThresholding16(image_data, dimx,dimy,dimz,methodNum):
	out_image = p3dFilt.malloc_ushort(dimx*dimy*dimz)
	thresh_val = p3dFilt.malloc_ushort(1)
	if methodNum == 1:
		err_code = p3dKittlerThresholding_16(image_data, out_image,dimx,dimy,dimz, thresh_val, None, None)
	elif methodNum == 2:
		err_code = p3dOtsuThresholding_16(image_data, out_image,dimx,dimy,dimz,thresh_val, None, None)	
	elif methodNum == 3:
		err_code = p3dPunThresholding_16(image_data, out_image,dimx,dimy,dimz,thresh_val, None, None)
	elif methodNum == 4:
		err_code = p3dRidlerThresholding_16(image_data, out_image,dimx,dimy,dimz,thresh_val, None, None)
	elif methodNum == 5:
		err_code = p3dKapurThresholding_16(image_data, out_image,dimx,dimy,dimz,thresh_val, None, None)
	elif methodNum == 6:
		err_code = p3dJohannsenThresholding_16(image_data, out_image,dimx,dimy,dimz,thresh_val, None, None)
	elif methodNum == 7:
		err_code = p3dHuangYagerThresholding_16(image_data, out_image,dimx,dimy,dimz,thresh_val, None, None)
	else:
		err_code = p3dOtsuThresholding_16(image_data, out_image,dimx,dimy,dimz, thresh_val, None, None)
	
	py_printErrorMessage(err_code)
	return out_image

#void p3d_idlWriteRaw(int, IDL_VPTR*, char* );
#IDL_VPTR p3d_idlGaussianFilter(int, IDL_VPTR*, char* );
#IDL_VPTR p3d_idlMeanFilter(int, IDL_VPTR*, char* );
#IDL_VPTR p3d_idlMedianFilter(int, IDL_VPTR*, char* );
#IDL_VPTR p3d_idlAnisotropicDiffusionFilter(int, IDL_VPTR*, char*);
#IDL_VPTR p3d_idlBilateralFilter(int, IDL_VPTR*, char* );
#IDL_VPTR p3d_idlBoinHaibelRingRemover(int, IDL_VPTR*, char* );
#IDL_VPTR p3d_idlSijbersPostnovRingRemover(int, IDL_VPTR*, char* );
#IDL_VPTR p3d_idlClearBorderFilter(int, IDL_VPTR*, char* );
#IDL_VPTR p3d_idlCreateBinaryCircle(int, IDL_VPTR*, char* );
#IDL_VPTR p3d_idlCreateBinaryCylinder(int, IDL_VPTR*, char* );
#IDL_VPTR p3d_idlCreateBinarySphere(int, IDL_VPTR*, char* );
#IDL_VPTR p3d_idlGetRegionByCoords(int, IDL_VPTR*, char* );
#IDL_VPTR p3d_idlAutoThresholding(int, IDL_VPTR*, char* );
#IDL_VPTR p3d_idlFrom16To8(int, IDL_VPTR*, char* );
  
  
