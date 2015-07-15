import itk
import numpy
import numpy as np
import argparse
import pdb
def save_file_mask (data_filepath, output_filepath):
    

    image_type_read = itk.Image[itk.F, 3]
    itk_py_converter_read = itk.PyBuffer[image_type_read]
    reader = itk.ImageFileReader[image_type_read].New()
    #pdb.set_trace()
    reader.SetFileName(data_filepath)
    reader.Update()
    out = reader.GetOutput()
    T1 = itk_py_converter_read.GetArrayFromImage(out)
    T1 = T1[:,::-1,::-1]
    #assert T1.flatten().max == 1
    T1 = (T1/T1.flatten().max())*255
    T1 = np.asarray(T1,dtype=int)
    image_type_write = itk.Image[itk.SS, 3]
    itk_py_converter_write = itk.PyBuffer[image_type_write]
    writer = itk.ImageFileWriter[image_type_write].New()
    writer.SetFileName(output_filepath)

    itk_image = itk_py_converter_write.GetImageFromArray(T1.tolist() )
    itk_image.SetSpacing(out.GetSpacing())
    itk_image.SetOrigin(0)

    writer.SetInput(itk_image.GetPointer())
    writer.UseCompressionOn()
    writer.Update()

def save_file_label (data_filepath, output_filepath):
    

    image_type_read = itk.Image[itk.F, 3]
    itk_py_converter_read = itk.PyBuffer[image_type_read]
    reader = itk.ImageFileReader[image_type_read].New()
    #pdb.set_trace()
    reader.SetFileName(data_filepath)
    reader.Update()
    out = reader.GetOutput()
    T1 = itk_py_converter_read.GetArrayFromImage(out)
    T1 = T1[:,::-1,::-1]
    #assert T1.flatten().max == 1
    #T1 = (T1/T1.flatten().max())*255
    T1 = np.asarray(T1,dtype=int)
    image_type_write = itk.Image[itk.SS, 3]
    itk_py_converter_write = itk.PyBuffer[image_type_write]
    writer = itk.ImageFileWriter[image_type_write].New()
    writer.SetFileName(output_filepath)

    itk_image = itk_py_converter_write.GetImageFromArray(T1.tolist() )
    itk_image.SetSpacing(out.GetSpacing())
    itk_image.SetOrigin(0)

    writer.SetInput(itk_image.GetPointer())
    writer.UseCompressionOn()
    writer.Update()


def save_dti (data_filepath, output_filepath):

    image_type = itk.Image[itk.F, 4]
    itk_py_converter = itk.PyBuffer[image_type]
    reader = itk.ImageFileReader[image_type].New()
    reader.SetFileName(data_filepath)
    reader.Update()
    out = reader.GetOutput()
    T1 = itk_py_converter.GetArrayFromImage(out)

    #Get the header information needs to be 3d
    def get_header(data_filepath):
        image_type = itk.Image[itk.F, 3]
        itk_py_converter = itk.PyBuffer[image_type]
        reader = itk.ImageFileReader[image_type].New()
        reader.SetFileName(data_filepath)
        reader.Update()
        out = reader.GetOutput()
        return (out.GetSpacing(),out.GetOrigin())
    header_info = get_header(data_filepath)

    tensor_array = np.zeros((T1.shape[0]*T1.shape[1],T1.shape[2],T1.shape[3]),dtype=np.float32)
    for id,tensor in enumerate(T1):
        tensor_array[id*T1.shape[1]:(id+1)*T1.shape[1],:,:] = tensor
    tensor_array = tensor_array[:,::-1,::-1]    
    image_type_write = itk.Image[itk.F, 3]
    itk_py_converter_write = itk.PyBuffer[image_type_write]
    writer = itk.ImageFileWriter[image_type_write].New()
    writer.SetFileName(output_filepath)
    itk_image = itk_py_converter_write.GetImageFromArray(tensor_array.tolist() )
    itk_image.SetSpacing(header_info[0])
    itk_image.SetOrigin(0)

    writer.SetInput(itk_image.GetPointer())
    writer.UseCompressionOn()
    writer.Update()
