# nonestrap

Another NoneBot2 project bootstrap tool.

## Installation

Install nonestrap via this command:

```console
pip install nonestrap
```

## Usage

```console
# install bootstrap file into ./mybot/ with onebot-v11 adapter and without any
# extra plugin under a virtual environment.
nonestrap -a onebot-v11 mybot

# install bootstrap file into ./mybot/ with both onebot-v11 and ding adapter
# and APScheduler under a virtual environment
nonestrap -a onebot-v11 -a ding mybot nonebot-plugin-apscheduler

# same as the first one but with production .env file.
nonestrap -a onebot-v11 -e prod mybot

# same as the first one but without creating a new virtual environment.
# use it if you have already prepared a virtual environment.
nonestrap -a onebot-v11 -V mybot
```
