from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from definitions import SITE_ROOT
from . import inputForms
from django.contrib.auth.models import User
import subprocess
import base64
import re
import os
import logging


def index(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'LogUser': inputForms.LogUser})
    else:
        return HttpResponseRedirect('/')


def log_user(request):
    if request.method == 'POST' and 'btn_login_camera' in request.POST:
        form = inputForms.LogUser(request.POST)
        if form.is_valid():
            picture = form.cleaned_data['pic1']
            user_name = prepare_log_img(picture)
            user = User.objects.get(username=user_name)
            request.session.set_expiry(86400)  # sets the exp. value of the session
            login(request, user)  # the user is now logged in
            return HttpResponseRedirect('/detska-kniznica')
        else:
            logging.error(form.errors)
            return HttpResponseRedirect('/detska-kniznica')
    elif request.method == 'POST' and 'btn_login' in request.POST:
        form = inputForms.LogUser(request.POST)

        if form.is_valid():
            user = form.login(request)
            if user:
                request.session.set_expiry(86400)  # sets the exp. value of the session
                login(request, user)  # the user is now logged in
                return HttpResponseRedirect('/detska-kniznica')
            else:
                logging.error(form.errors)
                return render(request, "login.html", {'LogUser': form})
        else:
            logging.error(form.errors)
            return render(request, "login.html", {'LogUser': form})
    else:
        logging.error("Bad request in login.")
        return HttpResponseRedirect('/detska-kniznica')


def log_out_user(request):
    logout(request)
    return HttpResponseRedirect('/detska-kniznica')


def prepare_log_img(picture):
    string_without_header = re.sub('^data:image/.+;base64,', '', picture)
    img_data = base64.b64decode(string_without_header)
    filename = SITE_ROOT + "/faceId/logged.png"
    with open(filename, 'wb') as f:
        f.write(img_data)
    os.chdir(SITE_ROOT + "\static\scripts")
    os.system("node face-detection.js logged.png")
    p = subprocess.Popen("node face-recognition.js", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    output = str(output)
    return output[output.find("'") + 1:output.rfind("'")]
