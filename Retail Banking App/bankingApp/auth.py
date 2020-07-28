
from datetime import datetime
import math, random
from flask import Blueprint, render_template, redirect, url_for, request, flash,session,make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required
from bankingApp.models import userstore, CustomerStatus, Transactions, AccountStatus
from bankingApp import db, create_app

auth = Blueprint('auth', __name__)

################################         BANK EXECUTIVE FUNCTION    ##########################################################

################################                LOGIN               ##########################################################
@auth.route("/")
@auth.route("/login")
def login():
    return render_template('login.html')


@auth.route('/')
@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = userstore.query.filter_by(username=username).first()
    if user==None:
        flash("Invalid user")
        return redirect(url_for('auth.login'))
    #print(user)
    if user and user.password!=password:
        flash("Please check your login details and try again.")
        return redirect(url_for('auth.login'))

    login_user(user)
    if user and user.password==password:
        session['user_id'] = user.username
        session['username'] = user.username
        flash("Logged in Successfully!!!")
        return redirect(url_for('auth.Home'))
####################################################     HOME        #############################################
@auth.route('/home')
def Home():
    if session['username']=="SB1234567":
        return render_template('home.html')
    if session['username']=="CS1234567":
        return render_template('cashierHome.html')

####################################################     CREATE CUSTOMER        #############################################
@auth.route('/createcustomer')
def create_customer():
    return render_template('create_customerscreen.html')


@auth.route('/createcustomer', methods=['POST'])
def create_customer_post():
    customerssnid = request.form.get('CUSTOMER SSN ID')
    customername = request.form.get('CUSTOMER ID')
    age = request.form.get('AGE')
    address = request.form.get('ADDRESS')
    state = request.form.get('STATE')
    city = request.form.get('CITY')
    
    digits = "0123456789"
    c_id =""
    for i in range(9) : 
        c_id += digits[math.floor(random.random() * 10)]
    c_id=int(c_id)
    print(customerssnid,customername,age,address,state,city,c_id)
    customer = CustomerStatus.query.filter_by(SSN_ID=customerssnid).first()
    date=str(datetime.today().strftime('%Y-%m-%d'))
    if customer:
        flash("Customer already exist")
        return redirect(url_for('auth.create_customer'))

    flash("Customer creation initiated successfully")
    new_user = CustomerStatus(SSN_ID=customerssnid,CustomerID=c_id, Name=customername, Age=age, Address=address, State=state,City=city,Status='Active',Message='Created',Last_Updated=date)
    #new_user.save()
    db.session.add(new_user)
    db.session.commit()

    return render_template('create_customerScreen.html', title='Create Customer Screen')
@auth.route("/updatecustomer")
def update_customer2():
    return render_template("update_customer.html")

@auth.route("/updatecustomer", methods=['GET', 'POST'])
@login_required
def update_customer():
    s_id=request.form.get('CUSTOMER SSN ID')
    newcustomername = request.form.get('name')
    newage = request.form.get('age')
    newaddress = request.form.get('add')
    print(s_id)
    if s_id:
        u=CustomerStatus.query.filter_by(SSN_ID=s_id).first()
        if u:
            resp=make_response(render_template("update_customer2.html",u=u))
            resp.set_cookie('obj3',s_id)
            return resp
        if u==None:
            flash("Account Not found")
            return render_template('update_customer2.html')
    if newcustomername or newage or newaddress:
        a=request.cookies.get('obj3')
        c=CustomerStatus.query.filter_by(SSN_ID=a).first()
        
        if newcustomername:
            c.Name=newcustomername
            db.session.commit()
        if newage:
            c.Age=newage
            db.session.commit()
        if newaddress:
            c.Address=newaddress
            db.session.commit()
        flash("Update Successfully initiated")
        return render_template("update_customer.html")

    



@auth.route("/deletecustomer", methods=['GET', 'POST'])

def delete_customer():
    customerssnid = request.form.get('CUSTOMER SSN ID')
    if customerssnid:
        q=CustomerStatus.query.filter_by(SSN_ID=customerssnid).delete()
        db.session.commit()
        if q:
            
            flash("Delete Successfully initiated")
            return render_template('delete_customer.html')
        if q==None:
            flash("Invalid Customer")
            return render_template('delete_customer.html')


    return render_template('delete_customer.html', title='Delete Customer')


@auth.route("/customerStatus")
def customer_status():
    d=CustomerStatus.query.order_by(CustomerStatus.SSN_ID).all()

    return render_template("CustomerStatus.html",d=d)


@auth.route('/create_Account')
def create_Account():
    return render_template('create_Account.html')


