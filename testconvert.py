from convertformats import save_file_mask
from convertformats import save_file_label

from os.path import join #import pdb
#pdb.set_trace()
#path = '/home/local/USHERBROOKE/havm2701/data/Synthetic_tumor_project/Synthetic_tumor/PPMI/Subject_3112_2011-06-27_243563_243565/TEST/temp'
path = '/data/havm2701/Synthetic_tumor_project/Synthetic_tumor/PPMI/Subject_3112_2011-06-27_243563_243565/TEST/4SEG'
#save_file_mask(join(path,'p-csf.nii.gz'),join(path,'p-csf.mha'))
#save_file_mask(join(path,'p-gray.nii.gz'),join(path,'p-gray.mha'))
#save_file_mask(join(path,'p-white.nii.gz'),join(path,'p-white.mha'))
save_file_label(join(path,'labels.nii.gz'),join(path,'labels.mha'))

#save_file_mask('Alighned_input/p_white.nii','Alighned_input/p_white.mha')
#save_file_mask('Alighned_input/p_gray.nii','Alighned_input/p_gray.mha')
#save_file_mask('Alighned_input/p_csf.nii','Alighned_input/p_csf.mha')

#save_file_mask('Alighned_input/p_vessel.mha','Alighned_input/p_vessel2.mha')
#path = '/data/havm2701/Synthetic_tumor_project/Synthetic_tumor/PPMI/Subject_3112_2011-06-27_243563_243565/TEST'
#save_dti(join(path,'aligned_tensors.nii.gz'),join(path,'tensors.mha'))