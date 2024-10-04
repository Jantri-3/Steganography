# Steganography
Cybersecurity Overview project 2024

## Payload Creation

### Step 1 Cypher
We first cypher the contents of plaintext.txt

### Step 2 Base32(Linguistics)
We encode the ciphered text to base 32

### Step 3 Pi(Linguistics)
We use pi decimals to "cover" the base 32 which means:  
imagine pi = 3.1416...  
and base32 decoded to string = Hola  

cover = ""  

We create a random string ABCDEFGHIJ  
we see the firt pi decimal = 1  
in pos 1 we write 'H' s.t the string is AHCDEFGHIJ  
cover+string  
then for the next char  
another random string 1234567890  
next pidecimal = 4  
in pos 4 we write 'o'  
1234o67890  
cover+ string  
...  


### Step 4 TimeFraction: 
use a fraction of pi depending on the date time of the execution to hide it even better   
being 0 = 0:00:00  
and 1 = 23:59:59  
If this option is ativated (using 'y') it will leave one line in the payload.txt with the current time of the execution to hide it in the metadata  

In order to run the payload creation you will need to add the message in "plaintext.txt", add to the /Payload-Creation the public key of the receiver of the message with the name "public_key.pem",and finally run payload.py.   
The usage of payload.py is :  
    For the normal use:  
        payload.py plaintext.txt  
    For the use including the time (include step4):  
        payload.py plaintext.txt y  

 The result will be stored in payload.txt
