from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StockForm
import requests, json
import pyEX as p
# Create your views here.
from .models import Stocks
c = p.Client(api_token=TOKEN)

def home(request):
    # pk_921fc8e4cab149df9532177da6cb3f71
    if request.method == "POST":
        ticker = request.POST["ticker"]
        api = c.chartDF(ticker)
    else:
        return render(request, 'home.html', {"api": "Enter ticker above"})

    return render(request, 'home.html', {"api":api.head(1),"ticker":ticker})

def about(request):
    return render(request, 'about.html', {})

def add_stocks(request):
    if request.method == "POST":
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request,"Stock has been added")
            return redirect("add_stocks")
    else:
        pass

    ticker = Stocks.objects.all()
    return render(request, 'add_stocks.html', {"ticker":ticker})

def del_stocks(request, stock_id):
    item = Stocks.objects.get(pk = stock_id)
    item.delete()
    messages.success(request,"deleted stock {}".format(stock_id))
    return redirect(add_stocks)