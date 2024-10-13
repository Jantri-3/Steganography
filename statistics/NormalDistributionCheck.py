import sys
import imageio as iio
from PIL import Image


def count_lsb(image_path):
    # Open the image
    img = Image.open(image_path)
    
    # Convert image to RGB if not already in that mode
    if img.mode != 'RGB' and img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Get pixel data
    pixels = img.getdata()
    
    count_0 = 0
    count_1 = 0
    
    # Iterate over each pixel
    for pixel in pixels:
        # Iterate over each channel (R, G, B, A)
        for value in pixel[:3]:  # Ignore alpha channel if present ([:3] for RGB, [:4] for RGBA)
            # Get the LSB by using bitwise AND with 1
            lsb = value & 1
            
            if lsb == 0:
                count_0 += 1
            else:
                count_1 += 1
    
    return count_0, count_1


def main():
    # Check if the filename is passed as an argument
    if len(sys.argv) < 2:
        print("Usage: python NormalDistributionCheck.py <Processed_filename> <Original_filename>")
        print("filename of the payload embedded image .png")
        print("filename of the original .png")
        sys.exit(1)


    image_path = sys.argv[2]
    count_0, count_1 = count_lsb(image_path)
    total = count_0 + count_1
    print("Original image ---------------------------------------------")
    print(f"Original number of 0's= {count_0}")
    print(f"Original number of 1's= {count_1}")
    print(f"Total number of 0's+1's befroe processing: {total}")
    print(f"Percentage of 0's {(count_0/total) * 100}%")
    print(f"Percentage of 1's {(count_1/total) * 100}%")

    image_path = sys.argv[1]
    proc_count_0, proc_count_1 = count_lsb(image_path)
    proc_total = proc_count_0 + proc_count_1
    print("Processed image ---------------------------------------------")
    print(f"Processed number of 0's= {proc_count_0}")
    print(f"Processed number of 1's= {proc_count_1}")
    print(f"Total number of 0's+1's after processing: {proc_total}")
    print(f"Percentage of 0's {(proc_count_0/proc_total) * 100}%")
    print(f"Percentage of 1's {(proc_count_1/proc_total) * 100}%")

    print("---------------------------------------------")




if __name__ == "__main__":
    main()