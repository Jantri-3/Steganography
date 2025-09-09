# Steganography
Cybersecurity Overview (DD2391) Project - Autumn 2024  
KTH Royal Institute of Technology  
**Team:**
- Juan Trilo Carreras
- Nils Eric Jordan
- Miguel Coelho

# Problem statement
Traditional data protection using encryption is effective, but it draws attention to the existence of a hidden message. Using an approach like steganography with the Least Significant Bit (LSB) technique in combination with encryption ensures to obscure the content of the message and aswell its existence.

## Challenges
**Evolving threat landscape:** Nowadays data breaches and unauthorized access to information is common. The number of cyber attacks is constantly increasing, often resulting in high reputational and financial damage. Therefore it is crucial to take security measures to protect confidential information.

**Visibility of encryption:** Encrypion provides an important basis for secure transmission of data. Nevertheless, the presence of encrypted data is often a sign that sensitive information is being transmitted, which motivates an attacker to further analyse and possibly attack this communication.

**Covert communication:** Individual who are involved in activities such as whisteblowing or activism need methods to communicate discreetly. This means that they need techniques not only to encrypt messages, but also to hide that information are being transmitted.

## Solution
Our solution uses secure public-key encryption to protect the information. Afterwards, the encrypted information gets encoded using Base32 to further obscure the content of the message. By embedding the result in random strings based on the decimals of PI, the message is altered in a pseudo-random manner before being embedded into an image using the LSB technique. Overall, this approach ensures confidentiality and hides the transmission of information using steganography. The additional layers of obfuscation help to protect the encrypted information even if a transmisison of data is noticed.

# How to use 
To set up the project environment, please run the following command to install the necessary packages:

`pip install -r requirements.txt`

## Creating the payload
In order to run the payload creation you will need to:  
- add the message you want to hide in "payload_creation/plaintext.txt"  
- add the public key of the receiver of the message as "payload_creation/public_key.pem"
- finally run payload.py 

The usage of payload.py is:    
- For the normal use:  
    - `python3 payload.py plaintext.txt`  
- For the use including the time (include step4):  
    - `python3 payload.py plaintext.txt y`

The result will be stored in payload.txt  

## Embedding the payload
To embed a created payload into a picture you have to pass a payload as a .txt file and a .png image shown as follows:

`python3 png_steganography.py /path/to/payload /path/to/image`

The picture with the embedded payload will be stored in the current working directory.

## Statistics  
In order to run the analysis_of_images.py we need to specify 2 image files.  
Ideally an image altered with the steganography used in the project and the original file without any kind of payload embedded.  
The usage of analysis_of_images.py is:  
- General usage  
    - `python3 analysis_of_images.py path/of/processedImage /path/of/original/image`
- To replicate the data shown in the documentation  
    -  `python3 analysis_of_images.py ./EvenLongerPayloadGhostwithFlower.png ./GhostWithFlower_original.png`
    -  `python3 analysis_of_images.py ./ShortPayloadGhostwithFlower.png ./GhostWithFlower_original.png`

## Retrieving the message (or, doing the reverse process)
To reverse the process described above (creating a payload and embedding it into an image), execute the following commands:
   - `python3 decoder.py /path/to/embedded_image.png`

Make sure to include the necessary private key (for decryption purposes) in the private_key.pem file, located in the extract_message folder.

Please note that this process will only work if:
   - the filename in question corresponds to a .png file;
   - the referred file can be open and read;
   - there is a valid payload embedded in the refered file;
   - there is a suitable private key in the private_key.pem file;
   - the provided private key matches the public key used to initially encrypt the payload in question;

# Documentation 
Here is the documentation of the project together with a short description of what every team member has done for the project.  

We have divided the work by phases, Juan Trillo Carreras has been in charge of leading the project as well as creating the scripts of the payload creation and latter analysis of the results. However, the ideas behind the payload creation were actually a group effort as a "brainstorming" process has been taken into consideration to have more than one steganography techinque.  

