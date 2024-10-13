# Steganography
Cybersecurity Overview project 2024

# Problem statement


# How to use 
First of all please, do $pip install -r requirements.txt  

## Creating the payload
In order to run the payload creation you will need to:
- add the message you want to hide in "payload_creation/plaintext.txt"  
- add the public key of the receiver of the message as "payload_creation/public_key.pem"
- finally run payload.py 

The usage of payload.py is:  
- For the normal use:  
    - python3 payload.py plaintext.txt  
- For the use including the time (include step4):  
    - python3 payload.py plaintext.txt y  

The result will be stored in payload.txt  

## Payload embedding  
## Statistics  
## Extracting the payload  
## Revealing the plaintext  

# Documentation  
## Payload Creation (Done by Juan Trillo)

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
cover + string  
...  


### Step 4 TimeFraction: 
use a fraction of pi depending on the date time of the execution to hide it even better   
being 0 = 0:00:00  
and 1 = 23:59:59  
If this option is ativated (using 'y') it will leave one line in the payload.txt with the current time of the execution to hide it in the metadata  


## Embedding paylaods into images


### Quick analysis of the modifications made to the images: (Done by Juan Trillo)
For checking how the image behaves depending on the payload embedded, we have modified the same image embedding it with 3 different  payloads a short one of 2000 characters and a longer one with 8.240 characters  and the even longer with 32.800 chars.  
We have first checked the original png LSB 0’s and 1’s  

- 🟢Original image🟢  
    - Original number of 0's= 174887  
    - Original number of 1's= 231103  
    - Total number of 0's+1's befroe processing: 405990  
    - Percentage of 0's 43.07667676543757%  
    - Percentage of 1's 56.92332323456243%  
- 🟡Image embedded with short payload (SP)🟡  
    - Processed number of 0's= 173169  
    - Processed number of 1's= 232821  
    - Total number of 0's+1's after processing: 405990  
    - Percentage of 0's 42.65351363334072%  
    - Percentage of 1's 57.34648636665928%  
- 🟠Image embedded with long payload (LP)🟠  
    - Processed number of 0's= 169647  
    - Processed number of 1's= 236343  
    - Total number of 0's+1's after processing: 405990  
    - Percentage of 0's 41.786004581393634%  
    - Percentage of 1's 58.213995418606366%  
- 🔴Even longer payload (ELP)🔴  
    - Processed number of 0's= 183493  
    - Processed number of 1's= 222497  
    - Total number of 0's+1's after processing: 405990  
    - Percentage of 0's 45.196433409689895%  
    - Percentage of 1's 54.803566590310105%  
  
After a comparison we can see that this modifications tended to make the difference between images (0’s and 1’s change even more)  
🟢Original = 43/56.9 ratio  
🟡SP = 42.65/57.34 ratio  
🟠LP = 41.78/58.21 ratio  
However for a really big payload this ratio was drastically reduced  
🔴ELP = 45.19/54.80  
Still far from a 50/50 ratio but still not a really significant change from the original image  
form 43 to 45.2 and from 56.9 to 54.8  
  
We could say that the embedded png will change their distribution not more than a 3% even in extreme cases (as a non existent payload will result in no change at all in the distribution)  
  
For replication, we have stored the program to extract this data (NormalDistributionCheck.py) and 3 different images (Original, SP and ELP)  
statistics
extract payload
reveal plaintext







### Room improvement (Pier)
...