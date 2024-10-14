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
In order to run the anylisis.py we need to specify 2 image files.  
Ideally an image altered with the steganography used in the project and the original file without any kind of payload embedded.  
The usage of analysis.py is:  
- General usage  
    - python3 analysis.py path/of/processedImage /path/of/original/image
- To replicate the data shown in the documentation  
    -  python3 analysis.py ./EvenLongerPayloadGhostwithFlower.png ./GhostWithFlower_original.png
    -  python3 analysis.py ./ShortPayloadGhostwithFlower.png ./GhostWithFlower_original.png

## Extracting the payload  
## Revealing the plaintext  

# Documentation  
Here is the documentation of the project together with a short description of what every team member has done for the project.  

We have divided the work by phases, Juan Trillo Carreras has been in charge of leading the project as well as creating the scripts of the payload creation and latter analysis of the results. However ,the ideas behind the payload creation were actually a group effort as a "brainstorming" process has been taken into consideration to have more than one steganography techinque.  

## Payload Creation (Done by Juan Trillo)
The payload used in this project is made by doing some modifications to a plaintext.  
Although only one step is actually procuring that the plaintext is actually secure,  
we use 3 different linguistic steganography techniques to hide that there even is a message (altogether of the latter technique of embedding this payload onto a .png file)

### Step 1 Cypher
We first cypher the contents of plaintext.txt

### Step 2 Base32(Linguistics)
We encode the ciphered text to base 32
and decode it to utf-8

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
Instead of using pi decimals we can also use a fraction of pi calculated with the date time of the execution to hide it even better   
being 0 = 0:00:00  
and 1 = 23:59:59  
s.t instead of the numbers used = 3.1415... is just 3.1415... * fraction_of_the_day resulting in e.g. 0.5438...

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
  
For replication, we have stored the program to extract this data (analysis.py) and 3 different images (Original, SP and ELP)  
statistics
extract payload
reveal plaintext


## Room improvement (Pier)
...

# Phases of the project

### Phase 1: Research 
Finished 29/09/2024  
Topics of research:  
- General steganography
- Steganography for pictures
- Png pictures structure
- Popular hiding techniques
- Python libraries for pngs

For the research phase we collected sources of information, made notes and summarized some articles and papers.   
### Phase 2: Crafting a payload
Finished 03/10/2024 (with some changes performed after that date -bug fixes, comments, and general improvements-)  

After the group made a brainstorming process of what steps should be taken to create the payload, Juan chose the different steps that should be carried out to craft the payload and created a script following said steps.  

### Phase 3: Embdeding of the payload to a .png
Finished 06/10/2024  

### Phase 4: Exctracting and revealing the plaintext from the .png
Finished: 13/10/2024


