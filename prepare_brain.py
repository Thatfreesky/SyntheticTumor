from os.path import join 
from os.path import isdir
import os
import numpy as np
from nibabel.testing import data_path



def isolate_tensors(path,dti_path):
	dti_file = join(path, dti_path)
	#t1_file = join(path,t1_path)
	import nibabel as nib

	#load t1 image
	#img_t1 = nib.load(t1_file)
	#img_affine1 = img_t1.get_affine()
	#t1 = img_t1.get_data()
	#print t1.shape


	#load dti image
	img_dti = nib.load(dti_file)
	img_affine2 = img_dti.get_affine()
	dti = img_dti.get_data()

	# check if modalitis are alighned
	#if img_affine1 != img_affine2:
	#	print 'modalities are not alighned'

	#img_mask = t1>0.001

	
	num_tensors = dti.shape[-1]
	temp_dir = join(path,'temp')
	if not isdir(temp_dir):
		os.mkdir(temp_dir)
	for i in range(num_tensors):
		tensor_path = join(temp_dir,str(i)+'.nii.gz')
		bi = dti[:,:,:,i]
		#bi = bi*img_mask
		array_img = nib.Nifti1Image(bi, img_affine2)
		array_img.to_filename(tensor_path)

	return temp_dir	


