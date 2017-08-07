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


class SaleForm(forms.Form):
    page = forms.CharField(required=False)
    datepicker_start = forms.CharField(label="ex : 07/21/2017")
    datepicker_end = forms.CharField(label="ex : 08/21/2017")
