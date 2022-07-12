from types import TracebackType
from django import http
from django.http import HttpResponseRedirect
from django.shortcuts import render
import markdown2
from markdown2 import Markdown
from django.urls import reverse
from django import forms
from . import util
import secrets

class add_entry_form(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 15}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry): #return a page when a query is sent
    markdowner = Markdown() #function alias 
    entrypg = util.get_entry(entry) #variable name of query
    if entrypg == None: #if wiki entry does not exist
        return render(request, "encyclopedia/no_entry.html") #return page - no entry yet 
    else: #if the page is found
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(entrypg), #content of entry
            "entryTitle": entry #title of entry 
        })

def search(request):
    query = request.GET.get("q", '') #get the query which the user inputted
    entry = util.get_entry(query)
    if entry != None: 
        return HttpResponseRedirect(reverse("entry", kwargs={'entry':query}))
    else: 
        entries = [] #empty list 
        for each in util.list_entries(): #for every returned topic
            if query.lower() in each.lower(): #if the query is in the returned topic 
                entries.append(each) #add it to the entries 
        return render(request, "encyclopedia/index.html", {
            "entries": entries,
            "search": True, 
            "value": query
        })

def add(request):
    if request.method == "POST":
        form = add_entry_form(request.POST) #store user input under the variable 'form'
        if form.is_valid(): #server side validation for submission
            title = form.cleaned_data["title"] #get title content
            description = form.cleaned_data["content"] #get description content
            edit = form.cleaned_data["edit"] #edit boolean value
            if edit is True or util.get_entry(title) is None:
                util.save_entry(title, description)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
            else:
                return render(request, "encyclopedia/add.html", {
                    "form": form,
                    "existing": True,
                    "entry": title
                })
        else: 
            return render(request, "encyclopedia/add.html", {
                "existing": False,
                "form": form
            })  
    elif request.method == "GET":
        return render(request, "encyclopedia/add.html", {
            "form": add_entry_form(),
            "existing": False
        })

def edit(request, entry): 
    entryPage = util.get_entry(entry)
    if entry == None: #copy code from entry()
        return render(request, "encyclopedia/no_entry.html") 
    else:
        form = add_entry_form()
        form.fields["title"].initial = entry
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/add.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "entryTitle": form.fields["title"].initial
        })

def rand_select(request):
    entrys = util.list_entries()
    random = secrets.choice(entrys)
    return HttpResponseRedirect(reverse("entry", kwargs={"entry": random}))