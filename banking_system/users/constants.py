SUCCESSFUL_REGISTRATION = 'Your account has been created you are all set for login'
SUCCESSFUL_LOGIN = 'Login successfully'
UNSUCCESSFUL_LOGIN = 'Login unsuccessfully..please check email and password'
NEW_USER_ADDED = 'new user added successfully'
ADMIN_NOT_ACTIVATE_UR_ACCOUNT = 'Hey! admin does not activate your account yet! cant login rn'
LOGOUT_SUCCESS = 'Logout successfully..'
ACCOUNT_UPDATED = 'Your account has been update!'
EMAIL_INFO = 'An email has been sent with instruction to reset your password.'
INVALID_TOKEN = 'That is an invalid or expired token'
PASSWORD_UPDATED = 'Your password has been updated!, you are now able to login'
ACCOUNT_ALREADY_EXISTED = 'You have already account'
ACCOUNT_CREATED = 'Your account has been created'
LOGIN_FIRST = "You need to login first"
ALREADY_CARD_EXISTED = 'You have already Card'
CARD_CREATED = 'your card has been created'
PENDING_LOAN = 'you have already current loan going on finish that  first'
TRANSACTION_SUCCESSFULLY = "Transaction is successfully done"
CANT_TRANSFER = 'You can not transfer to yourself it doesn\'t make any sense'
PASSWORD_INCORRECT = 'Password is incorrect'


def insufficient_balance(data):
    return 'Insufficient balance you have only:data'

def success_activity(activity):
    flash = f'Your {activity} has been requested with inactive status'
    return flash

def pending_activity(activity):
    flash = f'You have already current {activity} already'
    return flash


FLASH_MESSAGES = {
    'SUCCESS': 'success',
    'FAIL': 'danger',
    'INFO': 'info',
    'WARNING': 'warning'
}