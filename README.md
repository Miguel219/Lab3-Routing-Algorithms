# Lab3-Routing-Algorithms

## Installation

To install the required libraries you can run the following comands:
```
    pip install slixmpp
    pip install aioconsole
    pip install pandas
    pip install numpy
```

## For Flooding

If you want to write a message you must run it like this:
```
  python main.py -j <JID> -p <Password> -r "flooding"
```
There you will be asked the recipient JID and message, after that you can only listen. 
If you want to write other message, kill the script and run it again
  
If you want to listen, and just listen:
```
  python main.py -j <JID> -p <Password> -r "flooding" -t true
```

## For LSR

To run the link state rounting client move to the LSR directory and run:
```
    python lsr.py 
```
The program will ask for your alumchat credentials and other needed data like the paths for the topo file and the names file


## For DVR
First you have to replace "topo-demo.txt" and "names-demo.txt" files in main directory.
To run the distance vector rounting client move to the dvr directory and run:
```
    python main.py 
```
The program will ask for your alumchat credentials to login.
