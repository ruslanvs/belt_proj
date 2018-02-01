from __future__ import unicode_literals
print '*'*25, 'MODELS.PY', '*'*25

from django.db import models
import re, bcrypt
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
        nlen_min = 2
        pwlen_min = 8

        # VALIDATE NAME
        if len( post_data['name'] ) < nlen_min: # LENGTH
            errors["name"] = "Name cannot be less than " + str( nlen_min ) + " characters. "

        # VALIDATE ALIAS
        if len( post_data['alias'] ) < nlen_min: # LENGTH
            errors["alias"] = "Alias cannot be less than " + str( nlen_min ) + " characters. "

        elif not str.isalpha( str( post_data['alias'] ) ): # CONVENTIONS
            errors["alias"] = "Invalid characters in the alias. "

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
                alias = post_data['alias'],
                email = post_data['email'],
                pw = bcrypt.hashpw( post_data['pw'].encode(), bcrypt.gensalt() ),
            )

class User( models.Model ):
    name = models.CharField( max_length = 255 )
    alias = models.CharField( max_length = 255 )
    email = models.CharField( max_length = 255 )
    pw = models.CharField( max_length = 255 )
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )
    objects = UserManager()
    def __unicode__( self ):
        return "id: " + str( self.id ) + ", name: " + self.name + ", alias: " + self.alias
