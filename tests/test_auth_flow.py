import pytest
from fastapi.testclient import TestClient
from fastapiusertemplate.main import app
from fastapiusertemplate.database import get_db, engine
from fastapiusertemplate.models import Base
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True)
def setup_database():
    """Limpiar la base de datos antes de cada test"""
    # Recrear todas las tablas
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # Limpiar después del test
    Base.metadata.drop_all(bind=engine)


def test_complete_user_flow(client):
    """Test del flujo completo con cookies: crear → login → usar → refresh → logout"""
    
    # 1. Crear usuario
    user_data = {
        "email": "flowtest@example.com",
        "username": "flowuser",
        "password": "flowpassword123"
    }
    
    create_response = client.post("/register", json=user_data)
    assert create_response.status_code == 200
    user = create_response.json()
    print(f"✅ Usuario creado: {user['username']}")
    
    # 2. Login (establece cookies)
    login_data = {
        "username": "flowuser",
        "password": "flowpassword123"
    }
    
    login_response = client.post("/login", json=login_data)
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert login_data["message"] == "Login successful"
    assert "access_token" in login_response.cookies
    print(f"✅ Login exitoso: cookies establecidas")
    
    # 3. Usar cookies para acceder a perfil
    profile_response = client.get("/me")
    assert profile_response.status_code == 200
    profile_data = profile_response.json()
    assert profile_data["username"] == "flowuser"
    print(f"✅ Acceso a perfil con cookies: {profile_data['username']}")
    
    # 4. Refresh tokens
    refresh_response = client.post("/refresh")
    assert refresh_response.status_code == 200
    refresh_data = refresh_response.json()
    assert refresh_data["message"] == "Tokens refreshed successfully"
    print(f"✅ Tokens refrescados exitosamente")
    
    # 5. Verificar que aún podemos acceder después del refresh
    profile_response2 = client.get("/me")
    assert profile_response2.status_code == 200
    print(f"✅ Acceso funciona después del refresh")
    
    # 6. Logout
    logout_response = client.post("/logout")
    assert logout_response.status_code == 200
    print(f"✅ Logout exitoso")
    
    # 7. Verificar que no podemos acceder después del logout
    profile_response3 = client.get("/me")
    assert profile_response3.status_code == 401
    print(f"✅ Acceso denegado después del logout")
    
    print("\n🎉 ¡Flujo completo de autenticación con cookies funciona perfectamente!")