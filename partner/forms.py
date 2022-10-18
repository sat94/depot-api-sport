from django import forms
from accounts.models import partenaire

class Option_par_id(forms.ModelForm):
      class Meta:
        model = partenaire 
        fields = {
            "option",            
        }
        labels = {
            "option": "",        
       }
        widgets = {
             "option": forms.CheckboxSelectMultiple(),             
        }

class Actif_par_id(forms.ModelForm):
      class Meta:
        model = partenaire 
        fields = {            
            "actif"
        }
        labels = {
            "actif": "",        
        }
        widgets = {            
             "actif": forms.CheckboxInput(),
        }
 