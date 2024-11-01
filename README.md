# insta-xhs-crawler
---
Automatically creating reels which contents from instagram


## 1. Prerequisites

### 1.1.Server Configurations
``` bash
sudo apt update
sudo apt upgrade
sudo apt install build-essential
sudo apt install libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev
sudo apt install libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev libffi-dev
sudo apt install ffmpeg firefox
sudo add-apt-repository ppa:mozillateam/ppa
```

### 1.2.pyenv
if you need multiple versions of python in your work, [pyenv](https://github.com/pyenv/pyenv)
could be a better option.
```bash
curl https://pyenv.run | bash
```
after the installation was successfully, you can install specific python version, just like
```bash
pyenv install 3.13.0
```

### 1.3.sqlite
```angular2html
sudo apt install sqlite3
```

## 2.Application Settings

### 2.1.Instagram settings
```angular2html
[insta]
# don't changed.
host = https://www.instagram.com
user_name = your_name
password = your_password
author = insta_author
```
### 2.2.Xiaohongshu settings

```bash
[xhs]
country=your_country_code
phone=your_phone_number
```

## 3.App Running Environments
### 3.1.create python interpreter
```bash
python3 -m venv .venv
source ./venv/bin/activate
```
### 3.2.install requirements
```bash
pip install -r requirements
```

## 4.Function Descriptions
###  4.1.download codes used for each post from instagram
when it is first time to run this app, the program will retrieve all posts of the instagram author. after then, the program only fetch incremental data. all posts will be saved into database and marked as download and published. Now, there is no any media files saved in local disk
### 4.2.Publish the post to the destination platform
Since xhs doesn't support multiple video files in one post, it is necessary to merge downloaded videos into one file, we are using ffmpeg for this merge process. the first time you run it, you need to enter the sms code sent from xhs platform which will be used for subsequent logins. The instagram author has been posted numerous works which saved in our database, so the publishing program only retrieves 2 items at a time. you can use crontab to automate the process.