# Lol Player Stats (EZ.GG)

![EZ.GG logo](https://github.com/Mikolaj-Mroz/Lol-Player-Stats/blob/main/app/static/meta/logo.png?raw=true)

## Table of contents

* [Introduction](#introduction)
* [Technologies](#technologies)
* [Setup](#setup)
* [How to use](#how-to-use)

## Introduction

The goal of this project is to recreate a [OP.GG](https://op.gg) website functionality. This web app gets data from RIOT GAMES API and parses it creating data models that can be used to analyze yours and your friends progress in League of Legends. You can check out the web app [here!](http://lol-stats.eu-central-1.elasticbeanstalk.com)

## Technologies

Project has been created using:

* Flask version: 2.1.3
* Flask-WTF version: 1.0.1
* Riotwatcher version: 3.2.3
* WTForms version: 3.0.1

## Setup

To run this project first install requirements.

```
$ pip install -r 'requirements.txt'
```

Next in the **stats.py** in the modules folder change api_key to your own API KEY

Then all you have to do is run flask application.

```
$ flask run
```

## How to use

### Get player data

To get player data all you need is to choose the server and write the player nickname in the search bar.

![EZ.GG search bar](https://i.ibb.co/tKxN1Wp/search-bar.png)

And here you go! You can see your match history with all the needed stats!

![EZ.GG search bar](https://i.ibb.co/M2m0CZ7/game-stats.png)
