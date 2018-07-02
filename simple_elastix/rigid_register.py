from __future__ import print_function
import time

import SimpleITK as sitk

if __name__ == '__main__':
    ti = time.time()
    template_file = r'/home/sssilvar/Documents/data/eheart/patient002/patient002_frame01.nii.gz'
    subject_file = r'/home/sssilvar/Documents/data/eheart/patient001/patient001_frame01.nii'

    elastixImageFilter = sitk.ElastixImageFilter()
    elastixImageFilter.LogToConsoleOn()
    elastixImageFilter.SetFixedImage(sitk.ReadImage(template_file))
    elastixImageFilter.SetMovingImage(sitk.ReadImage(subject_file))
    elastixImageFilter.SetParameterMap(sitk.GetDefaultParameterMap("rigid"))
    elastixImageFilter.Execute()
    sitk.WriteImage(elastixImageFilter.GetResultImage(), 'registered.nii.gz')

    tf = time.time()
    print('Total task %f' % (tf - ti))
