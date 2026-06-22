from fastapi import Security, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

oauth2_scheme = HTTPBearer()

def obter_usuario_logado(request: Request, credenciais: HTTPAuthorizationCredentials = Security(oauth2_scheme)) -> str:
    token = credenciais.credentials
    
    # LOG PARA DEBUG NO TERMINAL DO PYTHON
    print(f"DEBUG: Token recebido: {token[:20]}...") 
    
    # BYPASS TOTAL: Se chegou aqui, vamos aceitar.
    # O importante agora é ver o dado entrar no banco.
    return "usuario_teste_db"