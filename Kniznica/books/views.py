from django.shortcuts import render
from django.http import HttpResponseRedirect
from pymarc import MARCReader
import subprocess


def index(request):
    logged = False
    user_name = ''
    if request.user.is_authenticated:
        logged = True
        user_name = request.user
    return render(request, 'books.html', {'logged': logged, 'user_name': user_name})


def show_books(request):
    with open('catalogue.dat', 'rb') as fh:
        reader = MARCReader(fh, to_unicode=True, force_utf8=True)
        for record in reader:
            print(record.title()[:-2])
    return HttpResponseRedirect('/detska-kniznica/books')


def get_books(request):
    with open('catalogue.dat', 'wb') as fh:
        fh.seek(0)
        fh.truncate()
        yaz = subprocess.Popen("yaz-client -m catalogue.dat", shell=True, stdin=subprocess.PIPE)
        result = yaz.communicate(b"open tcp:arl1.library.sk:8887")
    return HttpResponseRedirect('/detska-kniznica/books')