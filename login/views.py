from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from beholder.eyeballs import Eye
from .forms import LoginForm


class IndexView(TemplateView):
    template_name = 'login/login.html'

    def get(self, request):
        login_form = LoginForm()
        return render(request, self.template_name, {'login_form': login_form})

    def post(self, request):
        kwargs = request.POST.dict()
        login_form = LoginForm()
        eye = Eye()
        user = authenticate(request, username=kwargs['username'], password=kwargs['password'])

        if user is not None:
            return redirect('login:dashboard')

        else:
            return render(request, self.template_name, {'login_form': login_form, 'kwargs': kwargs,})