@auth.route('/create_Account', methods=['POST'])
def create_Account_post():
    
    
    c_id = request.form.get('CUSTOMER ID')
    AccType = request.form.get('type')
    amount=request.form.get('amount')
    if int(amount)==0:
        flash("Zero Balance Account can not be created")
        return render_template("create_Account.html")
    
    digits = "0123456789"
    Acc_ID =""
    for i in range(9) : 
        Acc_ID += digits[math.floor(random.random() * 10)]
    Acc_ID=int(Acc_ID)
    date=str(datetime.today().strftime('%Y-%m-%d'))
    a="4"
    b=AccountStatus.query.filter_by(CustomerID=c_id).first()
    if b:
        flash("Account already exist")
        return render_template("create_Account.html")
    
    
    flash("Account Creation Initiated")
    new_user = AccountStatus(CustomerID=c_id,AccountID=Acc_ID, AccountType=AccType,AccStatus='Active',Message='Created',Last_Updated=date,Balance=amount,CRDate=date,CRLastDate=date,Duration=a)
    db.session.add(new_user)
    db.session.commit()

    return render_template('create_Account.html', title='Create Customer Screen')

@auth.route("/deleteAccount", methods=['GET', 'POST'])
def delete_Account():
    Accid = request.form.get('CUSTOMERID')
    Type=request.form.get('type')
    print(Accid,Type)
    if Accid and Type:
        q=AccountStatus.query.filter_by(AccountID=Accid,AccountType=Type).delete()
        db.session.commit()
        if q:
            
            flash("Delete Successfully initiated")
            return render_template('delete_Account.html')
        if q==None:
            flash("Invalid Account")
            return render_template('delete_Account.html')


    return render_template('delete_Account.html', title='Delete Account')


@auth.route("/AccountStatus")
def Account_Status():
    d=AccountStatus.query.order_by(AccountStatus.AccountID).all()
    return render_template("AccountStatus.html", title='Account Status',d=d)
@auth.route("/customersearch")
def search_customer2():
    return render_template('customer_search.html')
@auth.route("/customersearch", methods=['GET', 'POST'])
def search_customer():
    c=None
    k=None
    ssn_id = request.form.get('SSNID')
    customer_id = request.form.get('c_id')
    print(ssn_id,customer_id)
    if ssn_id:
        c=CustomerStatus.query.filter_by(SSN_ID=ssn_id).first()
        
        if c:
            return render_template("customer_search2.html",c=c)
        

    if customer_id:
        k=CustomerStatus.query.filter_by(CustomerID=customer_id).first()
        if k:
            return render_template("customer_search3.html",k=k)

    flash("Customer not found")
    return render_template('customer_search.html')


@auth.route("/accountsearch")
def search_account2():
    return render_template('account_search.html')
@auth.route("/accountsearch", methods=['GET', 'POST'])
def search_account():
    c=None
    k=None
    acc_id = request.form.get('AccID')
    customer_id = request.form.get('c_id')
    print(acc_id,customer_id)
    if acc_id:
        c=AccountStatus.query.filter_by(AccountID=acc_id).first()
        
        if c:
            return render_template("account_search2.html",c=c)
        

    if customer_id:
        k=AccountStatus.query.filter_by(CustomerID=customer_id).first()
        if k:
            return render_template("account_search3.html",k=k)

    flash("Customer not found")
    return render_template('account_search.html')






################################         BANK CASHIER FUNCTION    ##########################################################
@auth.route("/depositmoney")
@login_required
def depositmoney2():
    return render_template('depositmoney.html')


@auth.route("/depositmoney", methods=['GET', 'POST'])
@login_required
def depositmoney():
    acc_id=request.form.get('AccID')
    
    amount = request.form.get('d1')
    c=AccountStatus.query.filter_by(AccountID=acc_id).first()
    if acc_id:
        
        
        if c:
            resp=make_response(render_template("depositmoney.html",c=c))
            resp.set_cookie('obj',acc_id)
            return resp
        if c==None:
            flash("Account Not found")
            return render_template('depositmoney.html')

    if amount:
        date=str(datetime.today().strftime('%Y-%m-%d'))
        b=100000
        b=int(b)
        digits = "0123456789"
        Tr_id =""
        for i in range(6) : 
            Tr_id += digits[math.floor(random.random() * 10)]
        Tr_id=int(Tr_id)
        a=request.cookies.get('obj')
        c=AccountStatus.query.filter_by(AccountID=a).first()
        AccType=c.AccountType
        c.Balance =int(c.Balance) + int(amount)
        db.session.commit()
        new_data = Transactions(TranscationID=Tr_id,SAccountID=b, DAccountID=a,AccountType=AccType,Amount=int(amount),TrDate=date,SAccountType='Savings/Current',DAccountType=AccType)
        db.session.add(new_data)
        db.session.commit()


        flash("Amount deposited successfully")
        return render_template("depositmoney.html")
    

