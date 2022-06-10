from flask import render_template, Blueprint
from flask import Blueprint

about = Blueprint('about', __name__)

@about.route("/money")
def money():
    return render_template('money.html', title='money')

@about.route("/fixed-deposits")
def fd():
    return render_template('fd.html', title='fixed-deposits')

@about.route("/loan")
def loan():
    return render_template('loan.html', title='loan')

@about.route("/insurance")
def insurance():
    return render_template('insurance.html', title='insurance')