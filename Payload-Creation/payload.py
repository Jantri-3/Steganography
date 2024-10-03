import sys
#Used for ciphering the message (Step 1)
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
#Used for encoding in base 32 (Step 2)
import base64
from datetime import datetime
from pi_decimals import n_of_pi_decimals 
#For step3 random chars
import random
import string 

Use_time = False
Cipherkey = b'ArbitraryKey'#Not used
Outputfile = "payload.txt"
pifile = "pi_decimals.txt"

#Step 1 cipher text
def cipher(contents):
    #We open the file where the public key is stored
    with open("public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read(),backend=default_backend())#Store the key

    # Encrypt the message using RSA
    ciphertext = public_key.encrypt(contents.encode(),#encode into bytes
                                    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None)
                                    )
        #We are using Optical Assymetric Encryption Padding (Padding scheme to assure randomness -this padding is NOT deterministic-)
        # mgf=padding.MGF1(algorithm=hashes.SHA256())
        # MGF1 (Mask Generation Function 1): 
        # Cryptographic function used in conjunction with OAEP. 
        # It will generates a mask (sequence of bytes used to randomize the encryption)
        #
        #hashes.SHA256(): 
        # We are using SHA256 in the MGF
        #
        #algorithm=hashes.SHA256()
        #We are ensuring SHA256 is the MAIN hashing function used in the OAEP

    return ciphertext

#Step 3 cover the message using pi decimals
def picover(contents):
    cover = ""
    length = len(contents)
    if Use_time:
            f = fraction_of_day(Outputfile)
    if length > 10000:
        n_of_pi_decimals(length)
        with open("npi_decimals.txt", "rb") as f:
            pipositions = f.read(length)
    else:
        with open("pi_decimals.txt", "rb") as f:
            pipositions = f.read(length)
    for i in length:
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        if Use_time:
            substitute_char(random_string,pipositions*f,contents[i])
        else:
            substitute_char(random_string,pipositions,contents[i])
        
        cover+= contents
    
    return cover

#Substitute chars
def substitute_char(s, i, new_char):
    if 0 <= i < len(s):
        s = s[:i] + new_char + s[i+1:]
    return s

def fraction_of_day(filename):
    now = datetime.now()
    #We get the current hour, minute, and second
    hours = now.hour
    minutes = now.minute
    seconds = now.second

    #We write it to the payload file in order to place it in the metadata
    with open(filename, 'w') as f:
        f.write(now.strftime("%H:%M:%S \n"))

    #we get the seconds since 0:0:00
    current_seconds = hours * 3600 + minutes * 60 + seconds

    #Out of all the seconds in a day
    total_seconds_in_a_day = 24 * 3600

    #We get the fraction of day that has passed since midnight to the current time
    frac_of_day = current_seconds / total_seconds_in_a_day
    return frac_of_day


def main():
    # Check if the filename is passed as an argument
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename> [y]")
        print("filename form where to read the plaintext")
        print("y: in order to have more security, use this option in order for the pi decimals to be multiplied by a fraction of the timedate")
        sys.exit(1)

    # Get the filename from the command-line argument
    filename = sys.argv[1]

    #specify number of decimals(-1)
    if len(sys.argv) >= 3:
        if sys.argv[2] == 'y':
            Use_time = True
        
    try:
        #get the payload
        with open(filename, 'r') as input_file:
            contents = input_file.read()

        print("hi1-------------")
        #Step 1 Cypher: cypher the contents
        s1contents = cipher(contents)

        print("hello2------------")
        #Step 2 Base32(Linguistics): encode the contents to base 32
        s2contents = base64.b32encode(s1contents)


        print("hi3-------------")
        #Step 3 Pi(Linguistics):use pi decimals to "cover" the base 32
        #& Step 4 TimeFraction: use a fraction of pi depending on the date time of the execution to hide it even better 
        #If this option is ativated (using 'y') it will leave one line with the current time of the execution
        s3contents = picover(s2contents)
        print("hi4??-------------")

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
    
    #Finalstep
    try:
        with open(Outputfile,'w')as output_file:
            output_file.write(s3contents)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
