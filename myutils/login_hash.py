
import hmac
import hashlib
import base64

########### fastapi_login
SECRET_KEY = '6b3a8722e818a07e6675777c105d502845b1a96f6bef69da774d5cbb6cc944f7'
PASSWORD_SALT = '497166f192bc8629d7449cf8ad8ea371331ebc2df53b1ee485cf0'  # 497166f192bc8629d7449cf8ad8ea371331ebc2df53b1ee485cf03db9279c3d9


def create_password_hash(str_passwd):
    res = hashlib.sha256( (str_passwd + PASSWORD_SALT).encode() ).hexdigest().lower()
    return res

def sign_data(data: str) -> str:
    '''Тhe function returns signed data; use hashlib library'''
    return hmac.new(
        SECRET_KEY.encode(),
        msg=data.encode(),
        digestmod=hashlib.sha256
    ).hexdigest().upper()

def get_username_from_signed_string(username_signed: str):
    '''The function returns a valid username from the hashed cookie'''
    username_base64, sign = username_signed.split('.')
    username = base64.b64decode(username_base64.encode()).decode()
    valid_sign = sign_data(username)
    if hmac.compare_digest(valid_sign, sign):
        return username