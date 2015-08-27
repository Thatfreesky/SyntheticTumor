from seed_utils import generate_seed_file
from os.path import join
from random import randrange
from random import uniform
from random import shuffle
from random import random
import os
from os.path import isdir
from os import mkdir


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
        data_filepath = '/home/local/USHERBROOKE/havm2701/data/Synthetic_tumor_project/Synthetic_tumor/Final_tumorsim/Output00T/SimTumor00T_T1.mha'
        mask_path = '/home/local/USHERBROOKE/havm2701/data/PPMI_test/3769_2012-01-11_301546_301547/Aligned/t1.nii.gz'
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

        self.xml_path = join('/home/local/USHERBROOKE/havm2701/data/Synthetic_tumor_project/Synthetic_tumor/EXPERIMENTS', self.identifier, 'TumorSim_params.xml')
        xmlfile_path = join(os.path.dirname(os.path.realpath(__file__)), 'SimTumor_configuration_template.xml')
        xml_empty = open(xmlfile_path).read()
        xml = xml_empty % params
        with open(self.xml_path, 'w') as File_xml_write:
            File_xml_write.write(xml)


if __name__ == "__main__":
    id_u = 'test'
    input_directory = '/home/local/USHERBROOKE/havm2701/data/PPMI_processed_example/input'
    output_directory = '/home/local/USHERBROOKE/havm2701/data/Synthetic_tumor_project/Synthetic_tumor/EXPERIMENTS'
    brain_name = 'blabla'

    # D.generate_seed()

    #from ipdb import set_trace
    # set_trace()
    for i in range(10):
        id_u = str(i+10)
        DD = WithinBrain(input_directory, brain_name, output_directory, id_u)
        DD.generate_seed()
        DD.tumor_parameters()
        DD.initiate(DD.generate_tumor_parameters)
        command = 'tumorsim ' + DD.xml_path
        os.system(command)
        del DD
