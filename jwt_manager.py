from jwt import encode,decode

#create token
def create_token(data:dict) -> str:
    token: str = encode(payload=data, key = '1234', algorithm = 'HS256')
    return token

#validate token
def validate_token(token: str) -> dict:
    data: dict = decode(token, key = '1234',algorithms = ['HS256'])
    return data


