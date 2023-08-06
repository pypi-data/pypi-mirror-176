#funções para salvar e escrever
from skimage.io import imred, imsave

def read_image(path, is_gray = False):
    image = imread(path, as_gray = is_gray)
    return image

def save_image(image, path):
    imsave(path, image)