# usuarios/tests/test_usuario.py

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def crear_usuario():
    def crear_usuario_aux(email="test@example.com", password="testpassword", first_name="Test", last_name="User"):
        user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
        return user
    return crear_usuario_aux

@pytest.mark.django_db
def test_crear_usuario(api_client):
    url = reverse('user-list')  # Asegúrate de que el nombre del endpoint coincida con el registrado en el router
    data = {
        "email": "newuser@example.com",
        "password": "newpassword123",
        "first_name": "New",
        "last_name": "User",
        "is_admin": False,
        "is_staff": False,
        "is_active": True
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email="newuser@example.com").exists()

@pytest.mark.django_db
def test_obtener_token(api_client, crear_usuario):
    usuario = crear_usuario()
    url = reverse('token_obtain_pair')
    data = {
        "email": usuario.email,
        "password": "testpassword"
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data

@pytest.mark.django_db
def test_acceso_endpoint_protegido(api_client, crear_usuario):
    usuario = crear_usuario()
    url = reverse('user-list')

    # Intento de acceso sin token
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Obtención del token y acceso con token
    token_url = reverse('token_obtain_pair')
    token_response = api_client.post(token_url, {"email": usuario.email, "password": "testpassword"})
    access_token = token_response.data["access"]

    # Añadimos el token al encabezado de autorización
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
