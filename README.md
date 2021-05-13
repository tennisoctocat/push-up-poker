# Push-Up Poker

This code applies a filter of a playing card on people's foreheads in real time to a live incoming video feed. The filter tilts when the person's head is tilted, and is centered on their forehead, with the bottom of the card located at the top of their eyebrows. Eventually, I'd like to include this filter in a video-calling app that allows myself and my friends to virtually play a game called "push-up poker", where we put cards on our foreheads and bet pushups on who has the highest card.


## Running the Code

Create a python virtual environment.
```
$ python3 -m venv env_name
```
Activate your python virtual environment.
```
$ source env_name/bin/activate
```
Install the required packages.
```
$ pip install -r requirements.txt
```
Run the code.
```
$ python server.py
```
Navigate to the following link using your favorite browser. You may need to explicitly tell your browser that this is a safe url if it complains.

[http://127.0.0.1:8080](http://127.0.0.1:8080)

Click Start, and you'll see the filter!


## Details

The "training" folder contains "FacialFeatures.ipynb", which is the notebook file used for training the neural network used for finding facial features. To train the neural network, I used the [Facial Keypoints Detection](https://www.kaggle.com/c/facial-keypoints-detection/data) dataset from Kaggle. 
It also contains "sorting.py" and "valid.py", which I wrote for data cleaning. "is_valid.py" is the result of running the aforementioned two scripts on the Kaggle dataset, and contains a 1 for every row in csv that was part of my validation dataset, and a 0 elsewhere.

filter.py contains code that uses the neural network to apply the card filter to the incoming video feed.

index.html, server.py, and client.js were all adapted from the [aiortc server example](https://github.com/aiortc/aiortc/tree/main/examples/server), and use the [aiortc library](https://aiortc.readthedocs.io/en/latest/api.html) to take in incoming video frames from the client, process them, and then return the processed video frames.



## Credits

The code was adapted from the [aiortc server example](https://github.com/aiortc/aiortc/tree/main/examples/server).

The audio file "demo-instruct.wav" was in the original aiortc example. The creators of aiortc borrowed it from the Asterisk
project. It is licensed as Creative Commons Attribution-Share Alike 3.0:
https://wiki.asterisk.org/wiki/display/AST/Voice+Prompts+and+Music+on+Hold+License

Special thanks to Professor Rhodes and Professor Dodds of Harvey Mudd College for giving me advice and helping me resolve elusive bugs.
