from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.views.generic import *
from django.contrib import admin
from django.urls import include, path
from ajouter.views import *
from dashboard.views import *
from .views import index, false
from profil.views import UserEditView, profils
from partner.views import *
from structure.views import Options, details, valide_option_structure, option_structure_valide
from main import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("rajouter/structure",rajout_structure , name='rajoutstructure'),
    path("rajouter/partenaire",rajout_partenaire, name='rajoutpartenaire'),
    path("rajouter/profils",rajout_profils , name='rajoutprofils'),
    path("rajouter/option",rajout_option, name ='rajoutoption'),
    path("", index, name='index'), 
    
    path("profils/user/mastructure/", ma_structure, name='maStructure'),
    path("profils/user/monpartenaire/", mon_partenaire, name='monPartenaire'),
    path("profils/user/modifstructure/<int:pk>", user_structure, name='modifstructure'),
    path("profils/user/modifpartenaire/<int:pk>", user_partenaire, name='modifpartenaire'),
    path('profils/user/partenaire/option/<int:pk>',option_user_partenaire, name='user_option_partenaire'),
    path('profils/user/structure/option/<int:pk>',option_user_structure, name='user_option_structure'),

    path("false/", false, name="false"),
    path('accounts/', include ('django.contrib.auth.urls')), 
    path('profils/', profils, name="profils" ) , 
    path('profils/modifier', UserEditView.as_view(), name='modifprofils') ,    
    path('profils/password', auth_views.PasswordChangeView.as_view(template_name='registration/password.html'), name='password') ,
    path('partenaire/', Partenaire, name="partenaire"),    
    path('partenaire/option/<int:pk>', Partenaire_option, name="optionbase"),
    path('partenaire/<str:slug>', Structure, name='structure'), 
    path('detail/<int:pk>', details, name="detail"),
    path('responsable/structure/<int:pk>', Options, name="responsable"),
    path('responsable/partenaire/<int:pk>', Options_partenaires, name="responsables"),
    path('activate/<uidb64>/<token>', activate, name="activate"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "reset_password.html"), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "password_reset_form.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "password_reset_done.html"), name ='password_reset_complete') 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

htmx_urlpatterns = [
    path("dash/add_option",add_option, name='add-option'),
    path('delete-option/<int:pk>/', delete_option, name='delete-option'),
    path("dash/modifier_option/<int:pk>",modifier_option, name='modif-option'),
    path("dash/modifier_option/valide/<int:pk>",modifier_option_valide, name='modif-option-valide'),
    path("dash/add_option/<int:pk>/", modifier_option, name='rajout-option'),  

    path('delete-partenaire/<int:pk>/', delete_partenaire, name='delete-partenaire'),
    path("dash/add_partenaire",add_partenaire, name='add-partenaire'),
    path("dash/modifier_partenaire/valide/<int:pk>",modifier_partenaire_valide, name='modif-partenaire-valide'),
    path("dash/modifier_partenaire/<int:pk>", modifier_partenaire, name='modif-partenaire'),

    path('delete-structure/<int:pk>/', delete_structure, name='delete-structure'),
    path("dash/add_structure",add_structure, name='add-structure'),
    path("dash/modifier_structure/valide/<int:pk>",modifier_structure_valide, name='modif-structure-valide'),
    path("dash/modifier_structure/<int:pk>", modifier_structure, name='modif-structure'),

    path('delete-personnel/<int:pk>/', delete_personnel, name='delete-personnel'),
    path("dash/add_personnel",add_personnel, name='add-personnel'),
    path("dash/modifier_personnel/valide/<int:pk>",modifier_personnel_valide, name='modif-personnel-valide'),
    path("dash/modifier_personnel/<int:pk>", modifier_personnel, name='modif-personnel'),
    
    path('check_username/', check_username, name='check-username'),
    path('check_email/', check_email, name='check-email'),
    path('check_tel/',check_tel, name='check_tel'),
    path('check_nameStructure/',check_name_struture, name='nameStructure'),
    path('check_password/',check_password, name='check_password'),
    path('check_villePartenaire/', check_ville_partenaire, name="check_villePartenaire"),
    path('check_slug/', check_slug, name="check_slug"), 

    path('valide/<int:pk>',option_partenaire_valide, name="valide"),
    path('structures/valide/<int:pk>',option_structure_valide, name="valide_structure"),
    path('structures/option/<int:pk>', valide_option_structure, name="valide_structure_option"),
    
    path('cherche_structure/',cherche_structure, name="cherche-structure"),
    path('cherche_personnel/',cherche_personnel, name="cherche-personnel"),
    path('cherche_partenaire/',cherche_partenaire, name="cherche-partenaire"),
    path('cherche_option/',cherche_option, name="cherche-option"),

    path('checkbox/valide/partenaire/<int:pk>',dash_valide_partenaire,name='valide_actif_partenaire'),
    path('checkbox/valide/structure/<int:pk>',dash_valide_structure,name='valide_actif_structure'),
   
]
dashboard_urlpatterns = [
    path("dash/", dashboard, name='dashboard'),
    path("dash/personnel", dashboard_personnel, name='dashboard_personnel'),
    path("dash/partenaire", dashboard_partenaire, name='dashboard_partenaire'),
    path("dash/structure", dashboard_structure, name='dashboard_structure'),    
    path("dash/option", dashboard_option, name='dashboard_option'),  
]
urlpatterns += htmx_urlpatterns 

urlpatterns += dashboard_urlpatterns