from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse

import json
from feeds import *

miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

def transaction(request):
	if request.method == 'POST':
	    data = request.POST.get("data")   
	    Blockchain.add_block(data)

	    print "New transaction"+data
	    print Blockchain.chain
	return render(request,"sfg/index.html",{})