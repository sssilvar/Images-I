import os
import nibabel as nb
import matplotlib.pyplot as plt

# Set the filename
# filename = os.path.normpath('/home/sssilvar/Documents/Dataset/test/workspace/002_S_0729/cvs/final_CVSmorph_tocvs_avg35_inMNI152.m3z')
filename = os.path.normpath('/home/sssilvar/Documents/Dataset/test/workspace/002_S_0729/cvs/el_reg_tocvs_avg35_inMNI152.mgz')
filename2 = os.path.normpath('/home/sssilvar/Downloads/final_CVS.mgz')


def load_image(filename, slide, title='Figure'):
    # Load image
    img = nb.load(filename)
    vol = img.get_data()

    # Plot slide
    plt.figure()
    plt.style.use('ggplot')
    plt.imshow(vol[:,:,slide], cmap='gray')
    plt.axis('off')
    plt.title(title)


if __name__ == '__main__':

    # Plot two images
    slide = 128
    title = 'MRI: %s' % os.path.split(filename)[1]
    load_image(filename, slide, title)

    title = 'MRI: %s' % os.path.split(filename2)[1]
    load_image(filename2, slide, title)

    # Show plots
    plt.show()
