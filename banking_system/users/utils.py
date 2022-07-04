import random
from flask import url_for
from flask_login import current_user
from flask_mail import Message
from validate_email_address import validate_email
from wtforms import ValidationError
from banking_system import mail, db
from banking_system.models import User, UserType, LoanType, Loan, Insurance, InsuranceType, TransactionType, \
    FixedDeposit

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password REset Request', sender='steffykhristi.18.ce@iite.indusuni.ac.in',
                  recipients=[user.user_email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then just ignore this msg and no change will be there.   
'''
    mail.send(msg)


def send_otp_email(user):
    pass
    # otp = random.randint(1111, 9999)
    # msg = Message('Your OTP is here: ', sender='steffykhristi.18.ce@iite.indusuni.ac.in',
    #               recipients=[user.user_email])
    # msg.body = f'''This is the OTP as requested: :{otp}
    # If you did not make this request then just ignore this msg and no change will be there.
    # '''
    # mail.send(msg)
    #
    # return otp


class CustomValidation:

    def validate_user_name(self, user_name):
        user = User.query.filter_by(user_name=user_name.data).first()
        if user:
            raise ValidationError('That username is taken please Choose different one')

    def validate_user_email(self, user_email):
        isvalid = validate_email(user_email.data, verify=True)
        print("##################",isvalid)
        email = User.query.filter_by(user_email=user_email.data).first()
        if email:
            raise ValidationError('That email is taken please Choose different one')
        if not isvalid:
            raise ValidationError('This email id is not exist')


# user route's functions starts

# assign the role of any user [ bank user / bank admin ]
def role_assign(user_id):
    user_role = UserType(user_id=user_id, user_role='user')
    db.session.add(user_role)
    db.session.commit()

# After applying for loan add the type of loan to loantype table with loan id data
def add_loan_type(loan_type, loan_id):
    loan_type = str(loan_type)
    loan = LoanType(loan_id=loan_id, loan_type=loan_type)
    db.session.add(loan)
    db.session.commit()

# add loan type
def loan_type():
    loan = Loan.query.filter_by(user_id=current_user.user_id).first()
    loan_type = LoanType(loan_id=[loan.loan_id])
    db.session.add(loan_type)
    db.session.commit()

# add type of insurance after applying for the insurance
def insurance_type():
    insurance = Insurance.query.filter_by(user_id=current_user.user_id).first()
    insurance_type = InsuranceType(insurance_id=insurance.insurance_id)
    db.session.add(insurance_type)
    db.session.commit()

# add the transaction type after any transaction
def add_transaction_type(transaction_type, transaction_id):
    transaction_type = TransactionType(
        transaction_type=transaction_type,
        transaction_id=transaction_id
    )
    db.session.add(transaction_type)
    db.session.commit()

# add fd's interest to the user accounts
def fd_interest(user):
    fds = FixedDeposit.query.all()

    for fd in fds:
        print("yayyyyyyyyyyyyy")
        print(fd.fd_create_date)
        print()


# user route's functions ends