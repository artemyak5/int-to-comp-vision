from PIL import Image

def otsu(link):
    image = Image.open(link)

    image_pixels = list(image.getdata())

    width, height = image.size

    for i in range(len(image_pixels)):
        image_pixels[i] = round((image_pixels[i][0]+image_pixels[i][1]+image_pixels[i][2])/3)

    histogram = [0] * 256
    for pixel_i in image_pixels:
        histogram[pixel_i] += 1

    total_pixels = width * height

    threshold = 0
    max_dispersion = 0

    for threshold_t in range(256):
        class_pixels_1 = sum(histogram[:threshold_t])
        class_pixels_2 = total_pixels - class_pixels_1

        if class_pixels_1 > 0:
            sum1 = 0
            for i in range(threshold_t):
                sum1 += i * histogram[i]
            mean1 = sum1 / class_pixels_1
        else:
            mean1 = 0

        if class_pixels_2 > 0:
            sum2 = 0
            for i in range(threshold_t, 256):
                sum2 += i * histogram[i]
            mean2 = sum2 / class_pixels_2
        else:
            mean2 = 0

        dispersion_between_classes = class_pixels_1 * class_pixels_2 * (mean1 - mean2) ** 2 / total_pixels ** 2

        if dispersion_between_classes > max_dispersion:
            max_dispersion = dispersion_between_classes
            threshold = threshold_t

    binary_data = []

    for pixel_i in image_pixels:
        if pixel_i <= threshold:
            binary_data.append(255)  
        else:
            binary_data.append(0)
    
    binary_image = Image.new('L', (width, height))
    binary_image.putdata(binary_data)

    cropped_image = Image.new('RGB', (width, height))
    for x in range(width):
        for y in range(height):
            if binary_image.getpixel((x, y)) == 0:
                cropped_image.putpixel((x, y), (255, 255, 255))
            else:
                cropped_image.putpixel((x, y), image.getpixel((x, y)))

    text = link
    word_to_insert = "_cut"
    link = text.replace(".", f"{word_to_insert}.", 1)
    cropped_image.save(link)

otsu('/Users/artemakubec/Downloads/прога/python/intToCompVis/Comparing Art Mediums_ Watercolor Paint vs_ Watercolor Pencils.jpeg')
otsu('/Users/artemakubec/Downloads/прога/python/intToCompVis/titul-3.jpg') #text
otsu('/Users/artemakubec/Downloads/прога/python/intToCompVis/50 Cute Texts You Only Receive When You Finally Find A Quality Guy.jpeg')#text
otsu('/Users/artemakubec/Downloads/прога/python/intToCompVis/IMG_5703.jpg')
