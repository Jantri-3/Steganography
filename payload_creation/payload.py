import sys
import os
#Used for ciphering the message (Step 1)
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
#Used for encoding in base 32 (Step 2)
import base64
from datetime import datetime

from payload_creation import pi_decimals

#For step3 random chars
import random
import string 

Use_time = False
Cipherkey = b'ArbitraryKey'
Outputfile = "payload.txt"
pifile = "pi_decimals.txt"
output_mode = "write"

def split_string(str):
    # We split the string into chunks of 190 characters this number should be changed depending on the pair of keys legnght used!!!
    return [str[i:i+190] for i in range(0, len(str), 190)]

#Step 1 cipher text
def cipher(contents):
    ciphertext = bytearray()
    # We open the file where the public key is stored
    with open("public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())# Store the key

    
    chunks = split_string(contents)

    for c in chunks:
       ciphertext += public_key.encrypt(c.encode(),# encode into bytes
                                    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None)
                                    )



    # Encrypt the message using RSA
    #ciphertext = public_key.encrypt(contents.encode(),#encode into bytes
    #                                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None)
    #                                )
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

#Step 3+4 cover the message using pi decimals
def picover(contents):
    cover = ""
    length = len(contents)
    if Use_time:
            frac = fraction_of_day(Outputfile) #calculate (current seconds since 00:00:00)/(total seconds in a day)
            pi_decimals.frac_of_pi_decimals(frac,length)

    if length > (10000 - 2):
        if Use_time:
            with open("timepi_decimals.txt", "r") as f:
                pipositions = f.read(length+2)[2:]#read the length needed skipping the "3." in order to only have the decimals of pi
        else:
            pi_decimals.n_of_pi_decimals(length)
            with open("npi_decimals.txt", "r") as f:
                pipositions = f.read(length+2)[2:]#read the length needed skipping the "3." in order to only have the decimals of pi
                
    else:
        if Use_time:
            with open("timepi_decimals.txt", "r") as f:
                pipositions = f.read(length+2)[2:]#read the length needed skipping the "3." in order to only have the decimals of pi
        else:
            with open("pi_decimals.txt", "r") as f:
                pipositions = f.read(length+2)[2:]
                

    pipositions = list(pipositions)
    for i in range(length):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))# we create a ten random character string

        # we substitute on that random string the character given by contents in the position indicated by piposition
        random_string = substitute_char(random_string,int(pipositions[i]),contents[i]) 
        
        cover = cover + str(random_string)#we concatenate
    
    return cover

#Substitute chars
def substitute_char(s, position, new_char):
    new_char = str(new_char) #As contents may have numbers
    if position < 0 or position >= len(s):#Just in case something weird happens
        return "Position out of range"
    new_string = s[:position] + new_char + s[position+1:] #copy the string form the beginning till the position, add new char, copy the string from the position till the end
    return new_string

def fraction_of_day(filename):
    now = datetime.now()
    #We get the current hour, minute, and second
    hours = now.hour
    minutes = now.minute
    seconds = now.second

    #We write it to the payload file in order to place it in the metadata
    with open(filename, 'w+') as f:
        f.write(now.strftime("TIME %H:%M:%S \n"))

    #we get the seconds since 0:0:00
    current_seconds = hours * 3600 + minutes * 60 + seconds

    #Out of all the seconds in a day
    total_seconds_in_a_day = 24 * 3600

    #We get the fraction of day that has passed since midnight to the current time
    frac_of_day = current_seconds / total_seconds_in_a_day
    return frac_of_day


def main():
    # check if correct usage is followed
    if len(sys.argv) < 2:
        print("Usage: python payload.py <filename> [y]")
        print("filename from where to read the plaintext")
        print("y: in order to have more security, use this option in order for the pi decimals to be multiplied by a fraction of the timedate")
        sys.exit(1)

    # get the filename from the command-line argument
    filename = sys.argv[1]

    # check if we are using tht time of the execution
    if len(sys.argv) >= 3:
        if sys.argv[2] == 'y':
            global Use_time 
            Use_time = True
        
    try:
        # get the payload
        with open(filename, 'r') as input_file:
            contents = input_file.read()
    
        # Step 1 Cypher: cypher the contents
        s1contents = cipher(contents)

        # Step 2 Base32(Linguistics): encode the contents to base 32
        s2contents = base64.b32encode(s1contents)

        s2contents = s2contents.decode('utf-8')
        # Step 3 Pi(Linguistics):use pi decimals to "cover" the base 32
        #& Step 4 TimeFraction: use a fraction of pi depending on the date time of the execution to hide it even better 
        #If this option is ativated (using 'y') it will leave one line with the current time of the execution
        s3contents = picover(s2contents)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
    
    #Delete temp files
    if os.path.isfile("timepi_decimals.txt"):
        os.remove("timepi_decimals.txt")

    if os.path.isfile("npi_decimals.txt"):
        os.remove("npi_decimals.txt")


    #Finalstep
    if output_mode == "write":
        try:
            # we create the output file and if time has been used  we just append the payload
            mode = 'a+' if Use_time else 'w+'
            with open(Outputfile,mode)as output_file:
                output_file.write(s3contents)
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
            sys.exit(1)
    elif output_mode == "return":
        return s3contents

if __name__ == "__main__":
    main()