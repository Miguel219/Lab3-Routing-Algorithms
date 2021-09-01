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
The program will ask for your alumchat credentials and other needed data 