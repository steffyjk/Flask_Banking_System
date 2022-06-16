from email.policy import default
from enum import unique
from flask import current_app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from pkg_resources import find_distributions
from banking_system import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    # print(user_id,"####################")
    p = User.query.get(int(user_id))
    # print("this is p: ",p)
    return p

#modified [ 09-06-2022 ]
class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(320),unique=True,nullable=False)
    user_password = db.Column(db.String(320), nullable=False)
    user_email = db.Column(db.String(120),unique=True,nullable=False)
    u_p= db.Column(db.String(320))
    user_phone_number=u_p
    user_first_name = db.Column(db.String(320),nullable=False)
    user_last_name = db.Column(db.String(320),nullable=False)
    user_address = db.Column(db.String(120),nullable=False)
    user_age = db.Column(db.Integer,nullable=False)
    date_of_birth = db.Column(db.DateTime,nullable=False)

    def get_id(self):
        return self.user_id

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.user_id}).decode('utf-8')


    @staticmethod
    def verify_reset_token(token):
        
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
        

    def __repr__(self):
        return f"User('{self.user_name}','{self.user_email}','{self.user_id}')"


class User_type(db.Model):
    user_type_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'))
    user_role = db.Column(db.String(320),nullable=False,default='user')

class Account(db.Model):
    account_number = db.Column(db.Integer,primary_key=True)
    # account_type = db.Column(db.String(100),nullable=False)
    account_status = db.Column(db.String(100),nullable=False, default= 'Inactive')
    account_balance = db.Column(db.Float,nullable=False,default=0.0)
    saving_balance = db.Column(db.Float,nullable=False,default=0.0)
    #added    
    account_creation_date = db.Column(db.DateTime,nullable=False, default= datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False,unique=True)
    branch_id = db.Column(db.Integer,db.ForeignKey('branch.branch_id'),nullable=False)

class Account_type(db.Model):
    account_type_id = db.Column(db.Integer,primary_key=True)
    account_number = db.Column(db.Integer,db.ForeignKey('account.account_number'),nullable=False)
    account_type = db.Column(db.String(100),nullable=False)

class Card(db.Model):
    card_number = db.Column(db.Integer,primary_key=True)
    cvv_number = db.Column(db.Integer,nullable=False)
    card_pin = db.Column(db.Integer,nullable=False)
    creation_date = db.Column(db.DateTime,nullable=False, default= datetime.utcnow)
    expiry_date = db.Column(db.DateTime,nullable=False, default= datetime.utcnow)
    account_number = db.Column(db.Integer,db.ForeignKey('account.account_number'),nullable=False)

class Transaction(db.Model):
    transaction_id = db.Column(db.Integer,primary_key=True)
    # transaction_type = db.Column(db.String(100),nullable=False)
    transaction_amount = db.Column(db.Float,nullable=False,default=0.0)
    sender_id = db.Column(db.Integer)
    receiver_id = db.Column(db.Integer)
    transaction_date = db.Column(db.DateTime,nullable=False, default= datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False)

class Transaction_type(db.Model):
    transaction_type_id = db.Column(db.Integer,primary_key=True)
    transaction_id = db.Column(db.Integer,db.ForeignKey('transaction.transaction_id'),nullable=False)    
    transaction_type = db.Column(db.String(100),nullable=False)

class Loan(db.Model):
    loan_id = db.Column(db.Integer,primary_key=True) 
    loan_amount = db.Column(db.Integer,nullable=False,default=0.0)
    loan_status = db.Column(db.String(100),nullable=False)
    rate_interest = db.Column(db.Float,nullable=False,default=0.0)
    # loan_type = db.Column(db.String(100),nullable=False)
    paid_amount = db.Column(db.Float,nullable=False,default=0.0)
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False)

class Loan_type(db.Model):
    loan_type_id = db.Column(db.Integer,primary_key=True)
    loan_id = db.Column(db.Integer,db.ForeignKey('loan.loan_id'),nullable=False)    
    loan_type = db.Column(db.String(100),nullable=False)

class Insurance(db.Model):
    insurance_id = db.Column(db.Integer,primary_key=True)
    insurance_amount = db.Column(db.Float,nullable=False,default=0.0)
    insurance_status = db.Column(db.String(100),nullable=False)
    # insurance_type = db.Column(db.String(100),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False)

class Insurance_type(db.Model):
    insurance_type_id = db.Column(db.Integer,primary_key=True)
    insurance_id = db.Column(db.Integer,db.ForeignKey('insurance.insurance_id'),nullable=False)    
    insurance_type = db.Column(db.String(100),nullable=False)

class Fixed_deposite(db.Model):
    fd_id = db.Column(db.Integer,primary_key=True)
    fd_amount = db.Column(db.Float,nullable=False,default=0.0)
    fd_status = db.Column(db.String(100),nullable=False)
    rate_interest = db.Column(db.Float,nullable=False,default=0.0)
    added_amount = db.Column(db.Float,nullable=False,default=0.0)
    account_number = db.Column(db.Integer,db.ForeignKey('account.account_number'),nullable=False)

class Bank_details(db.Model):
    bank_name = db.Column(db.String(20),unique=True,nullable=False,default='SJK BANK')
    bank_id = db.Column(db.Integer,primary_key=True,default='1007')
    bank_email = db.Column(db.String(120),unique=True,nullable=False,default='desaiparth974@gmail.com')
    bank_contact = db.Column(db.Integer,default='10058')

class Branch(db.Model):
    branch_id = db.Column(db.Integer,primary_key=True)
    branch_name = db.Column(db.String(20),unique=True,nullable=False)
    branch_address = db.Column(db.String(120),unique=True,nullable=False)
    bank_id = db.Column(db.Integer,db.ForeignKey('bank_details.bank_id'),nullable=False)


class Atm(db.Model):
    atm_id = db.Column(db.Integer,primary_key=True)
    atm_address = db.Column(db.String(120),unique=True,nullable=False)
    bank_id = db.Column(db.Integer,db.ForeignKey('bank_details.bank_id'),nullable=False)



    
