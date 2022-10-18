from accounts.models import MyUser
from django.contrib.auth.forms import UserChangeForm
import os

def delete_previous_picture(previous,new):
    if previous != new:
        os.remove(previous)
        return True
    return False    

class Profils(UserChangeForm):
    password = None
    def save(self, commit=True):
        delete_previous_picture(
            self.initial['photo'].path, 
            self.instance.photo.path
        )
        instance = super(Profils, self).save(commit=False)
        if commit:
            instance.save()
        return instance
    
    class Meta:
        model = MyUser
        fields = [
            "username",
            "nom", 
            "prenom",               
            "adresse", 
            "CodePostal", 
            "ville",
            "photo",
            "permission",                
            ]
        labels = {
            "username": "Nom d'utilisateur",
            "nom": " Votre nom",
            "prenom": "Votre prénom",
            "email" : "Votre mail",  
            "CodePostal" : "Votre code Postale",
            "ville" : "Votre ville",          
            "photo" : "Votre photo (facultatif)",         
        }  
        

