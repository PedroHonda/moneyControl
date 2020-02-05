from django.shortcuts import render
from moneyDatabase.models import StockBuying, StockSelling, FixedBuying, FixedSelling, REIFBuying, REIFSelling, Current, Taxes, Brokers

# Create your views here.
def mainPage_view(request, *args, **kwargs):
    return render(request, "webPages/index.html", {})

def settings_view(request, *args, **kwargs):
    return render(request, "webPages/settings.html", {})

def stock_view(request, *args, **kwargs):
    return render(request, "webPages/stock.html", {'heading': 'Stock'})
