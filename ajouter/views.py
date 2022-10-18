from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .token import account_activation_token
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import get_user_model
from accounts.models import option, partenaire, structure
from ajouter.forms import AjoutoptionForm, AjoutStrutureForm,SignupForm, AjoutPartenaireForm
from django.core.mail import EmailMessage
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def rajout_structure(request):
    context={}
    form = AjoutStrutureForm()
    context["form"]= form 
    return render(request, 'rajoutstructure.html', context = context)

@login_required
def rajout_partenaire(request):
    context={}
    form =  AjoutPartenaireForm() 
    context["form"]= form       
    return render(request, 'rajoutpartenaire.html', context = context)

@login_required
def activate(request, uidb64, token):
    User= get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True      
        user.save()          
        messages.success(request, "Votre compte est activé. Maintenant vous pouvez vous connecté a votre compte.")
        return redirect('index')
    return redirect('false')

@login_required
def active_Email(request, user, email, nom, password, permission):
    subject = "Bienvenu sur API-SPORT"
    message = render_to_string("template_activate_account.html",{
        'user': nom,
        'login': user,
        'password': password,
        'status': permission,
        'domain': get_current_site(request).domain,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })     
    emails = EmailMessage(subject, message, to=[email])
    if emails.send():
        messages.success(request, f"Bienvenue {nom}, veillez regardez dans vos mails {email} dans le mail vous trouverez un lien de validation, veillez cliquez sur le lien pour complèter le dossier.Note: Oubliez pas de regarder dans vos courriers indésirable.")
    else:
        messages.error(request, f'Nous avons pas pu vous envoyer un mail vers {email}, vérifier que vous tapez email correctement. ')

@login_required
def rajout_profils(request):
    context = {}
    form = SignupForm()
    context["form"]= form
    return render(request, "signup.html", context= context)

@login_required
def add_personnel(request):    
    if request.method == "POST":
        form = SignupForm(request.POST,request.FILES)         
        if form.is_valid():                   
            email = request.POST.get('email')
            password = request.POST.get('password1')
            nom = request.POST.get('prenom')
            permission = request.POST.get('permission') 
            user = form.save(commit=False)  
            if permission == f"Commercial": 
                user.is_admin = True
                user.commercial = True
            user.is_active = False           
            user.save()
            active_Email(request, user, email, nom, password, permission) 
            return redirect('dashboard_personnel')
        else:
            form = SignupForm() 
    return render(request, "signup.html",{"form": form})  

@login_required
def rajout_option(request):
    form = AjoutoptionForm()
    return render(request, "rajoutoption.html",{"form": form})

# HTMX ###################################################################

@login_required   
def add_option(request):
    if request.method == "POST":
        form = AjoutoptionForm(request.POST)         
        if form.is_valid():
            form.save()
            messages.success(request," L'option a bien été rajouter ! ")
            return redirect('dashboard_option')
        else:
            form = AjoutoptionForm() 
    return render(request, "rajoutoption.html",{"form": form}) 

@login_required
def check_username(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("<div style='color:#E53517; font-size: 20px;'>Le pseudo est déjà utiliser")
    else:
        return HttpResponse("<div style='color:#00ff1A; font-size: 20px;'>Le pseudo est utilisable.")

@login_required
def check_email(request):
    email = request.POST.get('email')
    if get_user_model().objects.filter(email=email).exists():
        return HttpResponse("<div style='color: red; font-size: 20px;'>L'email est déjà utiliser")
    else:
        return HttpResponse("<div style='color:#00ff1A; font-size: 20px;'>L'email est utilisable.")

@login_required
def check_tel(request):
    numberPhone = request.POST.get('numberPhone')
    structures = structure.objects.all()
    partenaires = partenaire.objects.all()
    if structures.filter(numberPhone=numberPhone).exists() or partenaires.filter(numberPhone=numberPhone).exists():
        return HttpResponse("<div style='color: red; font-size: 20px;'>Le téléphone est déjà utiliser")
    else:
        return HttpResponse("<div style='color:#00ff1A; font-size: 20px;'>Le téléphone est utilisable.")

@login_required
def check_name_struture(request):
    nom = request.POST.get('nom')
    structures = structure.objects.all()
    if structures.filter(nom=nom).exists():
        return HttpResponse("<div style='color: red; font-size: 20px;'>Le nom est déjà utiliser")
    else:
        return HttpResponse("<div style='color:#00ff1A; font-size: 20px;'>Le nom est utilisable.")

@login_required
def check_password(request):
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    if password1 != password2 or password2 != password1:
        return HttpResponse("<div style='color: red; font-size: 20px;'>les mots passes sont pas pareil")
    return HttpResponse("<div style='color:#00ff1A; font-size: 20px;'>les mots passes sont pareil")    

@login_required
def check_ville_partenaire(request):
    ville = request.POST.get('ville')
    structures = partenaire.objects.all()
    if structures.filter(ville=ville).exists():
        return HttpResponse("<div style='color: red; font-size: 20px;'>La ville est déjà utiliser")
    else:
        return HttpResponse("<div style='color:#00ff1A; font-size: 20px;'>La ville est utilisable.")

@login_required   
def check_slug(request):
    slug = request.POST.get('slug')
    options = option.objects.all()
    if options.filter(slug=slug).exists():
        return HttpResponse("<div style='color: red; font-size: 20px;'>Le titre est déjà utiliser")
    else:
        return HttpResponse("<div style='color:#00ff1A; font-size: 20px;'>Le titre est utilisable.") 

