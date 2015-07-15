#!/in/bash
#cd /home/local/USHERBROOKE/havm2701/data/Synthetic_tumor_project/Synthetic_tumor/PPMI/Subject_3112_2011-06-27_243563_243565/TEST/
#bet tensors.nii bet_tensors.nii -F
#python /home/local/USHERBROOKE/havm2701/git.repos/SyntheticTumor/prepare_brain.py
#
#ANTS 3 -m MI[/home/local/USHERBROOKE/havm2701/data/Synthetic_tumor_project/Synthetic_brain/subject04/subject04_t1w_p4_bet.nii.gz,t1_brain_warp.nii.gz,1,32] -o reg/TEST -i 10x10x0 -r Gauss[1.5,0] -t Exp[0.5]
#WarpImageMultiTransform 3 t1_brain_warp.nii.gz registered_files/T1_std.nii.gz -R reg/TESTWarp.nii reg/TESTAffine.txt
#
#WarpImageMultiTransform 3 temp/0.nii.gz temp/reg_0.nii.gz -R reg/TESTWarp.nii reg/TESTAffine.txt
#WarpImageMultiTransform 3 temp/1.nii.gz temp/reg_1.nii.gz -R reg/TESTWarp.nii reg/TESTAffine.txt
#WarpImageMultiTransform 3 temp/2.nii.gz temp/reg_2.nii.gz -R reg/TESTWarp.nii reg/TESTAffine.txt
#WarpImageMultiTransform 3 temp/3.nii.gz temp/reg_3.nii.gz -R reg/TESTWarp.nii reg/TESTAffine.txt
#WarpImageMultiTransform 3 temp/4.nii.gz temp/reg_4.nii.gz -R reg/TESTWarp.nii reg/TESTAffine.txt
#WarpImageMultiTransform 3 temp/5.nii.gz temp/reg_5.nii.gz -R reg/TESTWarp.nii reg/TESTAffine.txt
#

#cd /data/havm2701/Synthetic_tumor_project/Synthetic_tumor/PPMI/Subject_3112_2011-06-27_243563_243565/TEST/registered_files
#fast -S 1 -t 1 -o test -n 3 T1_std.nii.gz
#mv test_pve_0.nii.gz p-csf.nii.gz
#mv test_pve_1.nii.gz p-gray.nii.gz
#mv test_pve_2.nii.gz p-white.nii.gz
#mv test_seg.nii.gz labels.nii.gz

#python /home/local/USHERBROOKE/havm2701/git.repos/SyntheticTumor/testconvert.py
#prepare_tensor file
#python /home/local/USHERBROOKE/havm2701/git.repos/SyntheticTumor/align_tensor.py
python /home/local/USHERBROOKE/havm2701/git.repos/SyntheticTumor/testconvert.py