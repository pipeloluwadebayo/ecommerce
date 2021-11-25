from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.utils.text import capfirst
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from .models import Profile


class UserCreateForm(UserCreationForm):

    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',)
        return password2

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'name': 'email', 'id': 'id_email'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control mb-3' })
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control'})

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password',}))

    def __init__(self, request=None, *args, **kwargs):

        self.request = request
        self.user_cache = None
        super(UserLoginForm, self).__init__(*args, **kwargs)


        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class ProfileForm(forms.ModelForm):


    class Meta:
        model = Profile
        fields = ('phone_number', 'address_line_1', 'address_line_2', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs.update(
            {'class': 'form-control mb-3'})
        self.fields['address_line_1'].widget.attrs.update(
            {'class': 'form-control mb-3', 'name': 'email', 'id': 'id_email'})
        self.fields['address_line_2'].widget.attrs.update(
            {'class': 'form-control mb-3' })
        self.fields['state'].widget.attrs.update(
             {'class': 'form-control'})
        self.fields['country'].widget.attrs.update(
             {'class': 'form-control'})


class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = User.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email

class PwdResetConfirmForm(SetPasswordForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = User.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email

    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))

class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    username = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-username', 'readonly': 'readonly'}))

    fullname = forms.CharField(
        label='Fullname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Fullname', 'id': 'form-fullname'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'fullname',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True
