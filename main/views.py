from django.shortcuts import render

def index(request):
    return render(request,'index.html')

def recherche(request):
     return render(request,'recherche.html')
    
def false(request):
    return render(request,"false.html")


