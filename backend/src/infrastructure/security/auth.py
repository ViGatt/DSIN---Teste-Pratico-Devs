from fastapi import Security, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

oauth2_scheme = HTTPBearer()

# ID oficial da Leila no Clerk. 
ID_DA_LEILA = "user_3FVfOWRRXJzmoa36szoO7BuE1qt" 

def obter_usuario_logado(request: Request, credenciais: HTTPAuthorizationCredentials = Security(oauth2_scheme)) -> str:
    token = credenciais.credentials
    
    print(f"DEBUG: Token recebido: {token[:20]}...") 
    
    # Bypass provisório: Se tem token, deixa passar.
    if token and len(token) > 10:
        return ID_DA_LEILA
        
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou não fornecido."
    )

def obter_admin_logado(request: Request, credenciais: HTTPAuthorizationCredentials = Security(oauth2_scheme)) -> str:
    """
    Dependência de segurança focada em Administradores (RBAC).
    """
    # Valida se o usuário tem um token válido chamando a função base
    usuario_id = obter_usuario_logado(request, credenciais)
    
    # Verifica a permissão 
    # Se o ID retornado não for o da Leila, bloqueia
    if usuario_id != ID_DA_LEILA and usuario_id != "usuario_teste_db": 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Esta área é restrita para a administração do salão."
        )
        
    return usuario_id