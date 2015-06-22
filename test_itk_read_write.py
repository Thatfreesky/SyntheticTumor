import itk
import numpy
import numpy as np
import argparse

def save_file_mask (data_filepath, prediction_array, output_filepath):
    

    image_type = itk.Image[itk.SS, 3]
    itk_py_converter = itk.PyBuffer[image_type]
    reader = itk.ImageFileReader[image_type].New()

    reader.SetFileName(data_filepath)
    reader.Update()
    out = reader.GetOutput()

    writer = itk.ImageFileWriter[image_type].New()
    writer.SetFileName(output_filepath)

    itk_image = itk_py_converter.GetImageFromArray(prediction_array.tolist() )
    itk_image.SetSpacing(out.GetSpacing())
    itk_image.SetOrigin(out.GetOrigin())

    writer.SetInput(itk_image.GetPointer())
    writer.UseCompressionOn()
    writer.Update()



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Create mha mask to be used as seed by TumorSim')
    parser.add_argument('data_filepath', type=str,#argparse.FileType('r'),
                        help='path to the reference mha file')
    parser.add_argument('output_filepath', type=str,
                        help='path to save the seed mha file')
  
    args = parser.parse_args()

    data_filepath = args.data_filepath
    output_filepath = args.output_filepath
    #data_filepath = '/home/local/USHERBROOKE/havm2701/data/Synthetic_tumor_project/Synthetic_tumor/Final_tumorsim/Output00T/SimTumor00T_FLAIR.mha'
    output_filepath = 'test3.mha'
    D=np.zeros((181, 256, 256))
    center = (100,100,100)
    radius=5
    x,y,z = np.ogrid[:D.shape[0],:D.shape[1],:D.shape[2]]
    mask = (x-center[0])**2 + (y-center[1])**2 +(z-center[2])**2 <= radius*radius
    D[mask]=1

    D = numpy.array(D, dtype=numpy.short)
    #D[50:70,30:20,40:80]=500
    save_file_mask (data_filepath, D, output_filepath)
