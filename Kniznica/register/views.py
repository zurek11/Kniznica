from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render
from definitions import SITE_ROOT
from . import inputForms
from threading import Thread
import base64
import re
import os


def index(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'NewUser': inputForms.NewUser})
    else:
        return HttpResponseRedirect('/')


def new_user(request):
    if request.method == 'POST':
        form = inputForms.NewUser(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_email = form.cleaned_data['email']
            user_password1 = form.cleaned_data['password1']
            thread = Thread(target=save_user, args=(form, user_name))
            thread.start()
            user_instance = User.objects.create(username=user_name, email=user_email, password=user_password1)
            user_instance.set_password(user_instance.password)
            user_instance.save()
            request.session.set_expiry(86400)  # sets the exp. value of the session
            login(request, user_instance)  # the user is now logged in
            return HttpResponseRedirect('/detska-kniznica')
        else:
            print(form.errors)
            return render(request, "register.html", {'NewUser': form})


def save_user(form, user_name):
    base_to_png(form.cleaned_data['pic1'], user_name, "face1.png")
    base_to_png(form.cleaned_data['pic2'], user_name, "face2.png")
    base_to_png(form.cleaned_data['pic3'], user_name, "face3.png")
    base_to_png(form.cleaned_data['pic4'], user_name, "face4.png")
    base_to_png(form.cleaned_data['pic5'], user_name, "face5.png")


def base_to_png(base64_string, name, image_name):
    string_without_header = re.sub('^data:image/.+;base64,', '', base64_string)
    img_data = base64.b64decode(string_without_header)
    if not os.path.exists(SITE_ROOT + "/faceId/" + name):
        os.makedirs(SITE_ROOT + "/faceId/" + name)
    filename = SITE_ROOT + "/faceId/" + name + "/" + image_name
    with open(filename, 'wb') as f:
        f.write(img_data)
    os.chdir(SITE_ROOT + "/static/scripts")
    os.system("node face-detection.js " + name + " " + image_name)
