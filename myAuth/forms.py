# coding: utf-8
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core import validators
from int.myAuth.utils.generate_username import generate_username


class AuthenticationCustomForm(AuthenticationForm):
    
    email = forms.EmailField(label="Email", required=True)
    
    class Meta:
        fields = ("email", "password")
        
    def __init__(self, *args, **kwargs):
        super(AuthenticationCustomForm, self).__init__(*args, **kwargs)
        del self.fields["username"]
        self.fields.keyOrder = ["email", "password"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if email in validators.EMPTY_VALUES:
            raise forms.ValidationError("Por favor, preencha um email")
        
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if password in validators.EMPTY_VALUES:
            raise forms.ValidationError("Por favor, preencha sua senhal")
        
        return password
         
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Por favor, entre com um e-mail e senha corretos. Lembre-se que a senha diferencia letra maiúscula de minúscula.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("Esta conta está inativa.")
        self.check_for_test_cookie()
        return self.cleaned_data
            
class UserCreationCustomForm(UserCreationForm):
    
    email = forms.EmailField(required=True)
    fullname = forms.CharField(label="Nome completo", max_length=70, required=True)
    
    class Meta:
        model = User
        fields = ("email", "fullname", "password1", "password2")   
        
    def __init__(self, *args, **kwargs):
        super(UserCreationCustomForm, self).__init__(*args, **kwargs)
        del self.fields["username"]
        
    def clean_fullname(self):
        fullname = self.cleaned_data.get("fullname")
        if fullname not in validators.EMPTY_VALUES:
            # removes whitespace from the beginning and the end of the fullname
            fullname = fullname.strip()       

            # if there's no whitespace, then there's no last names
            if fullname.find(" ") == -1:
                raise forms.ValidationError("Você esqueceu do nome ou do sobrenome?")
            
            # if a whitespace was found but side-by-side only by one word, then the user has forgotten something
            if len(fullname.split()) == 1:
                raise forms.ValidationError("Você esqueceu do nome ou do sobrenome?")
               
        return fullname
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        
        if email in validators.EMPTY_VALUES:
            raise forms.ValidationError("E-mail vazio")
        
        try:
            User.objects.get(email=email)
            raise forms.ValidationError("Este e-mail já está sendo utilizado")
        except User.DoesNotExist:
            return self.cleaned_data["email"]
            
    def clean(self):        
        # generates the username only if the email was properly filled
        email = self.cleaned_data.get("email")
        if email not in validators.EMPTY_VALUES:
            self.cleaned_data["username"] = generate_username(email)

        # generates the first name and last names if fullname was filled 
        fullname = self.cleaned_data.get("fullname")
        if fullname not in validators.EMPTY_VALUES:        
            fullname = fullname.partition(" ")
            self.cleaned_data["first_name"] = fullname[0]
            self.cleaned_data["last_name"] = fullname[2]
         
        return self.cleaned_data
                 
    def save(self, commit=True):
        user = super(UserCreationCustomForm, self).save(commit=False)
        user.email = self.cleaned_data.get("email")
        user.username = self.cleaned_data.get("username")
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.is_active = False
        
        if commit:
            user.save()
        
        return user     