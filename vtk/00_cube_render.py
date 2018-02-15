import vtk
from vtk.util.colors import azure

# 1. Source
# Generate polygon data for a cube: cube
cube = vtk.vtkCubeSource()

# 2. Mapper
# Create a mapper for the cube data: cube_mapper
cube_mapper = vtk.vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube.GetOutputPort())

# 3. Actor
# Connect the mapper to an actor: cube_actor
cube_actor = vtk.vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.GetProperty().SetColor(azure)

# 4. Renderer
# Create a renderer and add the cube actor to it
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)
renderer.AddActor(cube_actor)

# 5. Render Window
# Create a render window
render_window = vtk.vtkRenderWindow()
render_window.SetWindowName('Simple VTK scene')
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)

# 6. Interactor
#  Create an interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Initialize de interactor and start the
# rendering loop
interactor.Initialize()
render_window.Render()
interactor.Start()


