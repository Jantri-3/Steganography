import png_steganography
import payload
import sys
import imageio

# This program makes both the payload creation and embedding happen in one step
def main():
    # Check if the program is used correctly, in particular
    # we want the input to contain an image and a plaintext files.
    if len(sys.argv) < 3:
        print("Usage: python embed_all_in_one.py <image_filename> <plaintext_filename> [y]")
        print("<image_filename>: filename from where to read the image")
        print("<plaintext_filename>: filename from where to read the plaintext")
        print("y: if you want to have more security, use this option in order for the pi decimals to be multiplied by a fraction of the timedate")
        sys.exit(1)
    
    image_filename = sys.argv[1]
    try:
        image = imageio.v3.imread(image_filename)
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
    
    sys.argv.remove(image_filename)
    sys.argv[0] = "payload.py"
    sys.argv[1] = sys.argv[1]
    payload.output_mode = "return"
    #print(sys.argv)
    payload_encrypted = payload.main()
    payload_binary = png_steganography.prepare_payload(payload_encrypted)
    print(png_steganography.least_significant_bit(image, payload_binary))
    
if __name__ == "__main__":
    main()
