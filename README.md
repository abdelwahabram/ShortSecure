# ShortSecure
url shortening service that checks for url security

## Table of contents
* [Demo link](#demo-link)
* [About](#about-the-website)
* [Status](#status)
* [Technologies](#technologies)
* [Setup](#setup)

## Demo link:
https://2bdelwahab000.pythonanywhere.com/

## About the website:
this is a url shortener that makes sure the url is secure before processing it and before redirecting the user to the url using virus total api and prints the security report

### why this is useful? 
[read this article](https://www.cmu.edu/iso/aware/dont-take-the-bait/shortened-url-security.html#:~:text=Shortened%20URLs%2C%20such%20as%20those,software%20on%20to%20your%20device.)

## Status:
this is the initial version

the demo link is used to show the website functionality but it still needs a short descriptive domain name (to be done later)

## Technologies:
* Python
* Django
* Bootstrap
* Crispy forms
* HTML
* CSS
* virus total api

## Setup
* fork the repo
* go to the root directory
* run : 
```console
user:~$ python3 manage.py runserver
```
