from django.shortcuts import render


def index(request):
    logged = False
    user_name = ''
    if request.user.is_authenticated:
        logged = True
        user_name = request.user
    return render(request, 'homepage.html', {'logged': logged, 'user_name': user_name})
