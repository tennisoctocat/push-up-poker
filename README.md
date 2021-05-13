# Push-Up Poker

The idea of this project is to create a filter of a playing card on people's foreheads. The filter will tilt when the person's head is tilted, and be centered on their forehead, with the bottom of the card located at the top of their eyebrows. Eventually, I'd like to include this filter in a video-calling app that allows myself and my friends to virtually play a game called "push-up poker", where we put cards on our foreheads and bet pushups on who has the highest card.

The code was adapted from the [aiortc server example](https://github.com/aiortc/aiortc/tree/main/examples/server).

## Running the Code

Create a python virtual environment.
```
$ python3 -m venv /path/to/env_name
```
Run your python virtual environment.
```
$ source /path/to/env_name/bin/activate
```
Install the required packages.
```
$ pip install -r requirements.txt
```
Run the code.
```
$ python server.py
```
Navigate to the following link using your favorite browser.
```
[http://127.0.0.1:8080]([http://127.0.0.1:8080])
```
Click Start, and you'll see the filter!


## Credits

The code was adapted from the [aiortc server example](https://github.com/aiortc/aiortc/tree/main/examples/server).

The audio file "demo-instruct.wav" was in the original aiortc example. The creators of aiortc borrowed it from the Asterisk
project. It is licensed as Creative Commons Attribution-Share Alike 3.0:
https://wiki.asterisk.org/wiki/display/AST/Voice+Prompts+and+Music+on+Hold+License
