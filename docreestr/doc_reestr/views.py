from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import Status, User, Document
from .form import RegistryForm, LoginForm, LoadDocumentForm


# Create your views here.

def index(request):
    sess = request.session if 'id' in request.session else None
    user_list = User.objects.all()
    print(sess)
    context = {'user_list': user_list, 'sess':sess}
    return render(request, 'doc_reestr/index.html', context)

def list_doc(request, user_id):
    sess = request.session if 'id' in request.session else None
    doc_list = Document.objects.filter(id_user = user_id)
    try:
        user = User.objects.get(id = user_id)
    except Exception:
        user = None
    context = {'doc_list': doc_list, 'user': user, 'sess':sess}
    return render(request, 'doc_reestr/list_docs.html',context)

def preview(request, user_id, doc_id):
    sess = request.session if 'id' in request.session else None
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
    context = {'doc':doc, 'user': user, 'status': status, 'sess':sess   }
    return render(request, 'doc_reestr/preview.html', context)

def login(request):
    if 'id' not in request.session:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                try:
                    user = User.objects.get(name = form.cleaned_data['name'])
                    if user.password == form.cleaned_data['password']:
                        request.session['id'] = user.id
                        request.session['name'] = user.name
                except Exception:
                    pass
                return HttpResponseRedirect('/doc_reestr')
        else:
            form = LoginForm()
        context = {'form': form}
        return render(request, 'doc_reestr/login.html', context)
    else:
        return HttpResponseRedirect('/doc_reestr')

def logout(request):
    request.session.pop('id')
    request.session.pop('name')
    return HttpResponseRedirect('/doc_reestr/')

def registry(request):
    if request.method == 'POST':
        form = RegistryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            INN = form.cleaned_data['INN']
            password = form.cleaned_data['password']
            user = User(name = name, INN = INN, password = password)
            user.save()
            return HttpResponseRedirect('/doc_reestr')
    else:
        form = RegistryForm()
    context = {'form':form}
    return render(request, 'doc_reestr/registry.html', context)

def load_doc(request):
    if 'id' in request.session:
        if request == 'POST':
            form = LoadDocumentForm(request.POST)
            print
            if form.is_valid():
                print('valid')
                doc = Document(name = form.cleaned_data['name'], id_user = request.session['id'], id_status = 1)
                doc.save()
                return HttpResponseRedirect('/doc_reestr/load_doc')
        else:
            form = LoadDocumentForm()
        return render(request, 'doc_reestr/load_doc.html', {'form':form, 'sess':request.session})
    return HttpResponseRedirect('/doc_reestr')

def my_doc(request):
    if 'id' in request.session:
        doc_list = Document.objects.filter(id_user = request.session['id'])
        context = {'docs': doc_list, 'sess':request.session}
        return render(request, 'doc_reestr/mydoc.html', context)
    else:
        return HttpResponseRedirect('doc_reestr')

def cancel(request, doc_id):
    pass

def setting(request):
    sess = request.session if 'id' in request.session else None
    return render(request, 'doc_reestr/setting.html', {'sess':sess})
