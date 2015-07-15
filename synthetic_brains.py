import os
from prepare_brain import isolate_tensors

class Brain(object):
	def __init__(self,path,name):

		self.brain_path = join(path,name)
		self.path = path
		for f in os.listdir(path):
			if 'T1' in f and '.nii.gz' in f:
				T1 = f
			if 'tensors.nii' in f:
				dti = f		


	def bet_tensor(self):
		input_name = join(self.path,self.dti)
		output_name = join(self.path,self.dti)+'.gz'
		self.dti = dti + '.gz'
		command = 'bet '+input_name+' '+output_name+' -F'
		os.command()

	def _isolate_tensors(self):
		return isolate_tensors(self.path,self.dti)

	def align_brain(self,ref_path):
		def warpImage(input_path,output_path):
			command = 'WarpImageMultiTransform 3 '+input_path+' '+output_path+' -R reg/TESTWarp.nii reg/TESTAffine.txt'
			os.command()
		dti_temp_dir = self._isolate_tensors()

		command = 'ANTS 3 -m MI['+ref_path+','+self.T1+',1,32] -o reg/TEST -i 10x10x0 -r Gauss[1.5,0] -t Exp[0.5]'
		os.command()
		for f in os.listdir(dti_temp_dir):
			input_path = join(dti_temp_dir,f)
			output_path = join(dti_temp_dir,'reg_'+f)
			warpImage(input_path,output_path)

		self.registered_dir = join(self.path,'Aligned')
		warpImage(join(self.path,self.T1),join(self.path,self.registered_dir,self.T1))	
#WarpImageMultiTransform 3 t1_brain_warp.nii.gz registered_files/T1_std.nii.gz -R reg/TESTWarp.nii reg/TESTAffine.txt
		


