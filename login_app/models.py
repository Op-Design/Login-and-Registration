from django.db import models
import re, bcrypt

class UserManager (models.Manager):
    def registration_validator(self,postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        email = User.objects.filter(email=postData['email'])
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_invalid'] = 'Invalid email address'
        if len(postData['email'])==None:
            errors['email_len']='Email address required'
        if email:
            errors['email_unique']='Email is already in system'
        if len(postData['first_name'])<2:
            errors['first_name']='First Name should be at least 2 characters'
        if len(postData['last_name'])<2:
            errors['last_name']='Last Name should be at least 2 characters'
        if len(postData['password'])<8:
            errors['password']='Password should be at least 8 characters long'
        if not postData['password']==postData['c_password']:
            errors['password_c']='Passwords should match'
        return errors
  
    def login_validator(self,postData):
        errors={}
        email = User.objects.filter(email=postData['email'])
        if not email:
            errors['creds']='Invalid Credentials TEST EMAIL'
        else:
            if email:
                logged_user = email[0]
                if not bcrypt.checkpw(postData['password'].encode(),logged_user.password.encode()):
                    errors['creds']='Invalid Credentials TEST PASSWORD'
        return errors    

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
    
    def __repr__(self):
        return f"<User: {self.first_name} {self.last_name} ({self.id})>"