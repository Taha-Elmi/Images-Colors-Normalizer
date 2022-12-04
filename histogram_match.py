from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import sys


def get_average_rgb(pixels):
    counter = 0
    rgb = [0, 0, 0]
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            counter += 1
            pixel = pixels[i, j]
            rgb[0] += pixel[0]
            rgb[1] += pixel[1]
            rgb[2] += pixel[2]
    return [x / counter for x in rgb]


if __name__ == "__main__":
    source_filename = "Source.jpg"
    reference_filename = "Reference.jpg"

    if len(sys.argv) > 1:
        source_filename = sys.argv[1]
    if len(sys.argv) > 2:
        reference_filename = sys.argv[2]

    source = Image.open(source_filename)
    source_pixels = np.array(source)
    source_rgb = get_average_rgb(source_pixels)

    reference = Image.open(reference_filename)
    reference_pixels = np.array(reference)
    reference_rgb = get_average_rgb(reference_pixels)

    print("src:", source_rgb)
    print("ref:", reference_rgb)

    differential = list(map(lambda i, j: i - j, reference_rgb, source_rgb))
    print("dif:", differential)

    for i in range(source_pixels.shape[0]):
        for j in range(source_pixels.shape[1]):
            pixel = source_pixels[i, j]
            pixel[0] = pixel[0] + differential[0] if pixel[0] + differential[0] >= 0 else 0
            pixel[1] = pixel[1] + differential[1] if pixel[1] + differential[1] >= 0 else 0
            pixel[2] = pixel[2] + differential[2] if pixel[2] + differential[2] >= 0 else 0

    source_rgb = get_average_rgb(source_pixels)
    reference_rgb = get_average_rgb(reference_pixels)
    print("src:", source_rgb)
    print("ref:", reference_rgb)

    new_filename = f'{source_filename.split(".")[0]}_edited.jpg'
    plt.imsave(new_filename, source_pixels.astype(np.uint8))
    plt.imshow(source_pixels)
    plt.show()

