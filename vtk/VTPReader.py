import vtk
import os

# Set filename
filename = os.path.join(os.getcwd(), 'files', 'ConePendulum.vtp')

# Reader
reader = vtk.vtkXMLPolyDataReader()
reader.SetFileName(filename)
reader.Update()

# Mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Renderer
ren = vtk.vtkRenderer()
ren.AddActor(actor)

# RenderWindow
ren_win = vtk.vtkRenderWindow()
ren_win.AddRenderer(ren)

# RenderWindowInteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)


# Start it
iren.Initialize()
ren_win.Render()
iren.Start()
