# admin panel's route's all constants are declared here


ADMIN_LOGIN_SUCCESS = 'admin Login successfully..'
ADMIN_LOGIN_UNSUCCESS = 'Login unsuccessfully..please check email and password'
USER_DELETED = 'User is been deleted from the user :)'
BRANCH_EXISTED = 'this branch has already exist!'
BRANCH_ADDED = 'branch is added successfully'
ATM_EXISTED = 'Atm has already exist at this area!'
ATM_ADDED = 'Atm is added successfully'
BANK_MEMBER_ADDED = 'New bank member has been created!'

BANK_MEMBER_DELETED = 'Bank member has been deleted'


def status_update(user_name, activity):
    flash = f'{user_name}\'s {activity} status has been changed :)'
    return flash


FLASH_MESSAGES = {
    'SUCCESS': 'success',
    'FAIL': 'danger'
}