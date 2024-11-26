from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .openaicall import response

@login_required(login_url="login")
def chat(request):
    reponse = ""
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        reponse = response(prompt)
    return render(request, 'chat.html', {'reponse': reponse})