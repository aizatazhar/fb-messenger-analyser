# fb-messenger-analyser

Python script that analyses your Facebook messages and visualises the data as interactive and responsive HTML graphs using the Bokeh library.

## Example ##
![alt text](https://i.imgur.com/lNimwy5.jpg)
![alt text](https://i.imgur.com/Ro3Zyg9.jpg)
![alt text](https://i.imgur.com/iigCmcF.jpg)
![alt text](https://i.imgur.com/qcOpWpJ.jpg)

## Installation ##

**Requirements**
* [Python 3](https://docs.bokeh.org/en/latest/docs/installation.html)
* [Bokeh](https://docs.bokeh.org/en/latest/docs/installation.html)

**Setup**
1. [Download your Facebook messages](https://www.facebook.com/help/1701730696756992?helpref=hc_global_nav) in JSON format (may take a few hours to generate if you have a lot of messages). ![alt text](https://i.imgur.com/6y4lxN0.png)

2. [Download fb-messenger-script.py from this repo](https://github.com/aizatazhar/fb-messenger-analyser/archive/master.zip) and place the file in the same directory as the desired messages folder you downloaded from Facebook. The folder should contain message_1.json, message_2.json, etc. (each json file has 10000 messages). ![alt text](https://i.imgur.com/Fj2xo7E.png)

3. Run the script by cd-ing into the directory and running `python fb-messenger-script.py`. The Bokeh html files will be generated in the same folder.
