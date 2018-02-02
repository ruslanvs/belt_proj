print '*'*25, 'VIEWS.PY', '*'*25
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Travel

def index ( request ):
    if "sess_u_id" not in request.session:
        return render( request, "belt/index.html" )
    else:
        return redirect( "/travels" )
    
def sign_in( request ):
    if "sess_u_id" not in request.session: #IF LOGGED IN ALREADY, THEN GOES TO HOME PAGE
        errors = User.objects.validator_login( request.POST )

        if errors:
            for e in errors:
                messages.error( request, errors[e] )
            return redirect( "/" )
        else:
            request.session['sess_u_id'] = User.objects.get( email = request.POST['email'] ).id
            return redirect( "/travels" )

    else:
        return redirect( "/travels" )

def sign_out( request ):
    request.session.flush()
    return redirect( "/" )

def sign_up( request ):
    if "sess_u_id" not in request.session: #IF LOGGED IN ALREADY, THEN GOES TO HOME PAGE
        errors = User.objects.validator_signup( request.POST )
        
        if errors:
            for e in errors:
                messages.error( request, errors[e] )
            return redirect( "/" )
            
        else:
            request.session['sess_u_id'] = User.objects.get( email = request.POST['email'] ).id
            messages.success( request, "Your user data has been saved" )
            return redirect( "/travels" )
    else:
        return redirect( "/travels" )

def travels( request ):
    if "sess_u_id" not in request.session:
        return redirect( "/" )
    else:
        page_data = {}
        sess_user = User.objects.get( id = request.session['sess_u_id'] )
        page_data = {
            "sess_user": sess_user,
            "user_travels": sess_user.joining_travels.all(),
            "other_travels": Travel.objects.exclude( joining_users = sess_user ),
        }
        print page_data['user_travels']        
        print page_data['other_travels']        
        return render( request, "belt/travels.html", page_data )

def travel_show( request, id ):
    if "sess_u_id" not in request.session:
        return redirect( "/" )
    else:
        t = Travel.objects.get ( id = id )
        sess_user = User.objects.get( id = request.session['sess_u_id'] )
        page_data = {
            "sess_user": sess_user,
            "travel": t,
            "other_travelers": t.joining_users.exclude( id = request.session['sess_u_id'] )
            # "other_travelers": User.objects.exclude( id = request.session['sess_u_id'] )
        }
        # print '*'*25, "OTHER TRAVELERS:", page_data['other_travelers']['name']
        return render( request, "belt/travel.html", page_data )

def travel_new( request ):
    if "sess_u_id" not in request.session:
        return redirect( "/" )
    else:
        return render( request, "belt/travel_new.html" )

def travel_create( request ):
    if "sess_u_id" not in request.session:
        return redirect( "/" )
    else:
        errors = Travel.objects.validator( request.POST, request.session['sess_u_id'] )

        if errors:
            for e in errors:
                messages.error( request, errors[e] )
            return redirect( "/travels/new" )

        else:
            return redirect( "/travels" )

def travel_join( request, id ):
    if "sess_u_id" not in request.session:
        return redirect( "/" )
    else:
        t = Travel.objects.get( id = id )
        sess_user = User.objects.get( id = request.session['sess_u_id'] )
        t.joining_users.add( sess_user )
        return redirect( "/travels" )

def travel_leave( request, id ):
    if "sess_u_id" not in request.session:
        return redirect( "/" )
    else:
        t = Travel.objects.get( id = id )
        sess_user = User.objects.get( id = request.session['sess_u_id'] )
        t.joining_users.remove( sess_user )
        return redirect( "/travels" )
