from accounts.models import MyUser, partenaire, structure
from django.contrib.auth.forms import UserChangeForm
from django import forms
import os

def delete_previous_picture(previous,new):
    if previous != new:
        os.remove(previous)
        return True
    return False 
 
class ModifPartenaire(UserChangeForm):    
    def save(self, commit=True):
        delete_previous_picture(
            self.initial['photo'].path, 
            self.instance.photo.path
        )
        instance = super(ModifPartenaire, self).save(commit=False)
        if commit:
            instance.save()
        return instance   
    class Meta:
        model = partenaire
        fields = (
            "ville",           
            "description",
            "numberPhone",          
            "photo",            
        )
        labels = {
            "numberPhone": "Téléphone",        
       }
        widgets = {
            "description": forms.Textarea(
                attrs={
                    'placeholder':"Vous pouvez rentrer jusqu'à 70 caractères.",
                    'rows' : 5,
                    'cols' : 35,
                }
            ),          
        }  

class ModifStructureForm(UserChangeForm):
    def save(self, commit=True):
        delete_previous_picture(
            self.initial['photo'].path, 
            self.instance.photo.path
        )
        instance = super(ModifStructureForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance
    class Meta:
        model = structure
        fields = [
            "nom",           
            "adresse",
            "membre",
            "numberPhone",        
            "photo",
            "piscine", 
            "haman",
            "sauna",                                    
        ]
        labels = {
            "user" : "le responsable de la structure (facultatif)",        
            "nom": "Nom de la structure",
            "adresse": "Adresse",
            "numberPhone": "Téléphone",  
            "membre"  : "Nombre de membres",                
        }
        widgets = {          
            "adresse": forms.Textarea(attrs={"rows" : 2, "cols": 23}),
        }  
       
class Actif_user(forms.ModelForm):
      class Meta:
        model = MyUser
        fields = {
            "is_active",            
        }
        widgets = {
             "is_active": forms.CheckboxInput(),             
        }

