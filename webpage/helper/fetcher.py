from webpage.models import Debtor
from django.contrib.auth.models import User

def get_debtor(cpf:str) -> Debtor:
    try:
        return Debtor.objects.get(cpf=cpf)
    except Debtor.DoesNotExist:
        return None
    except Exception as e:
        raise e
    

def get_auth_user(user_id:int) -> User:
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist as error:
        raise error
    except Exception as e:
        raise e