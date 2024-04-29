from django.contrib.auth.models import Group, Permission, User


def assign_group(user_name: str, role: str):
    perms_by_role = {
        "Owner": [
            "add_company",
            "change_company",
            "delete_company",
            "view_company",
            "add_debtor",
            "change_debtor",
            "delete_debtor",
            "view_debtor",
            "add_debt",
            "change_debt",
            "delete_debt",
            "view_debt",
            "add_companyuser",
            "change_companyuser",
            "delete_companyuser",
            "view_companyuser",
        ],
        "Admin": [
            "view_company",
            "add_debtor",
            "change_debtor",
            "delete_debtor",
            "view_debtor",
            "add_debt",
            "change_debt",
            "delete_debt",
            "view_debt",
            "add_companyuser",
            "change_companyuser",
            "delete_companyuser",
            "view_companyuser",
        ],
        "Worker": [
            "view_company",
            "add_debt",
            "change_debt",
            "delete_debt",
            "view_debt",
            "add_companyuser",
            "change_companyuser",
            "delete_companyuser",
            "view_companyuser",
        ],
        "Debtor": [
            "add_debtor",
            "change_debtor",
            "delete_debtor",
            "view_debtor",
            "add_debt",
            "view_debt",
        ],
    }
    
    try:
        user = User.objects.get(username=user_name)
        group, created = Group.objects.get_or_create(name=role)
        for perm in perms_by_role[role]:
            permission = Permission.objects.get(
                codename=perm,
            )        
            group.permissions.add(permission)
        user.groups.add(group)
    except Exception as e:
        print(f"Assign Group Exception: {str(e)}")
        raise e
