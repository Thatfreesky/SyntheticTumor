import itk
import numpy
import numpy as np
import argparse
import ipdb

'''
class Brain_mha(object):
    def __init__(self,path,dim):
        image_type = itk.Image[itk.SS, dim]
        itk_py_converter = itk.PyBuffer[image_type]
        reader = itk.ImageFileReader[image_type].New()

        reader.SetFileName(path)
        reader.Update()
        out = reader.GetOutput()
        ipdb.set_trace()
        self.image = itk_py_converter.GetArrayFromImage(out)
        self.spacing = out.GetSpacing()
        self.origin = out.GetOrigin()
 
'''

def Brain_mha(path,dim=3,dtype='int'):
    if 'float' in dtype:
        itk_type = itk.F
    elif 'int' in dtype:
        itk_type = itk.SS

    image_type = itk.Image[itk_type, dim]
    itk_py_converter = itk.PyBuffer[image_type]
    reader = itk.ImageFileReader[image_type].New()

    reader.SetFileName(path)
    reader.Update()
    out = reader.GetOutput()
  
    image = itk_py_converter.GetArrayFromImage(out)
    spacing = out.GetSpacing()
    origin = out.GetOrigin()
    brain = (image,spacing,origin)
    return brain

def save_mha (brain,path,dim=3,dtype='int'):
 
    if 'float' in dtype:
        itk_type = itk.F
    elif 'int' in dtype:
        itk_type = itk.SS

    image_type = itk.Image[itk_type, dim]
    itk_py_converter = itk.PyBuffer[image_type]


    writer = itk.ImageFileWriter[image_type].New()
    writer.SetFileName(path)

    itk_image = itk_py_converter.GetImageFromArray(brain[0].tolist() )
    itk_image.SetSpacing(brain[1])
    itk_image.SetOrigin(brain[2])

    writer.SetInput(itk_image.GetPointer())
    writer.UseCompressionOn()
    writer.Update()


