from django.shortcuts import render

def landing_page(request):
    return render(request, 'home/index.html')

def smart_matching(request):
    return render(request, 'home/smart_matching.html')

def instant_messaging(request):
    return render(request, 'home/instant_messaging.html')

def verified_profiles(request):
    return render(request, 'home/verified_profiles.html')
