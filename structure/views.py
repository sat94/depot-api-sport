from django.shortcuts import redirect, render
from accounts.models import partenaire, structure, option
from django.contrib.auth.decorators import login_required
from structure.forms import Actif_structure, Option_structure
from django.contrib import messages

@login_required
def details(request, pk):
    structures = structure.objects.get(id=pk) 
    form = Actif_structure(instance=structures) 
    forms = Option_structure(instance=structures)
    options = option.objects.all().order_by()
    partenaires = partenaire.objects.get(id=structures.part.id)
    listoptionpartenaire = [option_partenaire.id for option_partenaire  in partenaires.option.all()]
    listoptionstructure = [option_structure.id for option_structure  in structures.option.all()]
    if request.method == "POST": 
        form = Option_structure(request.POST, instance=structures)
        if form.is_valid():
           messages.success(request,"les options de la structure ont été modifier!")
           form.save()
        return redirect('detail', pk=structures.id)
      
    context = {
        "structure" : structures,
        "options" : options, 
        "listoptionpartenaire" : listoptionpartenaire,
        "listoptionstructure" : listoptionstructure,
        "form": form,  
        "forms" : forms,
    }
    return render(request, "detail.html", context)
    
@login_required
def Options(request, pk):
    structures = structure.objects.get(id=pk)
    context= {
        "structure" : structures
    }
    return render(request, "option.html", context)

def valide_option_structure(request, pk): 
    structures = structure.objects.get(id=pk) 
  

def option_structure_valide(request, pk): 
    structures = structure.objects.get(id=pk)   
    if request.method == "POST":
        form = Actif_structure(request.POST, instance=structures)          
        if form.is_valid():          
            form.save()
            messages.success(request,"l'option de la structure a été modifier!")
            return redirect('detail', pk=structures.id)
   

    






