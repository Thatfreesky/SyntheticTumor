from utils import Brain_mha
from utils import save_mha
import argparse
import itk
from os.path import join as join
from os import listdir as listdir
from os.path import isdir as isdir
from os import mkdir as mkdir


def mask_mha(brain_path, mask_path, save_path):

    #brain_path = '/home/local/USHERBROOKE/havm2701/git.repos/cnn_r/cnn_arc2_nozeropadding/CUDA3_2013DATASET/Tests_Jr/Arc1_test10/arc1_secondpahse_predictions_13_10/BRATS2012/VSD.HG_0116_CH2012.3508.mha'
    dtype = 'int'
    dim = 3
    if 'float' in dtype:
        itk_type = itk.F
    elif 'int' in dtype:
        itk_type = itk.SS

    image_type = itk.Image[itk_type, dim]
    itk_py_converter = itk.PyBuffer[image_type]
    reader = itk.ImageFileReader[image_type].New()
    reader.SetFileName(brain_path)
    reader.Update()
    out = reader.GetOutput()
    image = itk_py_converter.GetArrayFromImage(out)
    spacing = out.GetSpacing()
    origin = out.GetOrigin()
    brain = (image, spacing, origin)

    #mask_path = '/home/local/USHERBROOKE/havm2701/data/RESULTS/within_brain_classification/BRATS_2012_CHALLENGE/fixedMask/challenge_results/6dimensional_F_newmasks/kNN_alpha_0.033_beta_0.0058/boykov/Denoised/VSD.Seg_HG_0116.3508.mha'
    image_type2 = itk.Image[itk_type, dim]
    itk_py_converter2 = itk.PyBuffer[image_type2]
    reader2 = itk.ImageFileReader[image_type2].New()
    reader2.SetFileName(mask_path)
    reader2.Update()
    out2 = reader2.GetOutput()

    image2 = itk_py_converter2.GetArrayFromImage(out2)
    spacing2 = out2.GetSpacing()
    origin2 = out2.GetOrigin()
    #brain = (image2,spacing,origin)
    #mask_brain = Brain_mha('~/data/RESULTS/within_brain_classification/BRATS_2012_CHALLENGE/fixedMask/challenge_results/6dimensional_F_newmasks/kNN_alpha_0.033_beta_0.0058/boykov/Denoised/VSD.Seg_HG_0116.3508.mha')
    #MASK = input_brain2[0]
    MASK = image2
    BRAIN = None
    BRAIN = MASK
    output_brain = (BRAIN, brain[1], brain[2])
    save_mha(output_brain, save_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Create mha mask to be used as seed by TumorSim')
    parser.add_argument('input_path', type=str,  # argparse.FileType('r'),
                        help='path to the input mha file')

    parser.add_argument('mask_path', type=str,
                        help='path to the mask mha file')
    parser.add_argument('uidx', type=str,
                        help='user idx to identify the correct mha files')

    args = parser.parse_args()
    brain_path = args.input_path
    mask_path = args.mask_path
    #brain_list = [f for f in listdir(brain_path) if args.uidx in f and '.mha' in f]
    #mask_list = [f for f in listdir(mask_path) if '.mha' in f]
    '''	
    for brain in brain_list:
        idx = brain.find('.mha')
        str_idx = brain[idx-4:idx]
        for mask in mask_list:
            if str_idx not in mask:
                continue
            if not isdir(join(brain_path,'new')):
                mkdir(join(brain_path,'new'))
    '''
    mask_mha(brain_path, mask_path, brain_path)

    #input_brain = Brain_mha('/home/local/USHERBROOKE/havm2701/git.repos/cnn_r/cnn_arc2_nozeropadding/CUDA3_2013DATASET/Tests_Jr/Arc1_test10/arc1_secondpahse_predictions_13_10/BRATS2012/VSD.HG_0116_CH2012.3508.mha')
    #input_brain2 = Brain_mha('/home/local/USHERBROOKE/havm2701/git.repos/cnn_r/cnn_arc2_nozeropadding/CUDA3_2013DATASET/Tests_Jr/Arc1_test10/arc1_secondpahse_predictions_13_10/BRATS2012/VSD.HG_0116_CH2012.3508.mha')
