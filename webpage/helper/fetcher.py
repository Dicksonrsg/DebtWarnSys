from webpage.models import Debtor, CompanyUser, Company
from django.contrib.auth.models import User

def get_debtor(cpf:str) -> Debtor:
    try:
        return Debtor.objects.get(cpf=cpf)
    except Debtor.DoesNotExist:
        return None
    except Exception as e:
        raise e
    
    
def is_debtor(auth_user:User) -> bool:
    try:
        debtor = Debtor.objects.get(user_auth=auth_user)
        if debtor:
            return True
    except Debtor.DoesNotExist:
        return False
    except Exception as e:
        raise e
    

def get_company_id(auth_user:User) -> int:
    try:
        company_user = CompanyUser.objects.get(user_auth=auth_user)
        # Returns the first object
        company = company_user.company.all()[:1].get()
        return company.id
    except CompanyUser.DoesNotExist as e:
        raise e
    except Company.DoesNotExist as e:
        raise e
    except Exception as e:
        raise e
    

def get_auth_user(user_id:int) -> User:
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist as error:
        raise error
    except Exception as e:
        raise e