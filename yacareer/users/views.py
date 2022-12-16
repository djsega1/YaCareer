from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Profile


def signup(request):
    pass


def user_list(request):
    users = Profile.objects.published()
    context = {'items': users}
    return render(request, "users/user_list.html", context)


def user_detail(request, pk):
    user = get_object_or_404(Profile.objects.published(), pk=pk)
    context = {'item': user}
    return render(request, "users/user_detail.html", context)


@login_required(login_url='/users/login')
def profile(request):
    pass
