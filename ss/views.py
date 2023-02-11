from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .forms import UrlForm
from .models import Url
from decouple import config
import requests
import base64

# Create your views here.


def home(request):
    return HttpResponse("welcome")


def shorten(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            urlObject = Url(user=request.user, session=request.session.session_key)
        else:
            request.session.save()
            print(request.session.session_key)
            urlObject = Url(session=request.session.session_key)
        urlForm = UrlForm(request.POST, instance=urlObject)
        if urlForm.is_valid():
            url = urlForm.cleaned_data["url"]
            result = isSecure(url)
            vendors, status = result[0], result[1]
            if status:
                shortUrl = urlForm.save()
                id = shortUrl.id
                return render(request, "ss/url.html", {"url": shortUrl.url, "short": hash(id)})
            return render(request, "ss/security.html", {"url": url, "shorten": True, "secure": status, "vendors": vendors})
        return render(request, "ss/shorten.html", {"form": urlForm})
    return render(request, "ss/shorten.html", {"form": UrlForm()})


def redirectUrl(request, short):
    id = getId(short)
    url = get_object_or_404(Url, id=id)
    result = isSecure(url.url)
    vendors, status = result[0], result[1]
    return render(request, "ss/security.html", {"url": url.url, "secure": status, "vendors": vendors})


def hash(id):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    shortUrl = ""
    while int(id):
        char = int(id % 62)
        shortUrl = alphabet[char-1] + shortUrl
        id /= 62
    return shortUrl


def getId(shortUrl):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    id = 0
    base = 62
    reversedShortUrl = shortUrl[::-1]
    for idx, char in enumerate(reversedShortUrl):
        num = alphabet.index(char) + 1
        id += num * pow(base, idx)
    return id


def isSecure(url):
    url_id = base64.urlsafe_b64encode(f"{url}".encode()).decode().strip("=")
    api = config('api')
    url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
    headers = {
        "accept": "application/json",
        "x-apikey": api
    }
    response = requests.get(url, headers=headers)
    res = response.json()
    vendors = res['data']['attributes']['last_analysis_results']
    status = True
    for vendor in vendors:
        if vendors[vendor]['result'] == 'malicious':
            status = False
    return [vendors, status]
