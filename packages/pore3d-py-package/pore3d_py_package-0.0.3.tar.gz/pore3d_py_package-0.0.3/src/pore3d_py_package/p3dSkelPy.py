import p3dSkel
from p3dSkel import *

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
def py_p3dSkeletonLabeling(image_data, dimx,dimy,dimz):
    out_image = malloc_uchar(dimx*dimy*dimz)
    err_code = p3dSkeletonLabeling(image_data,out_image,dimx,dimy,dimz, None)
    py_printErrorMessage(err_code)
    return out_image
   
def py_p3dGVFSkeletonization(image_data, dimx,dimy,dimz,mu= 0.15,eps= 1E-4,hierarc = 1.0,scale= 0.0):
    out_image = malloc_uchar(dimx*dimy*dimz)
    err_code = p3dGVFSkeletonization(image_data,out_image,dimx,dimy,dimz, mu,ep,hierarc,scale, None)
    py_printErrorMessage(err_code)
    return out_image

def py_p3dLKCSkeletonization(image_data, dimx,dimy,dimz):
    out_image = P3D_Skel_Py.p3dSkel.malloc_uchar(dimx*dimy*dimz)
    err_code = p3dLKCSkeletonization(image_data,out_image,dimx,dimy,dimz, None)
    py_printErrorMessage(err_code)
    return out_image

def py_p3d_p3dThinningSkeletonization(image_data, dimx,dimy,dimz):
    out_image = malloc_uchar(dimx*dimy*dimz)
    err_code = p3dThinningSkeletonization(image_data,out_image,dimx,dimy,dimz, None)
    py_printErrorMessage(err_code)
    return out_image

def py_p3dSkeletonAnalysis(image_data,skeleton_image,skeleton_stats,dimx,dimy,dimz,nodes_im = None, pores_im= None,ends_im= None,throats_im= None,merging_factor= 0.85, tortuosity_depth= 3, resolution= 1.0):
    out_image = malloc_uchar(dimx*dimy*dimz)
    err_code=p3dSkeletonAnalysis(image_data,skeleton_image,skeleton_stats,nodes_im,pores_im,ends_im,throats_im,dimx,dimy,dimz,merging_factor,tortuosity_depth, resolution,None)
    py_printErrorMessage(err_code)
    return out_image

    
def py_p3dSkeletonPruning(image_data,dimx,dimy,dimz,thresh=3,ultimate = False,iterative = False):
    out_image = malloc_uchar(dimx*dimy*dimz)
    if iterative == True and ultimate == False:
        print("p3dIterativeSkeletonPruning")
        err_code = p3dIterativeSkeletonPruning (image_data, out_image,dimx,dimy,dimz, thresh, None )
        py_printErrorMessage(err_code)
        return out_image
    if ultimate == True:
        print("p3dUltimateSkeletonPruning")
        err_code =  p3dUltimateSkeletonPruning (image_data, out_image, dimx,dimy,dimz, iterative, None )
        py_printErrorMessage(err_code)
        return out_image
    # Default: iterative == False and ultimate = False
    print("p3dSimpleSkeletonPruning")
    err_code = p3dSimpleSkeletonPruning(image_data, out_image,dimx,dimy,dimz, thresh, None )
    py_printErrorMessage(err_code)
    return out_image
    

#IDL_VPTR p3d_idlSkeletonAnalysisFeasibility (int, IDL_VPTR*, char* );

	


################## Handle 16 bit
				
#IDL_VPTR p3d_idlPKSkeletonization(int, IDL_VPTR*, char* );
#IDL_VPTR p3d_idlSkeletonAnalysisFeasibility (int, IDL_VPTR*, char* );

  
  
