from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

oauth2_scheme = HTTPBearer()

def obter_usuario_logado(credenciais: HTTPAuthorizationCredentials = Security(oauth2_scheme)) -> str:
    """
    Descriptografa o token JWT do Clerk e retorna o ID do usuário.
    Se o token for inválido, bloqueia a requisição com Erro 401.
    """
    token = credenciais.credentials

    # =========================================================================
    # TODO (Produção): Implementar validação real do JWT com a chave do Clerk
    # =========================================================================
    # import jwt
    # try:
    #     payload = jwt.decode(token, "CHAVE_PUBLICA_DO_CLERK", algorithms=["RS256"])
    #     return payload.get("sub") # O Clerk guarda o ID do usuário no campo 'sub'
    # except jwt.ExpiredSignatureError:
    #     raise HTTPException(status_code=401, detail="Token expirado")
    # except jwt.InvalidTokenError:
    #     raise HTTPException(status_code=401, detail="Token inválido")
    
    # Simulador de tokens para testarmos no Swagger no desenvolvimento local
    if token == "token_da_maria":
        return "cliente_maria"
    if token == "token_da_leila":
        return "admin_leila"
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Acesso negado. Token inválido ou não fornecido."
    )