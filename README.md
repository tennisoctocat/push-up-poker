# Push-Up Poker

The idea of this project is to create a filter of a playing card on people's foreheads. The filter will tilt when the person's head is tilted, and be centered on their forehead, with the bottom of the card located at the top of their eyebrows. Eventually, I'd like to include this filter in a video-calling app that allows myself and my friends to virtually play a game called "push-up poker", where we put cards on our foreheads and bet pushups on who has the highest card.

The code was adapted from the [aiortc server example](https://github.com/aiortc/aiortc/tree/main/examples/server).

## Running the Code

Create a python virtual environment using ```$ python3 -m venv /path/to/env_name```
Run your python virtual environment using `$ source /path/to/env_name/bin/activate`.
Install only the required packages (and the required versions of the required packages) using `$ pip install -r requirements.txt`.
Run the code using `$ python server.py`.



-------

First install the required packages:

.. code-block:: console

    $ pip install aiohttp aiortc opencv-python

When you start the example, it will create an HTTP server which you
can connect to from your browser:

.. code-block:: console

    $ python server.py

You can then browse to the following page with your browser:

http://127.0.0.1:8080

Once you click `Start` the browser will send the audio and video from its
webcam to the server.

The server will play a pre-recorded audio clip and send the received video back
to the browser, optionally applying a transform to it.

In parallel to media streams, the browser sends a 'ping' message over the data
channel, and the server replies with 'pong'.

Additional options
------------------

If you want to enable verbose logging, run:

.. code-block:: console

    $ python server.py -v

## Credits

The code was adapted from the [aiortc server example](https://github.com/aiortc/aiortc/tree/main/examples/server).

The audio file "demo-instruct.wav" was in the original aiortc example. The creators of aiortc borrowed it from the Asterisk
project. It is licensed as Creative Commons Attribution-Share Alike 3.0:
https://wiki.asterisk.org/wiki/display/AST/Voice+Prompts+and+Music+on+Hold+License
