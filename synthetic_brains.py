import os
from convertformats import nii2mha_int
from convertformats import nii2mha_label
from convertformats import nii2mha_dti
from convertformats import merge_nii
import shutil
from prepare_brain import isolate_tensors
from os.path import join
from os import listdir
from os.path import isdir
from os.path import isfile
from ipdb import set_trace


class Brain(object):

    def __init__(self, path):

        #self.brain_path = join(path,name)
        self.path = path
        for f in os.listdir(self.path):
            if 't1' in f and '.nii.gz' in f:
                T1 = f
            if 'tensors.nii' in f:
                dti = f
        self.T1 = T1
        self.dti = dti

    def bet_tensor(self):
        if '.nii.gz' in self.dti:
            print 'tensor image is probably already skull striped ... exiting process'
            pass
        input_name = join(self.path, self.dti)
        output_name = join(self.path, self.dti) + '.gz'
        self.dti = self.dti + '.gz'
        command = 'bet ' + input_name + ' ' + output_name + ' -F'
        os.system(command)

    def _isolate_tensors(self):
        return isolate_tensors(self.path, self.dti)

    def align_brain(self, ref_path):
        def warpImage(input_path, output_path):
            command = 'WarpImageMultiTransform 3 ' + input_path + ' ' + output_path + ' -R ' + join(self.path, 'reg', 'TESTWarp.nii') + ' ' + join(self.path, 'reg', 'TESTAffine.txt')
            os.system(command)

        if not os.path.isdir(join(self.path, 'reg')):
            os.mkdir(join(self.path, 'reg'))
        dti_temp_dir = self._isolate_tensors()

        command = 'ANTS 3 -m MI[' + ref_path + ',' + join(self.path, self.T1) + ',1,32] -o ' + join(self.path, 'reg', 'TEST') + ' -i 10x10x0 -r Gauss[1.5,0] -t Exp[0.5]'
        os.system(command)
        dir_list = [f for f in os.listdir(dti_temp_dir) if 'reg_' not in f]
        for f in dir_list:
            input_path = join(dti_temp_dir, f)
            output_path = join(dti_temp_dir, 'reg_' + f)
            warpImage(input_path, output_path)

        self.__reformat(dti_temp_dir, join(self.path, 'dti.mha'))

        self.registered_dir = join(self.path, 'Aligned')
        if not os.path.isdir(self.registered_dir):
            os.mkdir(self.registered_dir)
        warpImage(join(self.path, self.T1), join(self.path, self.registered_dir, self.T1))

    def extract_brain_components(self):
        brain_components_path = join(self.path, 'brain_components')
        if not os.path.isdir(brain_components_path):
            os.mkdir(brain_components_path)
        if not os.path.isdir(join(brain_components_path, 'label_temp')):
            os.mkdir(join(brain_components_path, 'label_temp'))

        command = 'fast -S 1 -t 1 -o ' + join(brain_components_path, 'maps') + ' -n 3 ' + join(self.path, self.registered_dir, self.T1)
        command_label_4seg = 'fast -S 1 -t 1 -o ' + join(brain_components_path, 'label_temp/maps') + ' -n 4 ' + join(self.path, self.registered_dir, self.T1)

        os.system(command)
        os.system(command_label_4seg)
        maps_list = [f for f in os.listdir(brain_components_path) if 'maps' in f]
        #assert len(maps_list) == 6
        self.__reformat(join(brain_components_path, 'maps_pve_0.nii.gz'), join(brain_components_path, 'p_csf.mha'))
        self.__reformat(join(brain_components_path, 'maps_pve_1.nii.gz'), join(brain_components_path, 'p_gray.mha'))
        self.__reformat(join(brain_components_path, 'maps_pve_2.nii.gz'), join(brain_components_path, 'p_white.mha'))
        self.__reformat(join(brain_components_path, 'label_temp/maps_seg.nii.gz'), join(brain_components_path, 'labels.mha'))

        self.brain_components_path = brain_components_path

    def __reformat(self, name1, name2):
        import os
        if 'maps_seg.nii.gz' in name1:
            nii2mha = nii2mha_label
            rename = os.rename
        elif 'dti' in name2:
            nii2mha = nii2mha_dti
            rename = merge_nii
        else:
            nii2mha = nii2mha_int
            rename = os.rename
        temp_name = name2.replace('.mha', '.nii.gz')
        rename(name1, temp_name)
        nii2mha(temp_name, name2)

    def create_TumorSim_input(self, input_path):
        import shutil
        import os
        orig_path = '/data/havm2701/Synthetic_tumor_project/Synthetic_tumor/Final_tumorsim/TumorSimInput'
        shutil.copyfile(join(orig_path, 'mesh.vtk'), join(input_path, 'mesh.vtk'))
        shutil.copyfile(join(orig_path, 'p_vessel.mha'), join(input_path, 'p_vessel.mha'))
        shutil.copytree(join(orig_path, 'textures'), join(input_path, 'textures'))
        os.rename(join(self.brain_components_path, 'p_csf.mha'), join(input_path, 'p_csf.mha'))
        os.rename(join(self.brain_components_path, 'p_gray.mha'), join(input_path, 'p_gray.mha'))
        os.rename(join(self.brain_components_path, 'p_white.mha'), join(input_path, 'p_white.mha'))
        os.rename(join(self.brain_components_path, 'labels.mha'), join(input_path, 'labels.mha'))
        os.rename(join(self.path, 'dti.mha'), join(input_path, 'dti.mha'))

    def cleanup(self):
        listing = [f for f in listdir(self.path) if f not in ['input', 'tensors.nii', 't1.nii.gz']]
        for f in listing:
            if isdir(join(self.path, f)):
                shutil.rmtree(join(self.path, f))
            elif isfile(join(self.path, f)):
                os.remove(join(self.path, f))

        print 'Temporary files deleted'
