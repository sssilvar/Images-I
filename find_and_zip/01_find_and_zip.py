import os
import zipfile

# Set folder to zip
folder = '/home/sssilvar/Pictures'
folder = os.path.join(folder)

# Look for file extension
ext = '.mat'
files_to_zip = []

for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith(ext):
            filename = os.path.join(root, file)
            print(filename)
            files_to_zip.append(filename)

zf = zipfile.ZipFile("zip Dataset_riie_mat_files.zip", "w")

for fi in files_to_zip:
    zf.write(fi, compress_type=zipfile.ZIP_DEFLATED)
