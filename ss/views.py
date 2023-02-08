from django.http import HttpResponse
from django.shortcuts import render
from .forms import UrlForm

# Create your views here.

def home(request):
    return HttpResponse("welcome")

def shorten(request):
    if request.method == "POST":
        urlForm = UrlForm(request.POST)
        if urlForm.is_valid():
            # ToDo: check security
            shortUrl = urlForm.save()
            id = shortUrl.id
            return render(request, "ss/url.html", {"url": shortUrl.url, "short":hash(id)})
        return render(request, "ss/shorten.html", {"form":urlForm})
    return render(request, "ss/shorten.html", {"form":UrlForm()})

def hash(id):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    shortUrl = ""
    while int(id):
        char = int(id%62)
        shortUrl = alphabet[char] + shortUrl
        id /= 62
    return shortUrl

def getId(shortUrl):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    id = 0
    base = 62
    reversedShortUrl = shortUrl[::-1]
    for idx, char in enumerate(reversedShortUrl):
        num = alphabet.index(char)
        id += num * pow(base, idx)
    return id
# print(hash(12345))
# print(getId("dnh"))