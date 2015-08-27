import itk
import numpy
import numpy as np
from random import randrange
from random import shuffle
import nibabel as nib


def load_mask(mask_path):
    img_buffer = nib.load(mask_path)
    array = img_buffer.get_data()
    array = np.transpose(array, (2, 1, 0))
    return array[:, ::-1, ::-1]


def generate_seed_file(data_filepath, output_filepath, mask_path):

    image_type = itk.Image[itk.SS, 3]
    itk_py_converter = itk.PyBuffer[image_type]
    reader = itk.ImageFileReader[image_type].New()

    reader.SetFileName(data_filepath)
    reader.Update()
    out = reader.GetOutput()
    mask = load_mask(mask_path)
    # check validity of the mask
    mask = mask > 0  # .1 * mask.flatten().max()
    seed = generate_seed_array()
    seed = seed * mask
    while seed.flatten().sum() == 0:
        seed = generate_seed_array()
        seed = seed * mask

    writer = itk.ImageFileWriter[image_type].New()
    writer.SetFileName(output_filepath)

    itk_image = itk_py_converter.GetImageFromArray(seed.tolist())
    itk_image.SetSpacing(out.GetSpacing())
    itk_image.SetOrigin(out.GetOrigin())

    writer.SetInput(itk_image.GetPointer())
    writer.UseCompressionOn()
    writer.Update()


def generate_seed_array():
    # function to generate individual seeds
    def generate_one_seed():
        x_seed = randrange(60, 195, 5)
        y_seed = randrange(36, 213, 5)
        z_seed = randrange(16, 153, 5)
        center = (x_seed, y_seed, z_seed)
        print center
        radius = randrange(3, 12, 2)
        print radius
        x, y, z = np.ogrid[:D.shape[0], :D.shape[1], :D.shape[2]]
        seed = (x - center[0]) ** 2 + (y - center[1]) ** 2 + (z - center[2]) ** 2 <= radius * radius
        return seed

    D = np.zeros((181, 256, 256), dtype=bool)
    number_seeds = [2, 2, 3, 3, 2, 2, 3]
    shuffle(number_seeds)  # shuufle the list and take the first element
    number_seeds = number_seeds[0]
    for i in range(number_seeds):
        seed = generate_one_seed()
        D[seed] = True
    D = numpy.array(D, dtype=numpy.short)
    return D

'''
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Create mha mask to be used as seed by TumorSim')
    parser.add_argument('data_filepath', type=str,  # argparse.FileType('r'),
                        help='path to the reference mha file')
    parser.add_argument('output_filepath', type=str,
                        help='path to save the seed mha file')
    parser.add_argument('mask_path', type=str,
                        help='path to save the seed mha file')
    args = parser.parse_args()

    data_filepath = args.data_filepath
    output_filepath = args.output_filepath
    mask_path = args.mask_path
    #data_filepath = '/home/local/USHERBROOKE/havm2701/data/Synthetic_tumor_project/Synthetic_tumor/Final_tumorsim/Output00T/SimTumor00T_FLAIR.mha'
    output_filepath = 'test3.mha'

    # D[50:70,30:20,40:80]=500
    save_file_mask(data_filepath, output_filepath, mask_path)
'''
