from datetime import datetime
from flask_login import UserMixin
from bankingApp import db


class Transactions(db.Model):
    __tablename__ = 'Transactions'
    TranscationID=db.Column(db.Integer,primary_key=True)
    SAccountID = db.Column(db.Integer)
    DAccountID = db.Column(db.Integer)
    AccountType = db.Column(db.String(20))
    Amount = db.Column(db.Integer)
    TrDate = db.Column(db.String(20))
    SAccountType = db.Column(db.String(20))
    DAccountType = db.Column(db.String(20))

    def __repr__(self):
        return f"Transactions('{self.TranscationID}','{self.SAccountID}','{self.DAccountID}', '{self.AccountType}', '{self.Ammount}', '{self.TrDate}', " \
               f"'{self.SAccountType}', '{self.DAccountType}' )"


class AccountStatus(db.Model):
    __tablename__='AccountStatus'
    CustomerID = db.Column(db.Integer, primary_key=True)
    AccountID = db.Column(db.Integer,unique=True)
    AccountType = db.Column(db.String(20))
    AccStatus = db.Column(db.String(10))
    Message = db.Column(db.String(50))
    Last_Updated = db.Column(db.String(20))
    Balance = db.Column(db.Integer, nullable=False)
    CRDate = db.Column(db.String(20), nullable=False)
    CRLastDate = db.Column(db.String(20), nullable=False)
    Duration = db.Column(db.Integer)

    def __repr__(self):
        return f"AccountStatus('{self.CustomerID}', '{self.AccountID}', '{self.AccountType}', '{self.AccStatus}', " \
               f"'{self.Message}', '{self.Last_Updated}', '{self.Balance}', '{self.CRDate}', '{self.CRLastDate}', '{self.Duration}')"


class CustomerStatus(db.Model):
    __tablename__ = 'CustomerStatus'
    SSN_ID = db.Column(db.Integer, nullable=False, primary_key=True)
    CustomerID = db.Column(db.Integer, nullable=False, unique=True)
    Name = db.Column(db.String(50), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Address = db.Column(db.String(40), nullable=False)
    State = db.Column(db.String(20), nullable=False)
    City = db.Column(db.String(20), nullable=False)
    Status = db.Column(db.String(10))
    Message = db.Column(db.String(50))
    Last_Updated = db.Column(db.String(20))

    def __repr__(self):
        return f"CustomerStatus('{self.SSN_ID}', '{self.CustomerID}', '{self.Name}', '{self.Age}', '{self.Address}', '{self.State}','{self.City}' )"

class userstore(UserMixin, db.Model):
    __tablename__='userstore'
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"userstore('{self.username}', '{self.password}', '{self.timestamp}')"
    def is_authenticated(self):
        return True

    def is_active(self):
        return True
    def get_id(self):
        return str(self.username)
