import os
from django.http import QueryDict
from accounts.models import *
from partner.forms import Actif_par_id, Option_par_id
from profil.forms import Profils
from structure.forms import Actif_structure, Option_structure
from .forms import *
from ajouter.forms import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import  pandas as pd
from plotly.offline import plot
import plotly.express as px
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator


@login_required
def dashboard(request):
    context={}
    partenaires = partenaire.objects.all()
    part_count = partenaires.count()
    structures = structure.objects.all()
    struct = structures.count()
    personnel = MyUser.objects.all()  
    per = personnel.count() 
    qs = structures
    project = [
        {
            'Structure': x.nom,
            'Nombre': x.membre,           
            'Responsable' : x.nom
        } for x in qs
    ]
    df = pd.DataFrame(project)    
    fig = px.bar(df, x ="Structure", y="Nombre" , color="Responsable")
    fig.layout.plot_bgcolor = 'black'
    fig.layout.paper_bgcolor = 'black'
    fig.layout.legend = {'font_color':'white'}
    fig.update_xaxes({'color':'white'})
    fig.update_yaxes({'color':'white'})
  
    gantt_plot = plot(fig, output_type="div")

    cam=[{
        "nom" : x.nom,
        "membre"  : x.membre, 
        "Partenaire" : x.nom,        
    } for x in qs
    ]

    df = pd.DataFrame(cam)  
    figa = px.pie(df, values='membre',names="nom", title ="Api-Sport", color="Partenaire")
    figa.layout.paper_bgcolor = 'black'
    figa.layout.legend = {'font_color':'white'}
    figa.update_layout(title_font_color='white')
    figa.update_xaxes({'color':'white'})
    figa.update_yaxes({'color':'white'})
    cam_plot= plot(figa, auto_open=False, output_type="div")
          
    context= {
        "partenaires" : partenaires,
        "part" : part_count,
        "structures" : structures,
        "struct": struct,
        "personnel": personnel,
        "per": per, 
        "graph" : gantt_plot,  
        "cam" : cam_plot,
    }
    return render(request,'dashbord.html', context)

@login_required
def ma_structure(request):
    return render(request,'mastructure.html')

@login_required
def mon_partenaire(request):
    return render(request, 'monpartenaire.html')

def option_user_partenaire(request, pk):
    part = partenaire.objects.get(pk=pk)
    form = Option_par_id(instance=part)
    if request.method == "POST":
        form = Option_par_id(request.POST, instance=part)           
        if form.is_valid():             
            form.save()
            messages.success(request,"les options ont été modifier!")
            return redirect('monPartenaire')
    return render(request, 'option_partenaire.html',{'partenaire':part, 'form': form})


def option_user_structure(request, pk):
    structures = structure.objects.get(id=pk) 
    form = Option_structure(instance=structures)
    options = option.objects.all().order_by()
    partenaires = partenaire.objects.get(id=structures.part.id)
    listoptionpartenaire = [option_partenaire.id for option_partenaire  in partenaires.option.all()]
    listoptionstructure = [option_structure.id for option_structure  in structures.option.all()]
    if request.method == "POST": 
        form = Option_structure(request.POST, instance=structures)
        if form.is_valid():
           form.save()
           messages.success(request,"les options ont été modifier!")
        return render(request,'mastructure.html')

    context = {
        "structure" : structures,
        "options" : options, 
        "listoptionpartenaire" : listoptionpartenaire,
        "listoptionstructure" : listoptionstructure,       
        "form" : form,
    }
    return render(request, 'option_structure.html', context)


@login_required
def user_partenaire(request, pk):
    part = partenaire.objects.get(id=pk)
    form = ModifPartenaire(request.POST or None, request.FILES or None, instance=part)
    if form.is_valid():      
        form.save()
        messages.success(request,"le partenaire a été modifier!")
        return redirect('monPartenaire')
    return render(request,'modifpartenaire.html',{'partenaire':part, 'form': form})

@login_required
def user_structure(request, pk):
    part = structure.objects.get(id=pk) 
    form = ModifStructureForm(request.POST or None, request.FILES or None, instance=part)
    if form.is_valid():
        form.save()
        messages.success(request,"la structure a bien été modifier !")
        return redirect('maStructure')
    return render(request,'modifstructure.html',{'structure':part, 'form': form})

