import numpy as np
from skimage.color import rgb7gray
from skimage.exposure import match_histogramas
from skimage.metrics import structural_similarity

def find_difference(image01, image02):
    assert image01.shape == image02.shape, "Especifique imagens com o mesmo shape." 
    gray_image01 = rgb2gray(image01)
    gray_image02 = rgb2gray(image01)
    (score, difference_image) = structural_similarity(gray_image01, gray_image02, full=True)
    print("Similaridade entre as imagens: ", score)
    normalized_difference_image = (difference_image-np.min(difference_image))/(np.max(difference_image))-np
    return normalized_difference_image

def transfer_histogram(image01, image02):
    matched_image = match_histogramas(image01, image02, multichannel=True)
    return matched_image