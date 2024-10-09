# Generic libraries
import sys
# For processing and manipulating image files (extracting) 
import imageio as iio

### AUXILIARY FUNCTIONS ###

# (Written by n0rdan)
# Try to load the image specified in the input argument
def load_image(image_path):

    # Checks whether the specified path corresponds to a png or not: if not, abort.
    if not image_path.endswith(".png"):
        sys.exit("Specified file is not a png. Please provide a valid path to a png file.")

    try:
        return iio.v3.imread(image_path)
    except Exception as error:
        # Handles file errors, same as n0rdan's "handle_errors" function
        if isinstance(error, FileNotFoundError): 
            sys.exit("File cannot be found at the specified path. Please provide a valid path.")
        elif isinstance(error, PermissionError):
            sys.exit("Insufficient permissions to read the specified file. Check your permissions.")
        elif isinstance(error, IsADirectoryError):
            sys.exit("Expected a file, but found a directory. Please provide a valid path to a file.")
        else:
            sys.exit(f"An error occurred: {error}.")

# Takes a stegomedium (PNG flag) and a corresponding steganography method (e.g.: LSB) and
# returns the payload within.
def extract_payload(stegomedium, method):
    # Steps to take:
    # 1. Figure out if there is an actual payload in the image, exit if not.
    # 2. Implement logic on extracting LSB
    # i really dont know how to subdivide this step
    # Will be done later
    pass

# Takes a payload and decodes it, reversing the steps taken in Payload-Creation (by Jantri) and
# returning the decoded original message.
def decode_payload(payload):
    # TODO
    # Steps to take:
    # 1. Determine whether time-based encoding was used by analyzing the first section of the payload.
    # 2. Getting the characters pertaining to the actual encoded message, discarding the random junk.
    # 3. Base-32 decode the results obtained above.
    # 4. Decipher the results obtained above, as per the encryption mechanism used in Payload-Creation.
    #
    # Will be done later
    pass

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
________________________________________________________________________________________________,,,
______                   _           
|  _  \                 | |          
| | | |___  ___ ___   __| | ___ _ __ 
| | | / _ \/ __/ _ \ / _` |/ _ \ '__|
| |/ /  __/ (_| (_) | (_| |  __/ |   
|___/ \___|\___\___/ \__,_|\___|_|   
    
    """
    print(art)

def main():

    print_ascii_art()

    if len(sys.argv) < 2: # There are arguments missing for the program
        print("Usage: python png_steganography.py <file_path_payload> <file_path_picture>")
        print("The payload has to be a .txt file and the picture has to be a .png file")
    else:
        image = load_image(sys.argv[1])
        payload = extract_payload(image, method = "LSB")
        result = decode_payload(payload)

        # TODO: Display an error message if the image in the supplied path did not contain a payload.
        print("Success! The hidden message is:\n")
        print(result)

if __name__ == "__main__":
    main()