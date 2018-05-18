import os


if __name__ == '__main__':
    data_folder = '/home/ssilvari/Downloads/Groundtruth'
    output_folder = '/home/ssilvari/Downloads/migue_converted'
    extensions = ['nii', 'nii.gz']

    for root, dirs, files in os.walk(data_folder):
        for file in files:
            for ext in extensions:
                if file.endswith(ext):
                    filename = os.path.join(root, file)

                    cmd = 'mri_convert ' + filename + ' ' + os.path.join(output_folder, ext, file[:-(len(ext) +1)] + '.mgz') + ' -c'
                    print('[  OK  ] Running command: ' + cmd)
                    os.system(cmd)
