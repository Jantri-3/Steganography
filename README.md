# Steganography
Cybersecurity Overview Project Autumn 2024

# Problem statement (Pier)
This branch contains our attempt at building an all-in-one file that could prepare the payload and embed it into the file in one step. Unfortunately we couldn't complete this part, as for some reason there is a problem while reading the file containing the plaintext.
<br>If you look at payload_creation_embedding/payload.py, you can see that in the main function we open the text file received as an input, and after extracting its content we send it to the cypher function. At this point the program crashes, saying that the text file was not found. However, during the debugging, we saw that the program actually reaches that point, correctly opens the file and even prints its contents stored in the contents variable. For some reasons that we can't find though, once inside the cypher function this information is somehow lost, and trying to print the argument given as an input to cypher results in the program crashing and raising the file not found error. We still wanted you to read this part of our project, given the great amount of time we invested in it. 
<br>One other thing that I added to this branch was the stego_signatures file, which represents a better practice of how a global variable such as this one should be handled. Due to how the different parts of the project were developed separately, we couldn't do the same in the main branch, and had to resort to manually adding the strings in the two files where they were used, png_steganography.py and decoder.py.

# How to build
To resolve the dependencies and build the program you need to do the following steps:

- from the main folder, run
<code>python -m venv venv</code><br>This creates a virtual environment, which is a folder in the project that stores a few files and scripts.

- go to /venv/scripts and run
<code>activate</code><br> After this command, your shell should include (venv) at the beginning of the prompt.

- back to the main folder, run 
<code>pip install -e .</code> (don't forget the dot!) <br> This command will install the libraries and resolve the dependencies within the project files. It will also create the folder *.egg-info, which contains all the packages required for the project installation.

## How to run
<br>To run the program, you simply type
</br></br><code>python embed_payload/embed_all_in_one.py image_path plaintext_path [y/n]</code></br></br>
and this will produce a png image with the payload correctly embedded
NOTE: this is currently not working, but I'm working on it. The logic of the program should be correct,
but for some reason it doesn't find the plaintext.txt file.
