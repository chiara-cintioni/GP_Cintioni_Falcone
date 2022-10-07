from django.shortcuts import render


# request made by who uses the website
# django.shortcuts la usiamo per prendere il file html richiesto
def home(request):
    return render(request, "home.html")

def contact(request):
    return render(request, "contact.html")

def help(request):
    return render(request, "documentation/help.html")

def sources(request):
    return render(request, "sources.html")

def info(request):
    return render(request, "info.html")

def download(request):
    return render(request, "download.html")

def search(request):
    return render(request, "search.html")
