from __future__ import unicode_literals
print '*'*25, 'MODELS.PY', '*'*25

from django.db import models
import re, bcrypt, datetime
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager( models.Manager ):
    def validator_login( self, post_data ):
        errors = {}
        existing_user = User.objects.filter( email = post_data['email'] ).first()#>> get?
        if not existing_user: # EMAIL VALIDATION
            errors["email"] = "User with email " + post_data['email'] + " does not exist"
        else: # CHECK PW
            if not bcrypt.checkpw( post_data['pw'].encode(), User.objects.get( email = post_data['email'] ).pw.encode() ):
                errors["pw"] = "Wrong password"
        return errors

    def validator_signup( self, post_data ):
        errors = {}
        nlen_min = 3
        pwlen_min = 8

        # VALIDATE NAME
        if len( post_data['name'] ) < nlen_min: # LENGTH
            errors["name"] = "Name cannot be less than " + str( nlen_min ) + " characters. "

        # VALIDATE USERNAME
        if len( post_data['username'] ) < nlen_min: # LENGTH
            errors["username"] = "Username cannot be less than " + str( nlen_min ) + " characters. "

        elif not str.isalpha( str( post_data['username'] ) ): # CONVENTIONS
            errors["username"] = "Invalid characters in the username. "

        # VALIDATE EMAIL
        if not email_regex.match( post_data['email'] ): # CONVENTIONS
            errors["email"] = post_data['email'] + "is not a valid email. "

        else: # UNIQUENESS
            existing_user = User.objects.filter( email = post_data['email'] ).first()
            if existing_user:
                errors["email"] = "Email " + post_data['email'] + " is already in use"

        # VALIDATE PASSWORD CONVENTIONS AND CONFIRMATION
        if len( str( post_data['pw'] ) ) < pwlen_min:
            errors["pw"] = "Password should have at least " + str( pwlen_min ) + " characters"
        elif post_data['pw'] != post_data['pwc']:
            errors["pw"] = "Password confirmation does not match"

        if errors:
            return errors
        else: # SUCCESS - ADD NEW USER INTO THE DATABASE
            User.objects.create(
                name = post_data['name'],
                username = post_data['username'],
                email = post_data['email'],
                pw = bcrypt.hashpw( post_data['pw'].encode(), bcrypt.gensalt() ),
            )

class TravelManager( models.Manager ):
    def validator( self, post_data, sess_u_id ):
        errors = {}
        len_min = 1
        
        # now = datetime.datetime.today()
        # print '*'*25, 'TODAYS DATE/TIME:', now.strftime("%Y-%m-%d %H:%M:%S")
        # # datetime.date()
        # print '*'*25, 'FORM DATA DATE:', post_data['start_date']
        # print '*'*25, 'FORM DATA DATE:', datetime.datetime(2009,04,01)
        # d = post_data['start_date']
        # d.isoformat()
        # datetime.datetime(d)
        # datetime.strptime(d,'%b%d%Y').strftime('%m/%d/%Y')
        
        # print '*'*25, 'FORM DATA DATE:', datetime.strptime(d,'%b%d%Y').strftime('%m/%d/%Y')

# >>> s='2005-08-11T16:34:33Z'
# >>> t=datetime.datetime(2009,04,01)
# >>> t.isoformat()
        

        if len( str( post_data['destination'] ) ) < len_min:
            errors["destination"] = "Destination cannot be empty"

        if len( str( post_data['plan'] ) ) < len_min:
            errors["plan"] = "Description cannot be empty"
            
        if len( str( post_data['start_date'] ) ) < len_min:
            errors["start_date"] = "Start date cannot be empty"
        # elif post_data['start_date'] < now:
        #     errors["start_date"] = "Start date cannot be in the past" #>>> finish the date to be in the future check - resolve the "can't compare datetime.datetime to unicode" error

        if len( str( post_data['end_date'] ) ) < len_min:
            errors["end_date"] = "End date cannot be empty"
        elif post_data['end_date'] < post_data['start_date']:
            errors["start_date"] = "End date cannot be earlier than the start date"

        if errors:
            return errors
        else:
            sess_user = User.objects.get( id = sess_u_id )
            t = Travel.objects.create(
                planned_by_user = sess_user,
                destination = post_data['destination'],
                plan = post_data['plan'],
                start_date = post_data['start_date'],
                end_date = post_data['end_date']
            )

            t.joining_users.add( sess_user )


class User( models.Model ):
    name = models.CharField( max_length = 255 )
    username = models.CharField( max_length = 255 )
    email = models.CharField( max_length = 255 )
    pw = models.CharField( max_length = 255 )
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )
    objects = UserManager()
    def __unicode__( self ):
        return "id: " + str( self.id ) + ", name: " + self.name + ", username: " + self.username

class Travel( models.Model ):
    planned_by_user = models.ForeignKey( User, related_name = "planned_travels" )
    joining_users = models.ManyToManyField( User, related_name="joining_travels")
    destination = models.CharField( max_length = 255 )
    plan = models.TextField( max_length = 1000 )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )
    objects = TravelManager()