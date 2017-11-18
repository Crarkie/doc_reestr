from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import Status, User, Document
from .form import RegistryForm, LoginForm

# Create your views here.

def index(request):
    user_list = User.objects.all()
    context = {'user_list': user_list}
    return render(request, 'doc_registr/index.html', context)

def list_doc(request, user_id):
    doc_list = Document.objects.filter(id = user_id)
    try:
        user = User.objects.get(id = user_id)
    except Exception:
        user = None
    context = {'doc_list': doc_list, 'user': user}
    return render(request, 'doc_registr/list_docs.html',context)

def preview(request, user_id, doc_id):
    try:
        doc = Document.objects.get(id = doc_id)
    except Exception:
        doc = None
    try:
        user = User.objects.get(id = user_id)
    except Exception:
        user = None
    try:
        status = Status.objects.get(id = doc.id_status)
    except Exception:
        status = None
    context = {'doc':doc, 'user': user, 'status': status}
    return render(request, 'doc_registr/preview.html', context)

def login(request):
     if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            pass


def registry(request):
    if request.method == 'POST':
        form = RegistryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            INN = form.cleaned_data['INN']
            user = User(name = name, INN = INN)
            user.save()
            return HttpResponseRedirect('/doc_registr')
    else:
        form = RegistryForm()
    context = {'form':form}
    return render(request, 'doc_registr/registry.html', context)

def load_doc(request):
    pass

def my_doc(request):
    pass

def cancel(request, doc_id):
    pass

def setting(request):
    pass
