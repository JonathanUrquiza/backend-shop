from django.http import JsonResponse
from .models import User

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email, password=password).first()
        if user:
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'message': 'Login failed'}, status=401)

def user_register(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create(name=name, lastname=lastname, email=email, password=password)  # pylint: disable=no-member
        return JsonResponse({'message': 'Register successful'})
    

def user_logout(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email, password=password).first()
        if user:
            return JsonResponse({'message': 'Logout successful'})
        else:
            return JsonResponse({'message': 'Logout failed'}, status=401)
    else:
        return JsonResponse({'message': 'Logout failed'}, status=401)

def user_profile(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        password = request.GET.get('password')
        user = User.objects.filter(email=email, password=password).first()
        if user:
            return JsonResponse({'message': 'Profile successful'})
        else:
            return JsonResponse({'message': 'Profile failed'}, status=401)

def user_profile_edit(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email, password=password).first()
        if user:
            return JsonResponse({'message': 'Profile edit successful'})
        else:
            return JsonResponse({'message': 'Profile edit failed'}, status=401)
    else:
        return JsonResponse({'message': 'Profile edit failed'}, status=401)

def user_profile_delete(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email, password=password).first()
        if user:
            return JsonResponse({'message': 'Profile delete successful'})
        else:
            return JsonResponse({'message': 'Profile delete failed'}, status=401)
    else:
        return JsonResponse({'message': 'Profile delete failed'}, status=401)


def user_profile_change_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email, password=password).first()
        if user:
            return JsonResponse({'message': 'Profile change password successful'})
        else:
            return JsonResponse({'message': 'Profile change password failed'}, status=401)
    else:
        return JsonResponse({'message': 'Profile change password failed'}, status=401)

def user_profile_change_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email, password=password).first()
        if user:
            return JsonResponse({'message': 'Profile change email successful'})
        else:
            return JsonResponse({'message': 'Profile change email failed'}, status=401)
    else:
        return JsonResponse({'message': 'Profile change email failed'}, status=401)

def user_profile_change_username(request):
    if request.method == 'POST':
        return JsonResponse({'message': 'Profile change username successful'})
    else:
        return JsonResponse({'message': 'Profile change username failed'}, status=401)

def user_profile_change_avatar(request):
    if request.method == 'POST':
        return JsonResponse({'message': 'Profile change avatar successful'})
    else:
        return JsonResponse({'message': 'Profile change avatar failed'}, status=401)

def user_profile_change_background(request):
    if request.method == 'POST':
        return JsonResponse({'message': 'Profile change background successful'})
    else:
        return JsonResponse({'message': 'Profile change background failed'}, status=401)

def user_profile_change_theme(request):
    if request.method == 'POST':
        return JsonResponse({'message': 'Profile change theme successful'})
    else:
        return JsonResponse({'message': 'Profile change theme failed'}, status=401)

def user_profile_change_language(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # language = request.POST.get('language')  # No se usa porque el modelo User no tiene campo 'language'
        user = User.objects.filter(email=email, password=password).first()
        if user:
            # Nota: El modelo User no tiene un campo 'language' definido.
            # Si necesitas guardar el idioma, primero debes agregarlo al modelo.
            # Por ahora, solo verificamos que el usuario existe.
            return JsonResponse({'message': 'Profile change language successful'})
        else:
            return JsonResponse({'message': 'Profile change language failed'}, status=401)
    else:
        return JsonResponse({'message': 'Profile change language failed'}, status=401)

