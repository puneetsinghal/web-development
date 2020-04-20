# web-development

This repository is build while going through Udacity course CS253. Follow these steps to set up everything in your system to run the codes.

## Download

Download this directory in your system. You can use terminal to clone this directory as
```
git clone https://github.com/puneetsinghal/web-development
```

## Google App Engine
* Initiate google cloud
```
gcloud init
```
* Deploy this project
```
gcloud app deploy
```
* access the website on your cloud server

## Running on local system

### Dependencies

#### Python 3
You need to have python3 and pip3 installed in your system

#### Virtual environment
It is advisable to use virtual environment for this project. Steps are:
* Install virtualenv using https://virtualenv.pypa.io/en/latest/installation.html
* Use terminal to go to this directory
* Create virtual environment for this project using this command in your terminal
```
virtualenv env
```
This will create a directory with name "env" under project directory. You can choose any other name instead of "env". It is advisable to create virtual environment directory under this project but you could have choosen any directory of your choice

#### Python packages
* Use terminal to go to this directory
* Activate the virtual env as
```
source env/bin/activate
```
Note: your path to activate file might be different based on your choices while creating virtual environment in previous step.
* Install python dependencies using this command in terminal
```
pip3 install -r requirements.txt
```

#### Run
In the terminal running virtual environment (as activate in previous step), run the main.py as:
```
python3 main.py
```
By default, this will start a server on localhost with port 4000.

#
