from django.shortcuts import render, redirect
from .models import User
from django.core.urlresolvers import reverse
from django.contrib import messages
import bcrypt
import datetime

def index(request):

    if 'pokecount' in request.session:
        print "there is a session!"
    else:
        request.session['pokecount'] = 0
        request.session['message'] = []
    return render(request, 'login_reg_app/index.html')

def register(request):
    postData = {
    'f_name': request.POST['f_name'],
    'alias': request.POST['alias'],
    'email': request.POST['email'],
    'password': request.POST['password'],
    'c_password': request.POST['confirm_password']
    }

    user = User.objects.validate(postData)

    if user[0]:
        # user = (True, {'message': 'This is a message'})
        for error in user[1].itervalues():
            messages.error(request, error)
        
    else:
        request.session['id'] = User.objects.last().id
        user = User.objects.last()
        context = {'user': user}
        return render(request, 'login_reg_app/poke.html', context)

    return redirect('/')

def login(request):
    user = User.objects.filter(email = request.POST['email'])
        
    if user:
        if bcrypt.hashpw(request.POST['password'].encode('utf-8'), user[0].password.encode('utf-8')) == user[0].password:
            request.session['id'] = user[0].id
            context = {'user': user[0]}
            return render(request, 'login_reg_app/poke.html', context)
        else:
            messages.error(request, "This is not the correct username or password")
            return redirect('/')
    else:
        messages.error(request, 'This is not the correct username or password')
        return redirect('/')

def poke(request):
    if request.method == 'POST':
        request.session['pokecount']
    if request.POST['poke'] == poke:
        pokecount += 1
        print 'poked!'

    return redirect(reverse('login_reg_app:poke'))

def logout(request):
    request.session.clear()
    return redirect('/')
# Create your views here.


# to do list:
# have pokecount increase poke history when pressed
# show the log of poke history messages
# remain in user session when poke button is clicked
# show other users info in the table
# ask about middleware login stuff.
# logic is flawed in pokecount request session
# needs regex to access different users?
# need more if statements to make the different users pokeable