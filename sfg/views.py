#from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404, redirect, render_to_response
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from sfg.feeds import *
from sfg.forms import SignUpForm
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

#miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"
#..................Login..................

def log(request):
    if 'username' in request.session:
        return HttpResponseRedirect('/sfg/home/')
    else:
        context = {
        }
        return render(request,'sfg/login.html',context)

def login_next(request):
    name = request.POST.get('name', None)
    pwd = request.POST.get('pwd', None)
    try:
        user = authenticate(username=name, password=pwd)
    except KeyError:
        return render(request, 'sfg/login.html', {'login_message' : 'Fill in all fields'})
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/sfg/home')
    else:
        try:
            del request.session['username']
        except KeyError:
            return render(request, 'sfg/login.html', {'login_message' : 'Invalid Username or Password'})
        return HttpResponseRedirect('/sfg/')

def log_end(request):
    logout(request)
    return HttpResponseRedirect('/sfg/')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            email = form.cleaned_data['email']
            password = form.cleaned_data.get('password1')
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            return redirect('log')
    else:
        form = SignUpForm()
    context = {
        'form':form,
    }
    return render(request, 'sfg/signup.html',context)

#..................................................
@csrf_exempt
def apiAddBlock(request):
    received_json_data=json.loads(request.body.decode("utf-8"))
    #print received_json_data
    print "User: " + received_json_data['user']
    print "Image: " + received_json_data['image'][0:10]
    return JsonResponse({"User":received_json_data['user'], "Image": received_json_data['image']})

def transaction(request):
	if request.method == 'POST':
	    data = request.POST.get("data")
	    blockchain.add_block(data)
	    print ("New transaction"+data)
	    print (blockchain.chain)
	return render(request,"sfg/home.html",{})
