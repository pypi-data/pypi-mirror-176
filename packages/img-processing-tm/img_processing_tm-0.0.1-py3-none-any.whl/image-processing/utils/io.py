from skimage.io import imread, imsave

def read_image(path, is_gray = False):
    image = imread(path,as_gray = is_gray)
    return image

def save_image(image, path):
    image(path, image)

    