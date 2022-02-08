from django.http import request
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.utils.crypto import get_random_string
from django.core.signing import TimestampSigner
from django.core.signing import BadSignature, SignatureExpired
from files.forms import FileForm, LinkForm, PasswordForm
from .models import File, Link, MyUser
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.
class HomeView(ListView):

    def get(self, request):
        print(request.META.get('HTTP_USER_AGENT', ''))
        return render(request, 'home.html', {})

class FileView(ListView):
  
    def get(self, request):
        try:
            if request.session['user'] == None:
                return redirect('home')
        except:
            return redirect('home')
        form = FileForm()
        return render(request, 'upload_file.html', {'form':form})

    def post(self, request):
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            file = request.FILES['file']
            password = get_random_string(10)
            user = User.objects.get(username = request.session['user'])
            user = MyUser.objects.get(user=user)
            file_data = File(user = user, name=name, file=file, password=password)
            file_data.save()
            unique_link = file_data.get_absolute_url()
            form = FileForm()
            return render(request, 'upload_file.html', { 'password':file_data.password, 'unique_link':unique_link, 'form':form})
            
        return render(request, 'upload_file.html')


class LinkView(ListView):
    def get(self, request):
        try:
            if request.session['user'] == None:
                return redirect('home')
        except:
            return redirect('home')
        form = LinkForm()
        return render(request, 'upload_link.html', {'form':form})

    def post(self, request):
        
        form = LinkForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            link = form.cleaned_data['link']
            password = get_random_string(10)
            user = User.objects.get(username = request.session['user'])
            user = MyUser.objects.get(user=user)
            link_data = Link(user = user, name=name, link=link, password=password)
            link_data.save()
            unique_link = link_data.get_absolute_url()
            form = LinkForm()
            return render(request, 'upload_link.html', { 'password':link_data.password, 'unique_link':unique_link, 'form':form})
            
        return render(request, 'upload_link.html')


class SecureLinkView(ListView):
    def get(self, request, signed_pk):
        try:
            pk = Link.security.unsign(signed_pk, max_age=86400)
            link_obj = Link.objects.get(pk=pk)
        except(BadSignature, SignatureExpired, Link.DoesNotExist):
            messages.warning(request, "Link has expired or is Invalid!")
            return render(request, 'secure_link.html')
        form = PasswordForm()
        return render(request, 'secure_link.html', {'form':form, 'signed_pk':signed_pk})

    def post(self, request, signed_pk):
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            try:
                link_obj = Link.objects.get(password=password)
                link_obj.no_of_correct_attempts += 1
                link_obj.save()
                return render(request, 'secure_link.html', {'link':link_obj.link})
            except Link.DoesNotExist:
                messages.warning(request, "Invalid Link")
                
                
        return render(request, 'secure_link.html', {'form':form, 'signed_pk':signed_pk})


class SecureFileView(ListView):
    def get(self, request, signed_pk):
        try:
            pk = File.security.unsign(signed_pk, max_age=86400)
            file_obj = File.objects.get(pk=pk)
        except(BadSignature, SignatureExpired, File.DoesNotExist):
            messages.warning(request, "Link has expired or is Invalid!")
            return render(request, 'secure_file.html')
        form = PasswordForm()
        return render(request, 'secure_file.html', {'form':form, 'signed_pk':signed_pk})

    def post(self, request, signed_pk):
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            try:
                file_obj = File.objects.get(password=password)
                file_obj.no_of_correct_attempts += 1
                file_obj.save()
                return render(request, 'secure_file.html', {'file':file_obj.file})
            except File.DoesNotExist:
                messages.warning(request, "Invalid Link")
                
        return render(request, 'secure_file.html', {'form':form, 'signed_pk':signed_pk})




class LoginView(ListView):

    def get(self, request):
        return redirect('home')

    def post(self, request):
        username = request.POST['uname']
        password = request.POST['pwd']
        try:
            user = User.objects.get(username=username, password=password)
            user = MyUser.objects.get(user=user)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            user.agent = user_agent
            user.save()
            request.session['user'] = user.user.username
            request.session['agent'] = user_agent
            messages.success(request, "Login Successful")
            return redirect('home')

        except MyUser.DoesNotExist:
            messages.warning(request, "Invalid Login Details. Please try again")
            return redirect('home')

class LogoutView(ListView):
    def get(self, request):
        try:
            del request.session['user']
            return redirect('home')
        except:
            return redirect('home')

class SignUpView(ListView):
    def get(self, request):
        
        return redirect('home')

    def post(self, request):
        '''
        Create account system
        '''
        user_name = request.POST['uname']
        pwd1 = request.POST['pwd1']
        pwd2 = request.POST['pwd2']
        print(user_name)
        print(pwd1)
        print(pwd2)
        if pwd1 == pwd2:
            try:
                add_user = User(username=user_name, password=pwd1)
                add_user.save()
                my_user = MyUser(user=add_user, agent=None)
                my_user.save()
                messages.success(request, 'Account has been created successfully.')
            except:
                messages.warning(request, 'Signup Failed. Try Again!')
            return redirect('home')
        else:
            messages.warning(request, 'Passwords are not same.')
            return redirect('home')