from django.shortcuts import render

# Create your views here.
import datetime
import csv
import json
import pandas as pd

from user.tokens import account_activation_token
from django.http import HttpResponse
from django.shortcuts import render
from root.settings import EMAIL_DEFAULT_SENDER
from django.views import View
from user.forms import SendEmailForm, RegisterForm
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from user.models import CustomUser

# Create your views here.
from user.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect


from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'user/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('home_page')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        # Authenticate the user using the email and password
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        
        user = CustomUser.objects.filter(email=email).first()
        
        if user and user.check_password(password):
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            return super().form_valid(form)
        
        messages.error(self.request, 'Invalid username or password')
        return self.form_invalid(form)


class RegisterPage(generic.FormView):
    form_class=RegisterForm
    success_url=reverse_lazy('login_page')
    template_name='user/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.is_superuser = True 
        user.is_staff = True 
        user.set_password(form.cleaned_data.get('password'))     
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('user/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            # 'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token':account_activation_token.make_token(user),
        })
        send_mail(
            mail_subject,
            message,
            EMAIL_DEFAULT_SENDER,
            [user.email],
            fail_silently=False
            )
       
        response = super().form_valid(form)

       
        return HttpResponse('Please confirm your email address to complete the registration.')
    
class Activate(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # return redirect('home')
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')
    

class SendMail(View):
    sucessfully_sent=False
    def get(self,request,*args,**kwargs):
        form=SendEmailForm()
        context={
            'form':form,
            'sucessfully_sent':self.sucessfully_sent
        }
        return render(request,'user/send_email.html', context)

    def post(self, request,*args, **kwargs):
        form=SendEmailForm(request.POST)
        if form.is_valid():
            subject=form.cleaned_data['subject']
            message=form.cleaned_data['message']
            recipient_list=form.cleaned_data['recipient_list']
            send_mail(subject,message,EMAIL_DEFAULT_SENDER, recipient_list, fail_silently=False)
            self.sucessfully_sent=True
        context={
            'form':form,
            'sucessfully_sent':self.sucessfully_sent
            # Look, we don't have to define sucessfully sent=True in the html file, we should just say succesfully_sent as false in if part and give the form, and 
            # in else part we will give a sucess message!
        }
        return render(request,'user/send_email.html', context)