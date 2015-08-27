from os.path import join
from os import listdir
from os import mkdir
from os.path import isdir
from synthetic_brains import Brain
from ipdb import set_trace

ref_path = '/home/local/USHERBROOKE/havm2701/data/Synthetic_tumor_project/Synthetic_brain/subject04/subject04_t1w_p4_bet.nii.gz'
path = '/home/local/USHERBROOKE/havm2701/data/PPMI'
path_save = '/home/local/USHERBROOKE/havm2701/data/PPMI_processed'

subject_list = listdir(path)

for f in subject_list:
    for g in listdir(join(path, f)):
        if 'input' in g:
            continue
    subject = Brain(join(path, f))
    subject.bet_tensor()
    subject.align_brain(ref_path)
    subject.extract_brain_components()
    if not isdir(join(path_save, f)):
        mkdir(join(path_save, f))
    if not isdir(join(path_save, f, 'input')):
        mkdir(join(path_save, f, 'input'))
    subject.create_TumorSim_input(join(path_save, f, 'input'))
    subject.cleanup()
    del subject
