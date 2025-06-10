
from django.shortcuts import redirect, render
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class SignupForm(UserCreationForm):
    celular = forms.CharField(label='Celular', required=False)
    correo = forms.EmailField(label='Correo')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'dni']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('correo')
        user.phone = self.cleaned_data.get('celular')
        if commit:
            user.save()
        return user


# ----------------- Cerrar Sesion -----------------
@login_required
def signout(request):
    logout(request)
    return redirect("security:signin")

# # ----------------- Iniciar Sesion -----------------
def signin(request):
    
    data = {"title": "Login",
            "title1": "Inicio de Sesión"}
    if request.method == "GET":
        # Obtener mensajes de éxito de la cola de mensajes
        success_messages = messages.get_messages(request)
        return render(request, "security/auth/signin.html", {
            "form": AuthenticationForm(),
            "success_messages": success_messages,  # Pasar mensajes de éxito a la plantilla
            **data
        })
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    # Ensure the superuser belongs to all groups
                    all_groups = Group.objects.all()
                    user.groups.set(all_groups)
                # Permitir iniciar sesión al superusuario incluso sin grupos
                if user.is_superuser or user.groups.exists():
                    login(request, user)
                    return redirect("dashboard")
                else:
                    return render(request, "security/auth/signin.html", {
                        "form": form,
                        "error": "El usuario no tiene grupos asignados",
                        **data
                    })
            else:
                return render(request, "security/auth/signin.html", {
                    "form": form,
                    "error": "El usuario o la contraseña son incorrectos",
                    **data
                })
        else:
            return render(request, "security/auth/signin.html", {
                "form": form,
                 "error": "Datos invalidos",
                **data
            })


# ----------------- Registro de Usuario -----------------
def signup(request):
    data = {
        "title": "Registro",
        "title1": "Crear Cuenta",
        "title2": "Registro de Usuario",
    }

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado correctamente")
            return redirect("security:signin")
    else:
        form = SignupForm()

    return render(request, "security/auth/signup.html", {"form": form, **data})
