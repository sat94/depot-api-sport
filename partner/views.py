from django.shortcuts import redirect, render
from accounts.models import option, partenaire, structure
from django.contrib.auth.decorators import login_required
from partner.forms import Actif_par_id, Option_par_id
from django.contrib import messages

@login_required
def Partenaire(request):
    partenaires = partenaire.objects.all()  
    context= {"partenaires" : partenaires}  
    return render(request, "partner.html",context)

@login_required
def Structure(request, slug):
    structures = structure.objects.filter(slug__iexact= slug)      
    context= {
        "structures" : structures,                   
    }
    return render(request, "structure.html",context)

def Partenaire_option(request, pk):
    partenaires = partenaire.objects.get(id=pk)
    listoptionid = [option_partenaire.id for option_partenaire  in partenaires.option.all()]
    form = Option_par_id(instance=partenaires)  
    forms = Actif_par_id(instance=partenaires)
    options = option.objects.all()  
    structures = structure.objects.filter(part=pk)
    if request.method == "POST":
        form = Option_par_id(request.POST, instance=partenaires)           
        if form.is_valid():             
            form.save()
            messages.success(request,"les options du partenaire ont été modifier!")
            return redirect('optionbase', pk=partenaires.id)
            
    context= { "partenaires" : partenaires,
               "options" : options,
               "structures": structures,
               "listoptionid" : listoptionid,
               "form": form,
               "forms": forms                              
    }
    return render(request,"optionPartenaire.html",context)


def option_partenaire_valide(request, pk): 
    partenaires = partenaire.objects.get(id=pk) 
    form = Actif_par_id(request.POST, instance=partenaires) 
    if request.method == "POST":
        form = Actif_par_id(request.POST, instance=partenaires)          
        if form.is_valid():          
            form.save()
            messages.success(request,"le partenaire est modifier!")
            return redirect('optionbase', pk=partenaires.id )

@login_required
def Options_partenaires(request, pk):
    partenaires = partenaire.objects.get(id=pk)
    context= {
        "partenaires" : partenaires
    }
    return render(request,"user_resp.html", context)
  
    
