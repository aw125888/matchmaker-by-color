import numpy as np
import PIL.Image as Image

#take in an image
#analyze image and return color histogram representation 
#visualize histogram using matplotlib

def load_image(path):
    return Image.open(path)

def get_pixels(image):
    HSV_image = np.array(image.convert('HSV'))
    pixels = HSV_image.reshape(-1, 3)  # Reshape to a 2D array of pixels
    return pixels



#choose 1 of 36 hue groups, 1 of 4 saturation groups, and 1 of 4 brightness groups, convert these 3 group nums into one pos
def get_bin(h,s,v):
    h_bin = int(h) * 36//256 
    s_bin = int(s) //64
    v_bin = int(v) //64 

    return h_bin * 16 + s_bin * 4 + v_bin #0-575

def build_histogram(pixels):
    histogram = np.zeros(576)
    for pixel in pixels:
        h,s,v = pixel
        bin_index = get_bin(h,s,v)
        histogram[bin_index] += 1
    total_pix = len(pixels)
    histogram/= total_pix
    return histogram


def visualize_histogram(histogram):
    # Get indices of the 8 most common bins, largest first
    eight_highest = np.argsort(histogram)[-8:][::-1]

    rgb_colors = []

    for index in eight_highest:
        # Recover the hue, saturation, and brightness bin numbers
        h_bin = index // 16
        s_bin = (index % 16) // 4
        v_bin = index % 4

        # Use the center of each bin as the representative color
        h = int((h_bin + 0.5) * (256 / 36))
        s = int((s_bin + 0.5) * 64)
        v = int((v_bin + 0.5) * 64)

        # Convert representative HSV color to RGB
        rgb_color = Image.new("HSV", (1, 1), (h, s, v)).convert("RGB").getpixel((0, 0))

        rgb_colors.append(rgb_color)

    return rgb_colors

def shift_hue(histogram, shift_value):
    shifted_histogram = np.zeros_like(histogram)

    for index in range(len(histogram)):
        h_bin = index // 16
        s_bin = (index % 16) // 4
        v_bin = index % 4

        # Shift the hue bin and wrap around using modulo
        new_h_bin = (h_bin + shift_value) % 36

        # Calculate the new index in the histogram
        new_index = new_h_bin * 16 + s_bin * 4 + v_bin

        # Assign the value to the new index in the shifted histogram
        shifted_histogram[new_index] += histogram[index]

    return shifted_histogram

def shift_complementary(histogram):
    return shift_hue(histogram, 18)

def shift_soft_complementary(histogram):
    return shift_hue(histogram, 13)

def shift_analogous(histogram):
    shifted_histograms = []
    for shift_value in [-3, 3]: 
        shifted_histogram = shift_hue(histogram, shift_value)
        shifted_histograms.append(shifted_histogram)
    return shifted_histograms


 

