from .forms import UserCreateForm, UserLoginForm, UserEditForm, ProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import auth, User
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes








def user_login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username, password=password)


        if user is not None:
            auth.login(request, user)
            return redirect('/')


        else:
            return HttpResponse("Invalid Credentials")

    else:
        return render(request, 'account/login.html', {'form': UserLoginForm})



def register_user(request):
	if request.method == "POST":
		register_form = UserCreateForm(request.POST)
		if register_form.is_valid():
		    user = register_form.save()
		    login(request, user)
		    return redirect("shop:store")
		else:
		    return HttpResponse("Form is not valid")
	else:
	    register_form = UserCreateForm()
	    return render (request, 'account/register.html', {'form':register_form})

def dashboard(request):

    return render(request,
                  'account/dashboard.html',
                  {'section': 'profile'})

def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'account/edit_profile.html', {'user_form': user_form})



def delete_profile(request):
    user = User.objects.get(username=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('accounts:confirm_delete')


def checkout(request):
        billing_form = ProfileForm
        return render (request, 'account/checkout.html', {'form':billing_form})


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "account/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'pipeloluwadebayo.pythonanywhere.com',
					"site_name": 'https://pipeloluwadebayo.pythonanywhere.com',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="account/password_reset.html", context={"password_reset_form":password_reset_form})
