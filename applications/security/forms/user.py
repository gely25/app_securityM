from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupForm(forms.ModelForm):
    celular = forms.CharField(label='Celular', required=False)
    correo = forms.EmailField(label='Correo')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'dni']

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('correo')
        user.phone = self.cleaned_data.get('celular')
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user
