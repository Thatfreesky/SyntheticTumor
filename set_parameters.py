from seed_utils import generate_seed_file
from os.path import join
from random import randrange
from random import uniform
from random import shuffle
from random import random
import os
from os.path import isdir
from os import mkdir
from os import listdir


class PerBrain(object):

    def __init__(self, input_directory, brain_name):
        self.input_directory = input_directory
        self.brain_name = brain_name


class WithinBrain(PerBrain):

    def __init__(self, input_directory, brain_name, output_directory, identifier):
        super(WithinBrain, self).__init__(input_directory, brain_name)
        output_directory = join(output_directory, identifier)
        self.output_directory = output_directory
        self.seed_path = join(output_directory, 'seed.mha')
        self.identifier = identifier
        if not isdir(output_directory):
            mkdir(output_directory)

    def generate_seed(self,):
        #data_filepath = join(self.input_directory, 'labels.mha')
        #mask_path = join(self.input_directory, 'labels.mha')
        data_filepath = join(result_path, 'SimTumor00T_T1.mha')
        mask_path = join(result_path, 't1.nii.gz')
        generate_seed_file(data_filepath, self.seed_path, mask_path)

    def image_parameters(self,):
        pass

    def tumor_parameters(self,):
        # deformation parameters
        self.deformation_iterations = randrange(5, 50)
        self.deformation_initial_pressure = uniform(0.5, 8)  # control over necrosis
        self.deformation_kappa = uniform(10, 50)
        # infiltration parameters
        self.infiltration_iterations = randrange(5, 10)
        self.infiltration_body_force_iterations = randrange(5, 15)
        self.infiltration_body_force_coefficient = 7.5 + (7 * (random() - 0.5))
        self.infiltration_early_time = uniform(0.05, 5)
        self.infiltration_time_step = uniform(0.05, 5)
        # tumor type
        dist_tumor_type = ['ring', 'ring', 'none', 'uniform']  # ring type tumor has double the chance to get selected
        shuffle(dist_tumor_type)
        self.tumor_type = dist_tumor_type[0]

    @property
    def generate_tumor_parameters(self,):
        D = {}
        D['input-directory'] = self.input_directory
        D['output-directory'] = self.output_directory
        D['seed-path'] = self.seed_path
        D['identifier'] = self.brain_name + '_' + self.identifier
        D['deformation-iterations'] = self.deformation_iterations
        D['deformation-initial-pressure'] = self.deformation_initial_pressure
        D['deformation-kappa'] = self.deformation_kappa
        D['infiltration-iterations'] = self.infiltration_iterations
        D['infiltration-time-step'] = self.infiltration_time_step
        D['infiltration-early-time'] = self.infiltration_early_time
        D['infiltration-body-force-iterations'] = self.infiltration_body_force_iterations
        D['infiltration-body-force-coefficient'] = self.infiltration_body_force_coefficient
        D['tumor-type'] = self.tumor_type
        return D

    def initiate(self, params):

        self.xml_path = join(self.output_directory, 'TumorSim_params.xml')
        xmlfile_path = join(os.path.dirname(os.path.realpath(__file__)), 'SimTumor_configuration_template.xml')
        xml_empty = open(xmlfile_path).read()
        xml = xml_empty % params
        with open(self.xml_path, 'w') as File_xml_write:
            File_xml_write.write(xml)


def cleanup(path):
    keep_tags = ['T1Gad.mha', 'T2.mha', 'T1.mha', 'T1Gad', 'T1Gad', 'T1Gad', '.xml', '.log', 'truth.mha', 'FLAIR.mha', 'seed.mha']
    keep_files = []
    import ipdb

    for quary_file in listdir(path):
        flag = False
        for tag in keep_tags:
            if tag in quary_file:
                flag = True

        if flag is True:
            keep_files.append(quary_file)

    ipdb.set_trace()
    for r_file in listdir(path):
        if r_file not in keep_files:
            os.remove(join(path, r_file))

if __name__ == "__main__":
    id_u = 'test'
    HOME = os.environ['HOME']
    brains_directory = join(HOME, 'data/PPMI_processed')
    brain_names = listdir(brains_directory)
    result_path = join(HOME, 'data/Synthetic_tumor_project/Synthetic_tumor/EXPERIMENTS')

    len_brain_names = len(brain_names)
    brain_names = brain_names[:len_brain_names / 2]

    for brain_name in brain_names:
        input_directory = join(brains_directory, brain_name, 'input')
        output_directory = join(result_path, brain_name)
        if not isdir(output_directory):
            mkdir(output_directory)
        #brain_name = 'blabla'

        # D.generate_seed()

        for i in range(10):
            id_u = str(i)
            DD = WithinBrain(input_directory, brain_name, output_directory, id_u)
            DD.generate_seed()
            DD.tumor_parameters()
            DD.initiate(DD.generate_tumor_parameters)
            command = 'taskset 01 tumorsim ' + DD.xml_path
            os.system(command)
            del DD
            cleanup(join(output_directory, id_u))
