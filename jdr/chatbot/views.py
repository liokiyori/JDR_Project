from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .openaicall import response
from .models import Conversation

@login_required(login_url="login")
def chat(request):
    reponse = ""
    user = request.user
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        reponse = response(user, prompt)
        Conversation.objects.create(user=request.user, prompt=prompt, response=reponse)
        
    conversations = Conversation.objects.filter(user=request.user).order_by('timestamp')
    return render(request, 'chat.html', {'reponse': reponse, 'conversations': conversations})
