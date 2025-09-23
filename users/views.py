from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import User
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer

class IsSelfOrAdmin(permissions.BasePermission):
    """
    Permite que un usuario vea/edite su propio perfil; admin puede todo.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

    # Sólo admin puede listar/crear/borrar; cada usuario puede ver/editarse a sí mismo
    def get_permissions(self):
        if self.action in ["list", "create", "destroy"]:
            return [permissions.IsAdminUser()]
        elif self.action in ["retrieve", "update", "partial_update"]:
            return [permissions.IsAuthenticated(), IsSelfOrAdmin()]
        return [permissions.AllowAny()]

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # (Opcional) loguear automáticamente después de registrar:
        login(request, user)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@ensure_csrf_cookie
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]
    login(request, user)  # Usa sesiones + cookie
    return Response({"message": "Login exitoso", "user": UserSerializer(user).data})

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"message": "Logout exitoso"})

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)