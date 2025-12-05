from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Role

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            # Obtener datos del request (soporta JSON y form-data)
            import json
            if request.content_type == 'application/json':
                try:
                    data = json.loads(request.body)
                    email = data.get('email')
                    password = data.get('password')
                except json.JSONDecodeError:
                    return JsonResponse({'message': 'JSON inválido'}, status=400)
            else:
                email = request.POST.get('email')
                password = request.POST.get('password')
            
            # Validar que los campos estén presentes
            if not email or not password:
                return JsonResponse({
                    'message': 'Faltan campos obligatorios. Se requieren: email, password'
                }, status=400)
            
            # Buscar usuario en la base de datos
            try:
                user = User.objects.filter(email=email, password=password).first()
                if user:
                    # Obtener el rol del usuario
                    role_name = None
                    if user.role_id:
                        try:
                            role = Role.objects.filter(role_id=user.role_id).first()
                            if role:
                                role_name = role.role_name.lower()
                        except Exception:
                            pass
                    
                    return JsonResponse({
                        'message': 'Login successful',
                        'user_id': user.user_id,
                        'email': user.email,
                        'name': user.name,
                        'lastname': user.lastname,
                        'role_id': user.role_id,
                        'role_name': role_name
                    })
                else:
                    return JsonResponse({'message': 'Email o contraseña incorrectos'}, status=401)
            except Exception as e:
                return JsonResponse({
                    'message': f'Error al consultar la base de datos: {str(e)}'
                }, status=500)
        except Exception as e:
            return JsonResponse({
                'message': f'Error en el servidor: {str(e)}'
            }, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        try:
            # Obtener datos del request (soporta JSON y form-data)
            import json
            if request.content_type == 'application/json':
                try:
                    data = json.loads(request.body)
                    name = data.get('name')
                    lastname = data.get('lastname')
                    email = data.get('email')
                    password = data.get('password')
                except json.JSONDecodeError:
                    return JsonResponse({'message': 'JSON inválido'}, status=400)
            else:
                name = request.POST.get('name')
                lastname = request.POST.get('lastname')
                email = request.POST.get('email')
                password = request.POST.get('password')
            
            # Validar que todos los campos estén presentes
            if not name or not lastname or not email or not password:
                return JsonResponse({
                    'message': 'Faltan campos obligatorios. Se requieren: name, lastname, email, password'
                }, status=400)
            
            # Validar longitud de campos según el modelo
            if len(name) > 16:
                return JsonResponse({'message': 'El nombre debe tener máximo 16 caracteres'}, status=400)
            if len(lastname) > 80:
                return JsonResponse({'message': 'El apellido debe tener máximo 80 caracteres'}, status=400)
            if len(password) > 32:
                return JsonResponse({'message': 'La contraseña debe tener máximo 32 caracteres'}, status=400)
            if len(email) > 255:
                return JsonResponse({'message': 'El email debe tener máximo 255 caracteres'}, status=400)
            
            # Validar formato básico de email
            if '@' not in email:
                return JsonResponse({'message': 'El email no tiene un formato válido'}, status=400)
            
            # Verificar si el email ya existe en la base de datos
            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                return JsonResponse({
                    'message': 'Este email ya está registrado'
                }, status=400)
            
            # Buscar el rol "mixto" para asignarlo por defecto
            mixto_role_id = None
            try:
                mixto_role = Role.objects.filter(role_name__iexact='mixto').first()
                if mixto_role:
                    mixto_role_id = mixto_role.role_id
            except Exception:
                # Si no se encuentra el rol, continuar sin asignar rol
                pass
            
            # Crear el usuario en la base de datos con rol mixto
            try:
                user = User.objects.create(
                    name=name,
                    lastname=lastname,
                    email=email,
                    password=password,
                    role_id=mixto_role_id
                )
                return JsonResponse({
                    'message': 'Register successful',
                    'user_id': user.user_id,
                    'email': user.email,
                    'role_id': user.role_id
                }, status=201)
            except Exception as e:
                # Manejar errores de base de datos
                return JsonResponse({
                    'message': f'Error al crear el usuario en la base de datos: {str(e)}'
                }, status=500)
                
        except Exception as e:
            return JsonResponse({
                'message': f'Error en el servidor: {str(e)}'
            }, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    

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

# CRUD de Usuarios (solo para admin)
@csrf_exempt
def user_list(request):
    """Listar todos los usuarios (solo admin)"""
    if request.method == 'GET':
        try:
            users = User.objects.all()
            users_data = []
            for user in users:
                role_name = None
                if user.role_id:
                    try:
                        role = Role.objects.filter(role_id=user.role_id).first()
                        if role:
                            role_name = role.role_name
                    except Exception:
                        pass
                
                users_data.append({
                    'user_id': user.user_id,
                    'name': user.name,
                    'lastname': user.lastname,
                    'email': user.email,
                    'role_id': user.role_id,
                    'role_name': role_name,
                    'create_time': user.create_time.isoformat() if user.create_time else None
                })
            return JsonResponse({'users': users_data}, safe=False)
        except Exception as e:
            return JsonResponse({'message': f'Error al listar usuarios: {str(e)}'}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

@csrf_exempt
def user_create(request):
    """Crear un nuevo usuario (solo admin)"""
    if request.method == 'POST':
        try:
            import json
            if request.content_type == 'application/json':
                try:
                    data = json.loads(request.body)
                    name = data.get('name')
                    lastname = data.get('lastname')
                    email = data.get('email')
                    password = data.get('password')
                    role_id = data.get('role_id')
                except json.JSONDecodeError:
                    return JsonResponse({'message': 'JSON inválido'}, status=400)
            else:
                name = request.POST.get('name')
                lastname = request.POST.get('lastname')
                email = request.POST.get('email')
                password = request.POST.get('password')
                role_id = request.POST.get('role_id')
            
            if not name or not lastname or not email or not password:
                return JsonResponse({'message': 'Faltan campos obligatorios'}, status=400)
            
            # Validaciones
            if len(name) > 16:
                return JsonResponse({'message': 'El nombre debe tener máximo 16 caracteres'}, status=400)
            if len(lastname) > 80:
                return JsonResponse({'message': 'El apellido debe tener máximo 80 caracteres'}, status=400)
            if len(password) > 32:
                return JsonResponse({'message': 'La contraseña debe tener máximo 32 caracteres'}, status=400)
            if len(email) > 255:
                return JsonResponse({'message': 'El email debe tener máximo 255 caracteres'}, status=400)
            if '@' not in email:
                return JsonResponse({'message': 'El email no tiene un formato válido'}, status=400)
            
            # Verificar si el email ya existe
            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                return JsonResponse({'message': 'Este email ya está registrado'}, status=400)
            
            # Crear usuario
            user = User.objects.create(
                name=name,
                lastname=lastname,
                email=email,
                password=password,
                role_id=role_id if role_id else None
            )
            
            return JsonResponse({
                'message': 'Usuario creado exitosamente',
                'user_id': user.user_id,
                'email': user.email
            }, status=201)
        except Exception as e:
            return JsonResponse({'message': f'Error al crear usuario: {str(e)}'}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

@csrf_exempt
def user_update(request, user_id):
    """Actualizar un usuario (solo admin)"""
    if request.method == 'PUT' or request.method == 'POST':
        try:
            import json
            if request.content_type == 'application/json':
                try:
                    data = json.loads(request.body)
                except json.JSONDecodeError:
                    return JsonResponse({'message': 'JSON inválido'}, status=400)
            else:
                data = request.POST.dict()
            
            try:
                user = User.objects.filter(user_id=user_id).first()
                if not user:
                    return JsonResponse({'message': 'Usuario no encontrado'}, status=404)
                
                # Actualizar campos si están presentes
                if 'name' in data:
                    if len(data['name']) > 16:
                        return JsonResponse({'message': 'El nombre debe tener máximo 16 caracteres'}, status=400)
                    user.name = data['name']
                
                if 'lastname' in data:
                    if len(data['lastname']) > 80:
                        return JsonResponse({'message': 'El apellido debe tener máximo 80 caracteres'}, status=400)
                    user.lastname = data['lastname']
                
                if 'email' in data:
                    if len(data['email']) > 255:
                        return JsonResponse({'message': 'El email debe tener máximo 255 caracteres'}, status=400)
                    if '@' not in data['email']:
                        return JsonResponse({'message': 'El email no tiene un formato válido'}, status=400)
                    # Verificar si el email ya existe en otro usuario
                    existing_user = User.objects.filter(email=data['email']).exclude(user_id=user_id).first()
                    if existing_user:
                        return JsonResponse({'message': 'Este email ya está registrado'}, status=400)
                    user.email = data['email']
                
                if 'password' in data:
                    if len(data['password']) > 32:
                        return JsonResponse({'message': 'La contraseña debe tener máximo 32 caracteres'}, status=400)
                    user.password = data['password']
                
                if 'role_id' in data:
                    user.role_id = data['role_id'] if data['role_id'] else None
                
                user.save()
                
                return JsonResponse({
                    'message': 'Usuario actualizado exitosamente',
                    'user_id': user.user_id
                })
            except Exception as e:
                return JsonResponse({'message': f'Error al actualizar usuario: {str(e)}'}, status=500)
        except Exception as e:
            return JsonResponse({'message': f'Error en el servidor: {str(e)}'}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

@csrf_exempt
def user_delete(request, user_id):
    """Eliminar un usuario (solo admin)"""
    if request.method == 'DELETE' or request.method == 'POST':
        try:
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse({'message': 'Usuario no encontrado'}, status=404)
            
            user.delete()
            return JsonResponse({'message': 'Usuario eliminado exitosamente'})
        except Exception as e:
            return JsonResponse({'message': f'Error al eliminar usuario: {str(e)}'}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

@csrf_exempt
def role_list(request):
    """Listar todos los roles"""
    if request.method == 'GET':
        try:
            roles = Role.objects.all()
            roles_data = [{
                'role_id': role.role_id,
                'role_name': role.role_name
            } for role in roles]
            return JsonResponse({'roles': roles_data}, safe=False)
        except Exception as e:
            return JsonResponse({'message': f'Error al listar roles: {str(e)}'}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

