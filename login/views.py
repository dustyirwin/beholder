from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from inventory.models import SessionData
from .forms import LoginForm


class IndexView(TemplateView):
    template_name = 'login/login.html'

    def get(self, request):
        login_form = LoginForm()
        return render(request, self.template_name, {'login_form': login_form})

    def post(self, request):
        kwargs = request.POST.dict()
        login_form = LoginForm()
        user = authenticate(request, username=kwargs['username'], password=kwargs['password'])

        if user is not None:

            if not SessionData.objects.filter(user=kwargs['username']).exists():
                SessionData(
                    user=kwargs['username'],
                    session_id='testing...',
                    data={'market_data': {}}
                ).save()

            return redirect('search:query')

        else:
            return render(request, self.template_name, {'login_form': login_form, 'kwargs': kwargs,})
