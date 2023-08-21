import logging

from django.shortcuts import render, redirect
from django.views import View

from users.forms import RegistrationForm
from users.models import User


class SingUpView(View):
    template_name = 'registration/sing-up.html'
    form_class = RegistrationForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(email=email).exists():
                form.add_error('email',
                               'Пользователь с таким email уже существует.')
            else:
                print(email, password)
                user = User(email=email)
                user.set_password(password)
                user.is_active = True
                user.save()
                return redirect('login')

        return render(request, self.template_name, {'form': form})

