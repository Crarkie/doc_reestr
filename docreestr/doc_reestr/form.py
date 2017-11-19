from django.forms import Form
from django import forms

class RegistryForm(Form):
    name = forms.CharField(label = 'Название компании')
    INN = forms.CharField(label = 'ИНН')
    file = forms.FileField(label = 'Выбрать файл', required= False)
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

class LoginForm(Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Пароль'}), required = False)

class LoadDocumentForm(Form):
    title = forms.CharField(label = 'Название документа')
    document = forms.FileField(label='Выберите файл', required = False)
    passphrase = forms.CharField(label = 'Ключ аккаунта(не сохраняется)', widget=forms.PasswordInput)