## Payload Creation (Done by Juan Trillo)
The payload used in this project is made by doing some modifications to a plaintext.  
Although only one step is actually procuring that the plaintext is actually secure,  
we use 3 different linguistic steganography techniques to hide that there even is a message (altogether of the latter technique of embedding this payload onto a .png file)

### Step 1: Cypher
We first cypher the contents of plaintext.txt using RSA

<code>ciphertext = public_key.encrypt(contents.encode(),padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))</code>

We are using Optical Assymetric Encryption Padding (Padding scheme to assure randomness -this padding is not deterministic-)  
`mgf=padding.MGF1(algorithm=hashes.SHA256())`  
MGF1 (Mask Generation Function 1):   
Is a cryptographic function used in conjunction with OAEP which will generates a mask (sequence of bytes used to randomize the encryption)  
`hashes.SHA256(): `
This means that we are using SHA256 in the MGF
`algorithm=hashes.SHA256()`
We are ensuring SHA256 is the main hashing function used in the OAEP


### Step 2: Base32 (Linguistics)
We encode the ciphered text to base 32
and decode it to utf-8

### Step 3: Pi (Linguistics)
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


### Step 4: TimeFraction: 
Instead of using pi decimals we can also use a fraction of pi calculated with the date time of the execution to hide it even better   
being 0 = 0:00:00  
and 1 = 23:59:59  
s.t instead of the numbers used = 3.1415... is just 3.1415... * fraction_of_the_day resulting in e.g. 0.5438...

If this option is ativated (using 'y') it will leave one line in the payload.txt with the current time of the execution to hide it in the metadata  

## Payload Embedding (Done by Nils Jordan)
To embed a created payload into an .png image, the Least-Significant-Bit (LSB) technique is used. The program sequence is as follows:

1. Processing the input of the user
   - Checking for the appropiate amount of arguments
   - Checking for the appropiate file types
   - Checking for the appropiate order of arguments
2. Loading the provided image from the provided path
3. Loading the provided payload from the provided path
4. Embedding the payload into the image using the LSB technique
   - Checking if the payload fits into the image before embedding
5. Saving the modified image to the current working directory

### Least-Significant-Bit (LSB) technique
When LSB is used the embedding process consists of changing the least significant bits of pixels. This means that a pixel only changes very slightly in its color, but this change cannot be recognized by the human eye when a original image and a modified image is compared (Mandal, P. et al., 2022). An example illustrates the process:

**Original pixel:** `RGB = (10101100, 11010110, 01101101)` **Payload:** `01000001`

As described LSB changes the least significant bits of a pixel.

**Red:** `10101100` → `10101100` | No changes

**Green:** `11010110` → `11010111` | The last bit was changed from 0 to 1 

**Blue:** `01101101` → `01101100` | The last bit was changed from 1 to 0 

The result of applying LSB is a slightly modified pixel.

**Modified pixel:** `RGB = (10101100, 11010111, 01101100)`

LSB has the advantages that the it does not require a lot of computation power and that it can be integrated into other methods. Unfortunately LSB decreases the image quality and statistical analysis is a powerful technique to discover the application of the LSB technique. Nowadays LSB is focussed on embedding capacity rather than security, but several modifications of the LSB technique exist. There are also correction methods which can be used to improve the image quality when the LSB technique is applied (Mandal, P. et al., 2022).

### Quick analysis of the modifications made to the images (Done by Juan Trillo)
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
  
For replication, we have stored the program to extract this data (analysis_of_images.py) and 3 different images (Original, SP and ELP)  

## Payload Extraction (Done by Pier Paolo Penna)
This step involves, given a PNG image as the input, the detection and extraction of an embedded message within the file. The first step before extracting though, is having the program understand whether or not there is a message to be extracted to begin with. In order to achieve this, I thought of creating two strings, namely stegoSignature and stegoKey, made up of random characters. This was both to ensure an almost inexistent chance of false positives, while at the same time not looking suspicious if extracted from a third party, which would just see a bunch of gibberish letters. I added these two strings to the payload embedding part, as the beginning and the end of the embedded message. <br>Once the message is encoded in the image, the extraction follows three steps:

