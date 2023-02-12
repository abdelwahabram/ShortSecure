from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .forms import UrlForm, UserRegistrationForm
from .models import Url
from decouple import config
import requests
import base64
from django.contrib.auth import login

# Create your views here.


def home(request):
    return HttpResponse("welcome")


def register(request):
    if request.method == "POST":
        newUserForm = UserRegistrationForm(request.POST)
        if newUserForm.is_valid():
            saveSession = newUserForm.cleaned_data["saveSession"]
            newUser = newUserForm.save()
            login(request, newUser)
            if "urls" in request.session and saveSession:
                id_list = request.session["urls"]
                Url.objects.filter(id__in=id_list).update(user=request.user)
            return redirect("home")
        return render(request, "registration/register.html", {"form": newUserForm})
    return render(request, "registration/register.html", {"form": UserRegistrationForm()})


def shorten(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            urlObject = Url(user=request.user)
        else:
            urlObject = Url()
            if "urls" not in request.session:
                request.session["urls"] = []
        urlForm = UrlForm(request.POST, instance=urlObject)
        if urlForm.is_valid():
            url = urlForm.cleaned_data["url"]
            result = isSecure(url)
            vendors, status = result[0], result[1]
            if status:
                shortUrl = urlForm.save()
                id = shortUrl.id
                if not request.user.is_authenticated:
                    request.session["urls"] += [id]
                return render(request, "ss/url.html", {"url": shortUrl.url, "short": hash(id)})
            return render(request, "ss/security.html", {"url": url, "shorten": True, "secure": status, "vendors": vendors})
        return render(request, "ss/shorten.html", {"form": urlForm})
    return render(request, "ss/shorten.html", {"form": UrlForm()})


def redirectUrl(request, short):
    id = getId(short)
    url = get_object_or_404(Url, id=id)
    if url.status:
        result = isSecure(url.url)
        vendors, status = result[0], result[1]
        return render(request, "ss/security.html", {"url": url.url, "secure": status, "vendors": vendors})
    return redirect("home")#, message="url isn't active")


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
