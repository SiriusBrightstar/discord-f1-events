# F1 Next Event
A Python script that returns the next F1 Event

## Screenshot:
![Screenshot_1](https://github.com/SiriusBrightstar/f1-events/blob/main/Screenshots/F1_Bot.png)

## Steps to get this bot on your server:
- Create a bot using this guide: https://www.androidpolice.com/how-to-make-discord-bot/
- Clone this repo
```
git clone https://github.com/SiriusBrightstar/f1-events.git
cd f1-events/
nano src/auth.py
```
- Copy the Token from the Bot section and paste it in `/src/auth.py`
- Fill up all the variables on `/src/auth.py`
- Create docker image and run the container
```
sudo docker build . -t f1-events
sudo docker images
```
- Copy the Image ID
```
sudo docker run -d --restart always <PASTE DOCKER IMAGE ID HERE>
```

## Test without Docker:
- Clone this repo
```
git clone https://github.com/SiriusBrightstar/f1-events.git
cd f1-events/
```
- Install Python dependencies
```
pip3 install -r src/requirements.txt
```
- Fill up all the variables on `/src/auth.py`
```
nano src/auth.py
```
- Run the program
```
python3 src/main.py
```