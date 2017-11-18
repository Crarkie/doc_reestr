from django.forms import Form
from django import forms

class RegistryForm(Form):
    name = forms.CharField(label = 'Название компании')
    INN = forms.CharField(label = 'ИНН')
    file = forms.FileField(label = 'Выбрать файл', required= False)

class LoginForm(Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Логин'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Логин'}), required = False)