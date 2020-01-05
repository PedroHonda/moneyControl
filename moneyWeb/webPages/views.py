from django.shortcuts import render

# Create your views here.
def mainPage_view(request, *args, **kwargs):
    return render(request, "webPages/industriousIndex.html", {})
