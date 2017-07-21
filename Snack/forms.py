from django import forms


class ConnectForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class SignUpForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password")
    password_verif = forms.CharField(label="Validation password")
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")
    card_number = forms.CharField(label="Card Number", required=False)
