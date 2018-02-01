print '*'*25, 'VIEWS.PY', '*'*25
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def index ( request ):
    if "sess_u_id" not in request.session:
        return render( request, "belt/index.html" )
    else:
        return redirect( "/home" )
    
def sign_in( request ):
    if "sess_u_id" not in request.session: #IF LOGGED IN ALREADY, THEN GOES TO HOME PAGE
        errors = User.objects.validator_login( request.POST )
        if errors:
            messages.error( request, errors )
            return redirect( "/" )
        else:
            request.session['sess_u_id'] = User.objects.get( email = request.POST['email'] ).id
            return redirect( "/home" )
    else:
        return redirect( "/home" )

def sign_out( request ):
    request.session.flush()
    return redirect( "/" )

def sign_up( request ):
    if "sess_u_id" not in request.session: #IF LOGGED IN ALREADY, THEN GOES TO HOME PAGE
        errors = User.objects.validator_signup( request.POST )
        if errors:
            messages.error( request, errors )
            return redirect( "/" )
        else:
            request.session['sess_u_id'] = User.objects.get( email = request.POST['email'] ).id
            messages.success( request, "Your user data has been saved" )
            return redirect( "/home" )
    else:
        return redirect( "/home" )

def home( request ):
    if "sess_u_id" not in request.session:
        return redirect( "/" )
    else:
        page_data = {}
        sess_user = User.objects.get( id = request.session['sess_u_id'] )
        page_data = {
            "sess_user": sess_user,
        }
        
        return render( request, "belt/home.html", page_data )
