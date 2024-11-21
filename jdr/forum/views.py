from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def forum_homes(request):
    return render(request, 'home_forum.html', {})