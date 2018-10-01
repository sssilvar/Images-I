import vtk
import os

# Set filename
# filename = os.path.join(os.getcwd(), 'files', 'lh.vtk')
filename = '/user/ssilvari/home/Documents/temp/PCA_results/data_simulation/surfaces/thick_10/thick_10_PC1.obj'

# Set a VTKReader
reader = vtk.vtkDataObjectReader()
reader.SetFileName(filename)
reader.Update()

# Set a mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Set an actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Renderer
ren = vtk.vtkRenderer()
ren.AddActor(actor)

# RenderWindow
ren_win = vtk.vtkRenderWindow()
ren_win.AddRenderer(ren)

# WindowInteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

# Start it!
iren.Initialize()
ren_win.Render()
iren.Start()