def delete_previous_picture(previous,new):
    if previous != new:
        os.remove(previous)
        return True
    return False    

def delete_previous_pictures(previous):
    os.remove(previous)
    return True  

#option"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def cherche_option(request):
    cherche = request.POST.get('cherche')
    options = option.objects.filter(Q(slug__icontains=cherche) |                                   
                                    Q(description__icontains=cherche))                                                                     
    context = {
        'option' : options
    }
    return render(request,'dashboard_option.html', context)

@login_required
def dashboard_option(request):
    options = option.objects.all()
    paginator = Paginator(options, 5)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    context= { "option" : page_object }
    return render(request, 'dashboard_option.html', context)

@login_required
def delete_option(request, pk):
    option.objects.filter(id=pk).delete()
    messages.success(request,"l'option a été supprimer!")
    options = option.objects.all()
    context= { "option" : options }
    return render(request, 'dashboard_option.html', context)

@login_required
def modifier_option(request, pk):
    options = option.objects.get(id=pk)
    form = AjoutoptionForm(request.POST or None, instance=options)
    return render(request,'modif-option.html',{'option': options, 'form': form})

@login_required
def modifier_option_valide(request, pk):
    options = option.objects.get(id=pk)
    context= { "option" : options }    
    form = AjoutoptionForm(instance=options)
    if request.method == 'GET':
        return render(request, 'dashboard_option.html', context)
    elif request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = AjoutoptionForm(data, instance=options)
        if form.is_valid():
            form.save()
            messages.success(request,"l'otpion a été modifier !")
            return redirect('dashboard_option')
    return redirect('dashboard_option')
        
#partenaire#############################################################################

def cherche_partenaire(request):
    cherche = request.POST.get('cherche')
    partenaires = partenaire.objects.filter(Q(ville__icontains=cherche) |
                                       Q(slug__icontains=cherche) |
                                       Q(numberPhone__icontains=cherche) |
                                       Q(description__icontains=cherche))                                                                      
                                                                                                                
    context = {
        'partenaires' : partenaires
    }
    return render(request,'dashboard_partenaire.html', context)


@login_required
def dashboard_partenaire(request):
    partenaires = partenaire.objects.all() 
    paginator = Paginator(partenaires, 5)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    context= { "partenaires" : page_object}
    return render(request,'dashboard_partenaire.html', context)

def dash_valide_partenaire(request, pk):
    partenaires = partenaire.objects.get(id=pk)
    if request.method == "POST":
        form = Actif_par_id(request.POST, instance=partenaires)         
        if form.is_valid():          
            form.save()
            messages.success(request,"le partenaire a été modifier!")
            return redirect('dashboard_partenaire')   

@login_required
def delete_partenaire(request, pk):
    part = partenaire.objects.get(id=pk)
    default_image_path = part.photo.path
    partenaire.objects.filter(id=pk).delete()
    delete_previous_pictures(default_image_path) 
    messages.success(request,"le partenaire a été supprimer!")  
    partenaires = partenaire.objects.all()
    context= { "partenaires" : partenaires }
    return render(request, 'dashboard_partenaire.html', context)

@login_required
def modifier_partenaire(request, pk):
    partenaires = partenaire.objects.get(id=pk)
    form = AjoutPartenaireForm(instance=partenaires)
    return render(request,'modif-partenaire.html',{'partenaires': partenaires, 'form': form})

@login_required
def modifier_partenaire_valide(request, pk): 
    part = partenaire.objects.get(id=pk)
    if part.photo:
        default_image_path = part.photo.path
    form = AjoutPartenaireForm(request.POST or None, request.FILES or None, instance=part)
    if form.is_valid():
        if len(request.FILES)!= 0:
           delete_previous_picture(default_image_path, part.photo.path)
        form.save()
        messages.success(request,"le partenaire a été modifier!")
        return redirect('dashboard_partenaire')

@login_required
def add_partenaire(request):    
    if request.method == "POST":
        form = AjoutPartenaireForm(request.POST,request.FILES)         
        if form.is_valid():                      
            form.save()
            messages.success(request,"le partenaire a été ajouter!")
            return redirect('dashboard_partenaire')
        else:
            form = AjoutPartenaireForm() 
    return render(request, "rajoutpartenaire.html",{"form": form})  

#structure#################################################################  

