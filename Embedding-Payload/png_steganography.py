import sys
import imageio as iio

# Handle errors occuring while a file is being read or written
def handle_errors(error):

    if isinstance(error,FileNotFoundError): 
        sys.exit("File cannot be found at the specified path. Please provide a valid path.")
    elif isinstance(error,PermissionError):
        sys.exit("Insufficient permissions to read the specified file. Check your permissions.")
    elif isinstance(error,IsADirectoryError):
        sys.exit("Expected a file, but found a directory. Please provide a valid path to a file.")
    else:
        sys.exit(f"An error occurred: {error}.")

# Load the user's image
def load_image(image_path):

    try:
        return iio.v3.imread(image_path)
    except Exception as e:
        handle_errors(e)

def prepare_payload(payload_path):

    # Load the payload from a file
    try:
        with open(payload_path,'r') as f:
            payload = f.read()
    except Exception as e:
        handle_errors(e)

    # Convert the payload to binary
    #
    # The payload gets converted to a bytes object by using UTF-8 encoding.An ASCII character 'a' is represented as a
    # single byte, while ASCII characters like '€' are represented by two or more bytes. Using this approach we can 
    # make sure to include all ASCII characters from 0 - 255.
    #
    # Furthermore the format makes sure that every byte has least 8 bits which means that if necessary padding
    # with zeros is applied
    #
    payload_binary = ''.join(format(byte, '08b') for byte in payload.encode('utf-8'))

    return payload_binary

def least_significant_bit(stego_medium, payload_binary):

    # Store dimension and amount of channels of picture
    stego_medium_height = stego_medium.shape[0]
    stego_medium_width = stego_medium.shape[1]
    stego_medium_channel = stego_medium.shape[2]

    payload_index = 0 # Index to access bit of paylaod
    payload_length = len(payload_binary) # Store boundary of payload

    # Manipulate the LSB at every channel (R,G,B) at every pixel
    for i in range(stego_medium_height):
        for j in range(stego_medium_width):
            for k in range(stego_medium_channel):
                if payload_index < payload_length: # Manipulate as long as there are bits of the payload left

                    current_channel = stego_medium[i][j][k] # Store value of the current channel

                    if payload_binary[payload_index] == '1': # Change LSB to 1 by bitwise or, when payload is 1
                        stego_medium[i][j][k] |= 1
                    else: # Change/Clear LSB to 0 by bitwise and, when payload is 0
                        stego_medium[i][j][k] &= 0b11111110

                    payload_index += 1 # Increment payload index to go to next bit of the payload

                else: # When whole payload was embedded into the image save the new image
                    iio.v3.imwrite('modified.png',stego_medium)
                    return "Payload embedded into picture!"

def check_files(files):

    # Checks if user inputs are at least one .txt and one .png
    if not files[0].endswith('.txt') and not files[1].endswith('.txt'):
        sys.exit("Please add your payload as a .txt file.")
    elif not files[0].endswith('.png') and not files[1].endswith('.png'):
        sys.exit("Please add your picture as a .png file.")

    # Check if files were passed in the wrong order
    if files[0].endswith('.png') and files[1].endswith('.txt'):
        return 0

    return 1

# ASCII art which gets printed every time when the program is executed
def print_ascii_art():
    art = r"""
  _____  _   _  _____    _____ _                                                     _           
 |  __ \| \ | |/ ____|  / ____| |                                                   | |          
 | |__) |  \| | |  __  | (___ | |_ ___  __ _  __ _ _ __   ___   __ _ _ __ __ _ _ __ | |__  _   _ 
 |  ___/| . ` | | |_ |  \___ \| __/ _ \/ _` |/ _` | '_ \ / _ \ / _` | '__/ _` | '_ \| '_ \| | | |
 | |    | |\  | |__| |  ____) | ||  __/ (_| | (_| | | | | (_) | (_| | | | (_| | |_) | | | | |_| |
 |_|    |_| \_|\_____| |_____/ \__\___|\__, |\__,_|_| |_|\___/ \__, |_|  \__,_| .__/|_| |_|\__, |
                                        __/ |                   __/ |         | |           __/ |
                                       |___/                   |___/          |_|          |___/                               
    """
    print(art)


def main():

    print_ascii_art()

    if len(sys.argv) < 3: # There are arguments missing for the program
        print("Usage: python png_steganography.py <file_path_payload> <file_path_picture>")
        print("The payload has to be a .txt file and the picture has to be a .png file")
    else: 
        if check_files([sys.argv[1],sys.argv[2]]) == 0: # When user first inserts picture and then payload
            stego_image = load_image(sys.argv[1])
            prepared_payload = prepare_payload(sys.argv[2])
            print(least_significant_bit(stego_image,prepared_payload))
        else: # When user first inserts payload and then picture
            stego_image = load_image(sys.argv[2])
            prepared_payload = prepare_payload(sys.argv[1])
            print(least_significant_bit(stego_image,prepared_payload))

if __name__ == "__main__":
    main()