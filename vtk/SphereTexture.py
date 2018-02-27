import vtk
import os
import numpy as np
from vtk.util.colors import azure

jpegfile = 'files/masonry-wide.jpg'

# Create a render window
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(600, 600)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Generate an sphere polydata
sphere = vtk.vtkSphereSource()
sphere.SetThetaResolution(360)
sphere.SetPhiResolution(360)

# Read the image data from a file
reader = vtk.vtkJPEGReader()
reader.SetFileName(jpegfile)

# Create texture object
texture = vtk.vtkTexture()
if vtk.VTK_MAJOR_VERSION <= 5:
    texture.SetInput(reader.GetOutput())
else:
    texture.SetInputConnection(reader.GetOutputPort())

# Map texture coordinates
map_to_sphere = vtk.vtkTextureMapToSphere()
if vtk.VTK_MAJOR_VERSION <= 5:
    map_to_sphere.SetInput(sphere.GetOutput())
else:
    map_to_sphere.SetInputConnection(sphere.GetOutputPort())
map_to_sphere.PreventSeamOn()

# Create mapper and set the mapped texture as input
mapper = vtk.vtkPolyDataMapper()
if vtk.VTK_MAJOR_VERSION <= 5:
    mapper.SetInput(map_to_sphere.GetOutput())
else:
    mapper.SetInputConnection(map_to_sphere.GetOutputPort())

# Create actor and set the mapper and the texture
actor = vtk.vtkActor()
actor.GetProperty().SetColor(azure)
actor.SetMapper(mapper)
actor.SetTexture(texture)

ren.AddActor(actor)

iren.Initialize()
renWin.Render()
iren.Start()