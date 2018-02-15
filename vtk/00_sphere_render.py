import vtk
from vtk.util.colors import alice_blue

# Create a sphere
sphere = vtk.vtkSphereSource()
sphere.SetPhiResolution(100)
sphere.SetThetaResolution(100)

# Create a mapper
sphere_mapper = vtk.vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

# Create an actor
sphere_actor = vtk.vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(alice_blue)

# Create a renderer
ren = vtk.vtkRenderer()
ren.SetBackground(0, 0, 0)
ren.AddActor(sphere_actor)

# Create a renderer window
ren_window = vtk.vtkRenderWindow()
ren_window.SetWindowName('Sphere rendered in VTK')
ren_window.SetSize(500, 500)
ren_window.AddRenderer(ren)

# Create an interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(ren_window)

# Show it up
interactor.Initialize()
ren_window.Render()
interactor.Start()


