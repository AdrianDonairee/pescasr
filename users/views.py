from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer, RegisterSerializer, UpdateUserSerializer

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
            return [IsAuthenticated(), IsSelfOrAdmin()]
        return [permissions.AllowAny()]

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    """
    Registro público. No usa sesiones; el frontend debe pedir tokens en /api/user/login/ (o /api/token/).
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def logout(request):
    """
    Logout: recibe {"refresh": "<refresh_token>"} y lo blacklistea para invalidarlo.
    """
    refresh = request.data.get('refresh')
    if not refresh:
        return Response({'detail': 'Refresh token requerido.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh)
        token.blacklist()
        return Response({'detail': 'Logout exitoso.'}, status=status.HTTP_205_RESET_CONTENT)
    except Exception:
        return Response({'detail': 'Token inválido o ya revocado.'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        serializer = UpdateUserSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        serializer = UpdateUserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(request.user).data)