def cherche_structure(request):
    cherche = request.POST.get('cherche')
    structures = structure.objects.filter(Q(nom__icontains=cherche) |
                                       Q(slug__icontains=cherche) |
                                       Q(numberPhone__icontains=cherche) |                                                                       
                                       Q(adresse__icontains=cherche))                                                                           
    context = {
        'structures' : structures
    }
    return render(request,'dashboard_structure.html', context) 

@login_required
def dashboard_structure(request):
    structures = structure.objects.all()
    paginator = Paginator(structures, 5)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    context= { 
        "structures" : page_object
    }
    return render(request, 'dashboard_structure.html', context) 

@login_required
def delete_structure(request, pk):
    part = structure.objects.get(id=pk)
    if part.photo:
        default_image_path = part.photo.path
    structure.objects.filter(id=pk).delete()
    if part.photo:
        delete_previous_pictures(default_image_path) 
    messages.success(request,"la structure a bien été supprimer !")  
    structures = structure.objects.all()
    context= { "structures" : structures }
    return render(request, 'dashboard_structure.html', context)

@login_required
def modifier_structure(request, pk):
    structures = structure.objects.get(id=pk)
    form = AjoutStrutureForm(request.POST or None, instance=structures)
    return render(request,'modif-structure.html',{'structures': structures, 'form': form})

@login_required
def modifier_structure_valide(request, pk): 
    part = structure.objects.get(id=pk)
    if part.photo:
        default_image_path = part.photo.path
    form = AjoutStrutureForm(request.POST or None, request.FILES or None, instance=part)
    if form.is_valid():
        if len(request.FILES)!= 0:
           delete_previous_picture(default_image_path, part.photo.path)
        form.save()
        messages.success(request,"la structure a bien été modifier !")
        return redirect('dashboard_structure')

@login_required
def add_structure(request):    
    if request.method == "POST":
        form = AjoutStrutureForm(request.POST,request.FILES)         
        if form.is_valid():                   
            form.save()
            messages.success(request,"la structure a bien été ajouter !")
            return redirect('dashboard_structure')
        else:
            form = AjoutPartenaireForm() 
    return render(request, "rajoutstructure.html",{"form": form}) 

def dash_valide_structure(request, pk):
    structures = structure.objects.get(id=pk)
    if request.method == "POST":
        form = Actif_structure(request.POST, instance=structures)         
        if form.is_valid():          
            form.save()
            messages.success(request,"la structure a bien été modifier !")
            return redirect('dashboard_structure') 

#Personnel################################################################################

def cherche_personnel(request):
    cherche = request.POST.get('cherche')
    personnel = MyUser.objects.filter (Q(nom__icontains=cherche) |
                                       Q(slug__icontains=cherche) |
                                       Q(adresse__icontains=cherche) |
                                       Q(prenom__icontains=cherche) |
                                       Q(email__icontains=cherche) |
                                       Q(ville__icontains=cherche) |
                                       Q(username__icontains=cherche) |
                                       Q(CodePostal__icontains=cherche) |                                     
                                       Q(permission__icontains=cherche))                                                                           
    context = {
        'personnel' : personnel
    }
    return render(request,'dashboard_personnel.html', context) 

@login_required
def dashboard_personnel(request):
    personnel = MyUser.objects.all()
    paginator = Paginator(personnel, 4)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    context = { "personnel" : page_object }
    return render(request, 'dashboard_personnel.html', context)

@login_required
def delete_personnel(request, pk):
    part = MyUser.objects.get(id=pk)
    if part.photo:
        default_image_path = part.photo.path
    MyUser.objects.filter(id=pk).delete()
    if default_image_path:
        delete_previous_pictures(default_image_path) 
    messages.success(request,"la personne a bien été supprimer!")  
    personnel = MyUser.objects.all()
    context= { "personnel" : personnel }
    return render(request, 'dashboard_personnel.html', context)

@login_required
def modifier_personnel(request, pk):
    personnel = MyUser.objects.get(id=pk)
    form = Profils(request.POST or None, instance=personnel)
    return render(request,'modif-personnel.html',{'personnel': personnel, 'form': form})

@login_required
def modifier_personnel_valide(request, pk): 
    part = MyUser.objects.get(id=pk) 
    form = Profils(request.POST or None, request.FILES or None, instance=part)
    if form.is_valid():
        form.save()
        messages.success(request,"la personne a été modifier!")
    return redirect('dashboard_personnel')

