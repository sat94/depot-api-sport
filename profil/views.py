from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from .forms import Profils
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


@login_required
def profils(request):
    return render(request, 'profils.html')


class UserEditView(SuccessMessageMixin, UpdateView):
    form_class = Profils
    template_name = 'modifprofils.html'
    sucess_message = 'Le profils a bien été modifier !'
    success_url = reverse_lazy('profils') 
     
    def get_object(self):    
        return self.request.user

    
