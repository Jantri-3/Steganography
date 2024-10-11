# Generic libraries
import sys
# For processing and manipulating image files (extracting) 
import imageio as iio
# For processing and manipulating text (decoding/decrypting)
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from mpmath import mp

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

def generate_pifile(length, frac, filepath):

    # Just in case
    try:
        length = int(length)
    except ValueError as error:
        sys.exit("Interpreted file length cannot be parsed to an integer. Please report this to a developer!")
    
    mp.dps = length + 1
    pi_value = str(mp.pi * frac)

    with open(filepath, "w") as file:
        file.write(pi_value)

###

### MAIN FUNCTIONS ###

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

    ### Step 1: extract the actual payload from the input (method will depend on whether time-based encoding is used)
    aux_filepath = "auxconstant.txt"
    
    if payload[:4] == "TIME":
        _, timestr, payload = payload.split(" ")
        hour, minute, second = timestr.split(":")

        num_of_seconds = hour * 3600 + minute * 60 + second
        timefrac = num_of_seconds / (24 * 3600)

        length = len(payload) # Does not include "TIME hh:mm:ss "
        generate_pifile(length, frac = timefrac, filepath = aux_filepath)

        with open(aux_filepath, "r") as file:
            decimals = file.read(length + 2)[2:]
        decimals = list(decimals)

    else:
        length = len(payload)
        generate_pifile(length, frac = 1, filepath = aux_filepath)

        with open(aux_filepath, "r") as file:
            decimals = file.read(length + 2)[2:]
        decimals = list(decimals)

    # Obfuscation logic example (to hide the first character of the encoded payload): 
    # - generate a 10 character long string full of random characters
    # - get the first (index=0) decimal digit of the constant we picked (pi * frac, where frac = 1 if no time encoding is used)
    # - use that digit as an index to pick which of the 10 random characters we're going to replace with the first character of the payload
    # - pseudocode: random_string[k] = encoded_payload[0], where k = decimals[0]

    # Deobfuscation logic example (bearing in mind we know the constant used to generate decimals[]):
    # - for every 10-character 'chunk', extract the character whose index matches the corresponding digit of the constant
    result = ""
    for i in range(int(length // 10)):
        offset = decimals[i]
        result += payload[10*i+offset]
    
    # Since I want to use "payload" as my variable from here onwards, we're going to replace the original value with the extraction result
    payload = result

    ### Step 2: undo the base32-encoding step
    payload = payload.encode('utf-8')
    payload = base64.b32decode(payload)

    ### Step 3: decypher the payload
    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password = None)

    chunks = [payload[i:i+50] for i in range(0, len(payload), 50)]

    plaintext = ""
    for chunk in chunks:
        plaintext += private_key.decrypt(
            chunk.decode(), 
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None)
        )
    
    return plaintext

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