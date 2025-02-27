import vtk
from vtk.util.colors import tomato

filename = "files/test.stl"

sphereSource = vtk.vtkSphereSource()
sphereSource.SetPhiResolution(360)
sphereSource.SetThetaResolution(360)
sphereSource.Update()

# Write the stl file to disk
stlWriter = vtk.vtkSTLWriter()
stlWriter.SetFileName(filename)
stlWriter.SetInputConnection(sphereSource.GetOutputPort())
stlWriter.Write()

# Read and display for verification
reader = vtk.vtkSTLReader()
reader.SetFileName(filename)

mapper = vtk.vtkPolyDataMapper()
if vtk.VTK_MAJOR_VERSION <= 5:
    mapper.SetInput(reader.GetOutput())
else:
    mapper.SetInputConnection(reader.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(tomato)

# Create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

# Create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Assign actor to the renderer
ren.AddActor(actor)

# Enable user interface interactor
iren.Initialize()
renWin.Render()
iren.Start()