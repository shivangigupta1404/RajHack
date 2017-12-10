from __future__ import print_function
from django.shortcuts import render,get_object_or_404, redirect, render_to_response
from django.http import HttpResponse,Http404,HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from sfg.feeds import *
from sfg.forms import SignUpForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
import json,requests,uuid
from django.core import serializers

import csv
from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import LinearSVC
import pandas
from sklearn import svm


#miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"
#..................Login..................

def ocr_file(filename, overlay=False, api_key='61a8cd0dbb88957', language='eng'):
    """ OCR.space API request with local file.
      Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                  Defaults to False.
    :param api_key: OCR.space API key.
                  Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                  List of available language codes can be found on https://ocr.space/OCRAPI
                  Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
    }
    filename=filename.replace('%20',' ')
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',files={filename: f},data=payload,)

    result=r.content.decode()
    try: #for python 2.7
        result.decode("utf-8")
    except:
        pass

    result=json.loads(result)
    return result['ParsedResults'][0]['ParsedText']

def log(request):
    if 'username' in request.session:
        return HttpResponseRedirect('/sfg/dashboard/')
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
        return HttpResponseRedirect('/sfg/dashboard')
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
    print ("User: " + received_json_data['user'])
    print ("Image: " + received_json_data['image'][0:10])
    image=received_json_data['image']
    #image= b'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AwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/aAAwDAQACEQMRAD8A/fyiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKrXd1BY6bcXl3NHb2sETSzSucKiKCWYn0ABNA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mkIBX9vVG1cDoOlGMUtABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAH//Z'
    unique_filename = 'media/'+str(uuid.uuid4())+".jpg"
    with open(unique_filename, "wb") as fh:
        fh.write(image.decode('base64'))
    file_text = ocr_file(filename=unique_filename)
    return JsonResponse({"User":received_json_data['user'], "Image": received_json_data['image'],"filename":unique_filename,"text":file_text})
    #return render(request, 'sfg/home.html')

@login_required
def dashboard(request):
    return render(request, 'sfg/home.html',{'user':request.user.username})
@login_required
def view_chain(request):
    uname = User.objects.get(username=request.user.username)
    #print(uname)

    if uname.block_set.all:
        object_list = serializers.serialize("python", uname.block_set.all())
        #print(object_list)
        #prediction_model()
        #print(uname.block_set.all)
        for block in object_list:
            for txt,val in block.items.fields():
                print(txt)
                if(txt=='fields'):
                    for k,v in txt:
                        if k=='text':
                            print("hh")
                    #string+=val;

    return render(request,'sfg/view_chain.html',{'user':uname})

@login_required
def add_block(request):
    try:    #for python 2.7
        import sys
        reload(sys)
        sys.setdefaultencoding('utf8')
    except:
        pass
    if request.method == 'POST' and request.FILES['myfile']:
        title=request.POST.get("caption")
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        print (myfile.name)
        unique_filename = str(uuid.uuid4())+'.jpg'
        filename = fs.save(unique_filename, myfile)
        uploaded_file_url = fs.url(filename)
        file_text = ocr_file(filename=uploaded_file_url[1:])
        username = request.user.username
        data={'title':title,'image':uploaded_file_url,'text':file_text,'user':username}
        blockchain.add_block(data)
        return render(request, 'sfg/home.html', {'uploaded_file_url': uploaded_file_url,'file_text':file_text})
    return render(request, 'sfg/new_block.html')

clf=svm.SVC()
def prediction_model():
    filename='sfg/trainLabels.csv'
    names=['image','level']
    data = pandas.read_csv(filename, names=names)
    #print data
    im=data.image
    image=im.values.reshape(-1, 1)
    X, y = image, data.level

    clf.fit(X, y)

#def predict_user(request):

    #print clf.predict(request.data)
