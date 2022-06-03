from orgadmin.models import Contract, ContractSign


def has_contract(user_type, org_code):
    return Contract.objects.filter(user_type=user_type, is_active=True,
                                   created_by__organization_code=org_code).exists()


def has_contract_submitted(user, user_type, org_code):
    return ContractSign.objects.filter(user=user, contract_code__user_type=user_type, approved=None,
                                       contract_code__created_by__organization_code=org_code).exists()


def has_contract_approved(user, user_type, org_code):
    return ContractSign.objects.filter(user=user, contract_code__user_type=user_type, approved=True,
                                       contract_code__created_by__organization_code=org_code).exists()