@auth.route("/withdrawlmoney")
@login_required
def withdrawlmoney2():
    return render_template('withdrawlmoney.html')

@auth.route("/withdrawlmoney", methods=['GET', 'POST'])
@login_required
def withdrawlmoney():
    acc_id=request.form.get('AccID')
    
    amount = request.form.get('d1')
    c=AccountStatus.query.filter_by(AccountID=acc_id).first()
    if acc_id:
        
        
        if c:
            resp=make_response(render_template("withdrawlmoney.html",c=c))
            resp.set_cookie('obj2',acc_id)
            return resp
        if c==None:
            flash("Account Not found")
            return render_template('withdrawlmoney.html')

    if amount:
        date=str(datetime.today().strftime('%Y-%m-%d'))
        b=100000
        b=int(b)
        digits = "0123456789"
        Tr_id =""
        for i in range(6) : 
            Tr_id += digits[math.floor(random.random() * 10)]
        Tr_id=int(Tr_id)

        a=request.cookies.get('obj2')
        c=AccountStatus.query.filter_by(AccountID=a).first()
        AccType=c.AccountType
        if int(c.Balance)==0:
            flash("Insufficient Balance")
            return render_template("withdrawlmoney.html")
        c.Balance =int(c.Balance) - int(amount)
        db.session.commit()
        new_data = Transactions(TranscationID=Tr_id,SAccountID=a, DAccountID=b,AccountType=AccType,Amount=int(amount),TrDate=date,SAccountType=AccType,DAccountType='Savings\current')
        db.session.add(new_data)
        db.session.commit()

        flash("Amount withdrawl successfully")
        return render_template("withdrawlmoney.html")
@auth.route("/transfermoney")
def transfermoney2():
    return render_template('transfer.html')

@auth.route("/transfermoney", methods=['GET', 'POST'])
@login_required
def transfermoney():

    source_account_type = request.form.get('type1')
    source_account_id = request.form.get('SOURCEID')
    target_account_type = request.form.get('type2')
    target_account_id = request.form.get('TARGETID')
    transfer_amount = request.form.get('amount')

    date=str(datetime.today().strftime('%Y-%m-%d'))
    c=AccountStatus.query.filter_by(AccountID=source_account_id).first()
    d=AccountStatus.query.filter_by(AccountID=target_account_id).first()
    digits = "0123456789"
    Tr_id =""
    for i in range(6) : 
        Tr_id += digits[math.floor(random.random() * 10)]
    Tr_id=int(Tr_id)
    if c and d:
        B1=c.Balance
        if int(B1)==0:
            flash("Insufficient Balance")
            return render_template("transfer.html")
    
        c.Balance =int(c.Balance) -int(transfer_amount)
        db.session.commit()
        B2=c.Balance
        B3=d.Balance
        d.Balance=int(d.Balance) + int(transfer_amount)
        db.session.commit()
        B4=d.Balance
        new_data = Transactions(TranscationID=Tr_id,SAccountID=source_account_id,DAccountID=target_account_id, AccountType=source_account_type, Amount=transfer_amount,TrDate=date,SAccountType=source_account_type,DAccountType=target_account_type)
        db.session.add(new_data)
        db.session.commit()
        flash("Amount Transfer Successfully")
        return render_template("transfer.html",B1=B1,B2=B2,B3=B3,B4=B4)

    
    if (c and d==None) or (c==None and d) or (c==None and d==None):
        flash("Account Not found")
        return render_template('transfer.html', title='Transfer Money')

@auth.route("/accountstatement")
@login_required
def accountstatement2():
    return render_template('account_statement.html')

@auth.route("/accountstatement", methods=['GET', 'POST'])
@login_required
def accountstatement():
    deposiit=[]
    withdrawl=[]
    account_id = request.form.get('AccID')
    if account_id:
        a=Transactions.query.filter_by(SAccountID=account_id).first()
        b=Transactions.query.filter_by(DAccountID=account_id).first()
    
        if a or b:
            withdrawl.append(a)
            deposiit.append(b)
            return render_template("account_statement2.html",a=a,b=b)
    
        if a==None and b==None:
            flash("Account Not Found")
            return render_template("account_statement.html")

@auth.route("/logout")
def logout():
    flash("Logged out Successfully!!!")
    return redirect(url_for('auth.login'))
