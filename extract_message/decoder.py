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
import os

stego_signature = "yb-c;>zZ~)9>Lw(PnL5Tk@ugrp)N{7"
stego_end = "Cvy$+5cZNw-[r[!w/t(TaIcKa^fT;}"

class Signature_not_found_error:
    #If the file does not contain our custom signature, we throw an exception
    pass

### AUXILIARY FUNCTIONS ###

# (Written by Nils)
# Try to load the image specified in the input argument
def load_image(image_path):

    # Checks whether the specified path corresponds to a png or not: if not, abort.
    if not image_path.endswith(".png"):
        sys.exit("Specified file is not a png file. Please provide a valid path to a png file.")

    try:
        return iio.v3.imread(image_path)
    except Exception as error:
        # Handles file errors, same as nils's "handle_errors" function
        if isinstance(error, FileNotFoundError): 
            sys.exit("Image file cannot be found at the specified path. Please provide a valid path.")
        elif isinstance(error, PermissionError):
            sys.exit("Insufficient permissions to read the specified image file. Check your permissions.")
        elif isinstance(error, IsADirectoryError):
            sys.exit("Expected a file, but found a directory. Please provide a valid path to an image file.")
        else:
            sys.exit(f"An error occurred while attempting to load the image file: {error}.")

def load_private_key(key_path):

    if not key_path.endswith(".pem"):
        sys.exit("Specified file is not a pem file. Please provide a valid path to a pem file.")

    try:
        with open(key_path, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password = None)
    except Exception as error:
        if isinstance(error, FileNotFoundError): 
            sys.exit("Key file cannot be found at the specified path. Please provide a valid path.")
        elif isinstance(error, PermissionError):
            sys.exit("Insufficient permissions to read the specified key file. Check your permissions.")
        elif isinstance(error, IsADirectoryError):
            sys.exit("Expected a file, but found a directory. Please provide a valid path to a key file.")
        else:
            sys.exit(f"An error occurred while attempting to load the key file: {error}.")

    return private_key

def generate_pifile(length, frac, filepath):
    print(frac)

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
def binary_to_string(binary_payload):
    all_characters = [] 
    
    for i in range(0, len(binary_payload), 8):
        byte = binary_payload[i:i+8] #one byte of the input
        single_character = chr(int(byte, 2)) #byte to integer to character
        all_characters.append(single_character) #insert the character in the buffer
        
    return "".join(all_characters) #convert the buffer to a string

# Takes a stegomedium (PNG flag) and a corresponding steganography method (e.g.: LSB) and
# returns the payload within.
def extract_payload(stego_image, method):
    stego_image_height = stego_image.shape[0]
    stego_image_width = stego_image.shape[1]
    stego_image_channel = stego_image.shape[2]
    
    reading_index = 0
    signature_binary = ''.join(format(byte, '08b') for byte in stego_signature.encode('utf-8'))
    signature_length = len(signature_binary)
    
    embedded_payload = ""
    
    stego_end_binary = ''.join(format(byte, '08b') for byte in stego_end.encode('utf-8'))
    stego_end_length = len(stego_end_binary)
    stego_end_buffer = ""
    
    for i in range(stego_image_height):
        for j in range(stego_image_width):
            for k in range(stego_image_channel):
                if reading_index < signature_length:
                    if int(stego_image[i][j][k] & 1) == int(signature_binary[reading_index]):
                        reading_index += 1
                    else:
                        #one of the first len(signature) bits does not match the corresponding bit on the signature
                        raise Signature_not_found_error
                else:
                    lsb = stego_image[i][j][k] & 1
                    embedded_payload += str(lsb)
                    stego_end_buffer += str(lsb)
                    
                    if len(stego_end_buffer) > stego_end_length:
                        #the length of the buffer must match the length of the end signature at all times
                        stego_end_buffer = stego_end_buffer[-stego_end_length:]
                        
                    if stego_end_buffer == stego_end_binary:
                        print("Payload successfully extracted!\nDecoding in progress...\n")
                        embedded_payload = embedded_payload[:-stego_end_length]
                        return binary_to_string(embedded_payload)

# Takes a payload and decodes it, reversing the steps taken in Payload Creation (by Nils) and
# returning the decoded original message.
def decode_payload(payload):

    ### Step 1: extract the actual payload from the input (method will depend on whether time-based encoding is used)
    aux_filepath = "auxconstant.txt"
    key_filepath = "private_key.pem"
    
    if payload[:4] == "TIME":
        _, timestr, payload = payload.split(" ")
        hour, minute, second = timestr.split(":")

        hour = int(hour)
        minute = int(minute)
        second = int(second)

        num_of_seconds = hour * 3600 + minute * 60 + second
        timefrac = int(num_of_seconds) / (24 * 3600)

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
    payload = payload.strip()
    
    result = ""
    for i in range(int(length // 10)):
        offset = decimals[i]
        result += str(payload[10*i+int(offset)])
    
    # Since I want to use "payload" as my variable from here onwards, we're going to replace the original value with the extraction result
    payload = result

    ### Step 2: undo the base32-encoding step
    payload = payload.encode('utf-8')
    payload = base64.b32decode(payload)

    ### Step 3: decypher the payload (by undoing the steps taken to encrypt it in Payload Creation)
    private_key = load_private_key(key_filepath)

    chunks = [payload[i:i+256] for i in range(0, len(payload), 256)]

    decrypted = bytearray()
    try:
        for chunk in chunks:
            decrypted += private_key.decrypt(
                chunk, 
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None)
            )
    except Exception as error:
        sys.exit(f"An error occurred while attempting to decrypt the payload (is the provided private key right for this payload?): {error}.")

    
    result = decrypted.decode()

    # Clean up temporary files
    if os.path.isfile(aux_filepath):
        os.remove(aux_filepath)

    return result

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
        try:
            payload = extract_payload(image, method= "LSB")
            try:
                result = decode_payload(payload)
            except Exception as error:
                sys.exit(f"An error occurred: {error}.")
        except Signature_not_found_error as error:
            sys.exit("Loaded file does not contain any hidden message")
        print("Success! The hidden message is:\n")
        print(result)

if __name__ == "__main__":
    main()