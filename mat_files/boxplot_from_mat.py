import numpy as np
from scipy.io import loadmat

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='ssilvar', api_key='VDBHTsfZMOezpId5m162')



if __name__ == '__main__':
    mat_file = 'espacio_completo_saccad.mat'
    mat = loadmat(mat_file)

    # Load CP Distances
    cp_right_eye_magnitude = np.ravel(mat['cp'])
    cp_left_eye_magnitude = mat['cp2']
    cp_right_eye_orientation = mat['cp3']
    cp_left_eye_orientation = mat['cp4']

    # Load control Distances
    control_right_eye_magnitude = np.ravel(mat['control'])
    control_left_eye_magnitude = mat['control2']
    control_right_eye_orientation = mat['control3']
    control_left_eye_orientation = mat['control4']


    # Plot them
    control = go.Box(
        y=control_right_eye_magnitude,
        name='CONTROL',
        marker = dict(
            color = 'rgb(0, 128, 128)',
        )
        )
    cp = go.Box(
        y=cp_right_eye_magnitude,
        name='CP',
        marker = dict(
            color = 'rgb(214, 12, 140)',
        )
        )
    layout = go.Layout(
        title = "Correlation distance",
        width = 1080,
        height = 1920,
        font=dict(size=40, color='#030303'),
        showlegend=False
    )
    data = [control, cp]
    fig = go.Figure(data=data, layout=layout)
    py.image.save_as(fig, filename='a-simple-plot.png')


