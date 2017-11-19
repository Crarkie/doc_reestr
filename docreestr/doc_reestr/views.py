from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.core.management import call_command
from django.shortcuts import render, get_object_or_404
from .models import Status, User, Document
from .form import RegistryForm, LoginForm, LoadDocumentForm, SettingsForm
from .transactions import *
from base58 import b58encode
from base58 import b58decode


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
    data_handler = DataHandler('localhost:5001', 'localhost:8545')
    blockchain_doc = data_handler.get_document(b58decode(doc.hash_file))
    context = {'doc':doc, 'user': user, 'status': Status.objects.get(id = blockchain_doc['state'].value),
               'sess':sess, 'account' : blockchain_doc['creator']}
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
        if request.method == 'POST':
            form = LoadDocumentForm(request.POST, request.FILES)
            if form.is_valid():
                user = User.objects.get(id = request.session['id'])


                destination = open('upload', 'wb+')
                for chunk in request.FILES['document'].chunks():
                    destination.write(chunk)
                destination.close()

                doc = upload_document(file_path='upload',
                                address=user.account, passphrase=form.cleaned_data['passphrase'])

                document = Document(name=form.cleaned_data['title'],
                                    id_user=User.objects.get(id=request.session['id']),
                                    id_status=Status.objects.get(id = doc['state']), hash_file=b58encode(doc['hash']))
                document.save()

                return HttpResponseRedirect('/user' + str(document.id_user.id) + '/doc' + str(document.id))
        else:
            form = LoadDocumentForm()
        return render(request, 'doc_reestr/load_doc.html', {'form':form.as_table(), 'sess':request.session})
    return HttpResponseRedirect('/doc_reestr')

def my_doc(request):
    if 'id' in request.session:
        doc_list = Document.objects.filter(id_user = request.session['id'])
        context = {'docs': doc_list, 'sess':request.session, 'user': request.session['id']}
        return render(request, 'doc_reestr/mydoc.html', context)
    else:
        return HttpResponseRedirect('doc_reestr')

def cancel(request, doc_id):
    pass

def setting(request):
    sess = request.session if 'id' in request.session else None
    if sess:
        if request.method == 'POST':
            form = SettingsForm(request.POST)
            if form.is_valid():
                user = User.objects.get(id = sess['id'])
                user.account = form.cleaned_data['account']
                user.save()
                return HttpResponseRedirect('')
        else:
            form = SettingsForm()
            user = User.objects.get(id=sess['id'])
        return render(request, 'doc_reestr/setting.html', {'sess':sess, 'acc':user.account, 'form':form})
