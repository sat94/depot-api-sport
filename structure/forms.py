from accounts.models import option, structure
from django import forms

class Option_structure(forms.ModelForm):
      def __init__(self, *args, **kwargs):
          super(Option_structure, self).__init__(*args, **kwargs)
          part_ids = [option.id for option in self.instance.part.option.all()]
          CUSTOM_QUERYSET_SALLE = option.objects.exclude(id__in=part_ids)
          self.fields['option'].queryset = CUSTOM_QUERYSET_SALLE
      class Meta:
        model = structure 
        fields = {
            "option",            
        }
        labels = {
            "option": "",        
       }
        widgets = {
             "option": forms.CheckboxSelectMultiple(),             
        }


class Actif_structure(forms.ModelForm):
      class Meta:
        model = structure
        fields = {            
            "actif"
        }
        labels = {
            "actif": "",        
       }
        widgets = {            
             "actif": forms.CheckboxInput(),
        }
