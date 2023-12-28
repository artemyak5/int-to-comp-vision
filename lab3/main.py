import cv2 as cv
import numpy as np

image_path = '/Users/artemakubec/Downloads/прога/python/intToCompVis/dom.png'
image = cv.imread(image_path)

matrix_kernel = np.ones((7, 7))


def pad_image(img, width):
    return np.pad(img, ((width, width),
                        (width, width),
                        (0, 0)),
                  mode='edge')


def morph_op(img, kernel, mode='erosion'):
    width_kernel = kernel.shape[0]
    img = ((-1) * (img + 1)) % 256
    padded_img = pad_image(img, int(width_kernel / 2))
    result_img = np.empty(img.shape)

    if mode == 'erosion':
        for x in range(img.shape[0]):
            for y in range(img.shape[1]):
                if np.vdot(padded_img[x:x + width_kernel, y:y + width_kernel, 0], kernel) == kernel.sum() * 255:
                    result_img[x, y] = [255, 255, 255]
                else:
                    result_img[x, y] = [0, 0, 0]
    else:  # Assuming if mode is not 'e', it is 'd'
        for x in range(img.shape[0]):
            for y in range(img.shape[1]):
                if np.vdot(padded_img[x:x + width_kernel, y:y + width_kernel, 0], kernel) > 0:
                    result_img[x, y] = [255, 255, 255]
                else:
                    result_img[x, y] = [0, 0, 0]

    return (((-1) * (result_img + 1)) % 256).astype('uint8')


def closing(img, kernel):
    dilated_img = morph_op(img, kernel, 'dilation')
    closed_img = morph_op(dilated_img, kernel, 'erosion')
    return closed_img


def opening(img, kernel):
    eroded_img = morph_op(img, kernel, 'erosion')
    open_img = morph_op(eroded_img, kernel, 'dilation')
    return open_img


cv.imwrite('erosion.jpg', morph_op(image, matrix_kernel, 'erosion'))
cv.imwrite('dilation.jpg', morph_op(image, matrix_kernel, 'dilation'))
cv.imwrite('closing.jpg', closing(image, matrix_kernel))
cv.imwrite('opening.jpg', opening(image, matrix_kernel))