1. Determine if the image given in input contains the stegoSignature as the beginning of the message. This ensures that we only extract messages from images that do contain them.
2. If the image is a stego medium, we proceed with the payload extraction. This operation is performed by using the bitwise and operator, confronting the bytes of the image with the byte <code>00000001</code>, which results in extracting the last bit of the byte passed in the input, thus revealing the embedded message.
3. The last step was looking for the stegoEnd in order to stop the payload extraction. This operation was performed using a string buffer that contained the last extracted bits for the size of the stegoEnd. At every step we would confront the stegoEnd and the current buffer, interrupting execution once they match. Again, the randomness and length of the stegoEnd string ensures a negligible false positive rate.

## Payload Decoding (Done by Miguel Coelho)
Just as payload extraction is the inverse of payload embedding, payload decoding is the inverse of payload creation: to accomplish this task, the script will walk back through the steps taken in payload creation in reverse. Starting with a payload string delivered by the previous stage of the script, the steps to take are as follows:

1. Determine whether time-based encoding was used (or, in other words, whether the constant used to cloak the payload in random characters is pi or not);
   - With the current setup, this is determined by simply looking at the start of the payload. If time-based encoding is used, the payload will include a "timestring" (e.g.: TIME 19:09:14) in the very beginning; if not, no such string will be found.
2. Retrieve the characters belonging to the actual payload (or, discarding the junk characters used for obfuscation);
   - As described in "Payload Creation", this obfuscation technique depends on an auxiliary constant (c), which is calculated as follows:
      - If time-based encoding is used, c = (timestring_as_seconds/24*3600) * pi
      - Otherwise, c = pi
   - The decimal digits of this constant are then interpreted as the indexes of the characters pertaining to the actual payload in the provided payload string (e.g.: if the first decimal digit of our constant is 2, then the first character of the actual payload resides at input_string[2]).
   - Knowing that the input_string can be cleanly divided into 10 character long chunks, with each chunk containing exactly one character of the actual payload, we can systematically extract all the right characters, one chunk at a time.
3. Reverse the base32 encoding step (Step 2 of Payload Creation);
4. Reverse the encryption technique used to cypher the initial plaintext into ciphertext (Step 1 of Payload Creation) using a user-provided matching private key (found in "./private_key.pem") in PEM format.


## Room improvement (Pier)
This section describes the steps taken for improving the program in a UX sense.
Disclaimer: unfortunately, this part of the project didn't seem to work properly, as there were some errors in locating the plaintext file from its path. You'll read this issue in more detail in the branch where this improvement is written, as we couldn't merge the two projects.
<br>The general idea is that a user would input the plaintext and the image in which to hide the message, rather than manually crafting the encrypted payload and subsequently insert it into the image. With this in mind, we created a file named embed_all_in_one.py that serves this exact purpose, being a unique launcher for the first half of our program, invoking the functions for both the payload creation and its embedding.
<br>One other thing that I added was a stego_signatures file, that contains two strings that we used as identifiers to mark the beginning and the end of the encrypted message, as they were necessary for payload extraction.
You will find more details of the whole process in the README.md file of the other branch, including instructions on how to build the project with another method.

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
Finished: 03/10/2024 (with some changes performed after that date -bug fixes, comments, and general improvements-)  

After the group made a brainstorming process of what steps should be taken to create the payload, Juan chose the different steps that should be carried out to craft the payload and created a script following said steps.  

### Phase 3: Embdeding of the payload to a .png
Finished: 06/10/2024
- Bug fixes, comments and improvements performed after that date

### Phase 4: Extracting the payload from the .png and revealing the original message
Finished: 13/10/2024 (with minor changes such as bug fixes, improved error handling, etc... made afterwards)

- Work on the decoder.py script began on 10/10/2024;
- The section "decode_payload" was finished by 10/10/2024;
- The section "extract_payload" was finished by 13/10/2024;

# References
Mandal, P. et al. (2022) 'Digital Image Steganography: A Literature Survey', Information Sciences, 609, pp. 1451-1488. [doi:10.1016/j.ins.2022.07.120](https://doi.org/10.1016/j.ins.2022.07.120).
