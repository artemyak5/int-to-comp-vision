from PIL import Image
import numpy as np

pixelart = Image.open('/Users/artemakubec/Downloads/прога/python/lab2/lab2/1.jpeg')

pixelmov20_10 = np.zeros((41, 41))
pixelmov20_10[0, 9] = 1

invers_mat = np.zeros((3, 3))
invers_mat[1, 1] = -1

Blurring = np.eye(7)

increasing_sharpness = np.array([[0, -1, 0],
                                 [-1, 5, -1],
                                 [0, -1, 0]])

Sobel_filter = np.array([[-1, -2, -1],
                    [0, 0, 0],
                    [1, 2, 1]])

Bord_filter = np.array([[-1, -1, -1],
                 [-1, 8, -1],
                 [-1, -1, -1]])

amoungus = np.array([[0.65432210, 0.87654321, 0.12345678],
                           [0.98765432, 0.54321098, 0.13579246],
                           [0.24680135, 0.99900011, 0.11122233]])


def gaus_ker(x, y):
    return (1 / (np.pi * 2)) * np.exp(-1 * (abs(x - y) ** 2) / 2)



gaus = np.empty((11, 11))
for x in range(11):
    for y__ in range(11):
        gaus[x, y] = gaus_ker(x, y)


changed_size_tuple = tuple((np.array(pixelart.size) * 0.3).astype(int))[::-1]
changed_size_img = pixelart.resize(changed_size_tuple)


def add_padding_to_image(img, width):
    img_array = np.array(img)
    padded_array = np.pad(img_array, ((width, width), (width, width), (0, 0)))
    padded_img = Image.fromarray(padded_array)
    return padded_img



def convolve_image(img, kernel, d=1):
    img_array = np.array(img)
    kw = kernel.shape[0]  
    pad_img = add_padding_to_image(img, int(kw / 2))
    result_img = np.ndarray(img_array.shape)
    for x in range(img_array.shape[0]):
        for y in range(img_array.shape[1]):
            for k in range(3):
                result_img[x, y][k] = int(np.vdot(pad_img[x:x + kw, y:y + kw, k], kernel) / d)
    result_img = (result_img % 256).astype('uint8')
    return Image.fromarray(result_img)


convolve_image(pixelart, pixelmov20_10).save('pixelmov20_10.jpg')
convolve_image(pixelart, invers_mat).save('invers-mat.jpg')
convolve_image(pixelart, gaus, gaus.sum()).save('gaus.jpg')
convolve_image(pixelart, Blurring, 7).save('Blurring.jpg')
convolve_image(convolve_image(pixelart, increasing_sharpness), np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]), 16).save('increasing_sharpness.jpg')
convolve_image(pixelart, Sobel_filter).save('Sobel-filter.jpg')
convolve_image(pixelart, Bord_filter).save('Bord-filter.jpg')
convolve_image(pixelart, amoungus).save('amoungus.jpg')
