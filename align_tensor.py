from os.path import join 
from os.path import isdir
import os
import numpy as np
from nibabel.testing import data_path
path = '/home/local/USHERBROOKE/havm2701/data/Synthetic_tumor_project/Synthetic_tumor/PPMI/Subject_3112_2011-06-27_243563_243565/TEST/'
path_read = join(path,'temp')
dir_list = [join(path_read,f) for f in os.listdir(path_read) if 'reg_' in f]


dti_path = 'bet_tensors.nii.gz'
t1_path = 't1_brain_warp.nii.gz'

dti_file = join(path, dti_path)
import nibabel as nib

#load t1 image
#img_t1 = nib.load(t1_file)
#img_affine1 = img_t1.get_affine()
#t1 = img_t1.get_data()
#print t1.shape


#load dti image
img_dti = nib.load(dir_list[0])
img_affine = img_dti.get_affine()
dti = img_dti.get_data()
dti_shape = dti.shape
DTI_tensors = np.zeros((dti_shape[0],dti_shape[1],dti_shape[2],6))

for i,path_file in enumerate(dir_list):
    img_buffer = nib.load(path_file)
    data_buffer = img_buffer.get_data()
    DTI_tensors[:,:,:,i] = data_buffer

tensor_path = join(path,'aligned_tensors.nii.gz')    
array_img = nib.Nifti1Image(DTI_tensors, img_affine)
array_img.to_filename(tensor_path)
# check if modalitis are alighned
#if img_affine1 != img_affine2:
#   print 'modalities are not alighned'



