from flask import Flask, render_template, make_response, redirect, request
import pickle 
from Database import UDB

app = Flask(__name__)

#Main Page
@app.route('/')
def index():
    userName=request.cookies.get('userName')
    if userName==None or userName=='guest':
        return render_template('index1.html')
    elif userName == 'Admin':
        return redirect('/Admin')
    else:
        menu=readMenu()
        return render_template('menutemplate1.html',username=userName,menuItems=menu)
# to set the cookie and redirect to the main page
@app.route('/setCookie', methods=['POST','GET'])
def setCookie():
    if request.methods=='POST':
        userName=request.form['userName']
    resp=make_response(redirect('/'))
    resp.set_cookie('userName',userName)
    return resp
    

# to get the cookie and return it
@app.route('/getCookie', methods=['POST', 'GET'])
def getCookie():
    userName=request.cookies.get('userName')
    return userName

# LOGIN PAGE
@app.route('/login/<errNumber>')
def login(errNumber=0):
    message=''
    if errNumber=='1':
        message='Username or Password is Incorrect'
    return render_template('login1.html',message=message)

# LOGIN EXECUTER
@app.route('/loginExe', methods=['POST'])
def loginExe():
    userName=request.form['userName'].lower()
    password=request.form['Password']
    
    try:
        f=open('sessionStatus.pkl','rb')
        sessionStatus=pickle.load(f)['sessionStatus']
        f.close()
    except:
        CloseSession()
        f=open('sessionStatus.pkl','rb')
        sessionStatus=pickle.load(f)['sessionStatus']
        f.close()
    
    if UDB.access(userName,password):
        if userName == 'admin':
            resp=make_response(redirect('/Admin'))
            resp.set_cookie('userName',userName)
        elif sessionStatus == 'Open':
            resp=make_response(redirect('/'))
            resp.set_cookie('userName',userName)
        else:
            resp=make_response(redirect('/'))
            resp.set_cookie('userName',userName)
            return redirect('/kCafeClosed')
        return resp
    else:
        return redirect('/login/1')

#Sign OUT
@app.route('/signOut')
def signOut():
    resp=make_response(redirect('/'))
    resp.set_cookie('userName','guest')
    return resp

# SIGN UP PAGE
@app.route('/signup/<errNumber>')
def signup(errNumber):
    message=''
    if errNumber=='1':
        message='username has been taken'
    if errNumber=='2':
        message='password does not match'
    if errNumber=='3':
        message='password is too short'

    return render_template('signup.html', message=message)

# sIGNUP EXECUTER
@app.route('/signupExe', methods=['POST'])
def signupExe():
    userName=request.form['userName']
    password=request.form['Password']
    ConfirmPassword=request.form['ConfirmPassword']
    email=request.form['email']
    
    if UDB.getUserByName(userName):
        return redirect('/signup/1')
    elif len(password)<8:
        return redirect('/signup/3')
    elif password!=ConfirmPassword:
        return redirect('/signup/2')
    else:
        newUser=UDB.User({'username':userName.lower(),'password':password, 'email':email})
        UDB.add(newUser)
        
    return redirect('/success')

@app.route('/success')
def success():
    return render_template('success1.html')
    
@app.route('/profile')
def profile():
    username=getCookie()
    userData=UDB.getUserByName(username)
    if username==None or username=='guest':
        return redirect('/login/0')
    user={
        'username':userData.username,
        'DOB':userData.DOB,
        'email':userData.email,
        'voteID':"userData.voteID",
        'regDate':userData.regDate,
        'nationality':userData.nationality,
        'questionsID':"userData.questionsID",
        'answersID':"userData.answersID"
    }
    return render_template('profile.html',user=user)

@app.route('/profileEdit/<message>')
def profileEdit(message):
    if message=='0':
        message='edit your profile'
    if message=='1':
        message='your password does not match'
    if message=='2':
        message='your password is too short'
    if message=='3':
        message='email is compulsory'
        
    username = getCookie()
    userData = UDB.getUserByName(username)
    Email = userData.email
    
    return render_template('profileEdit.html', username=username, message=message)
    

@app.route('/edit', methods=["post"])
def edit():
    return redirect('/profileEdit/0')

@app.route('/editExecuter', methods=["post"])
def editExecuter():
    username = getCookie()
    userData = UDB.getUserByName(username)


    if len(request.form['password'])<8:
        return redirect('/profileEdit/2')
    if request.form['password']!=request.form['confirmPassword']:
        return redirect('/profileEdit/1')
    if request.form['email']=='':
        return redirect('/profileEdit/3')
    
    userData.email=request.form['email']
    userData.password=request.form['password']
    userData.nationality=request.form['nationality']
    
    
    UDB.update(userData)
    
    return 'changes has been applied'
    
def readMenu():
    try:
        f = open('menu.pkl','rb')
        order=pickle.load(f)
        f.close()
        return order
    except:
        f=open('orderDB.pkl','wb')
        pickle.dump({},f,pickle.HIGHEST_PROTOCOL)
        f.close()
        return {}

def readOrders():
    try:
        f = open('orderDB.pkl','rb')
        order=pickle.load(f)
        f.close()
        return order
    except:
        f=open('orderDB.pkl','wb')
        pickle.dump({},f,pickle.HIGHEST_PROTOCOL)
        f.close()
        return {}

@app.route('/order/<foodname>')
def orderpage(foodname):
    Orders = readOrders()
    userName=request.cookies.get('userName')
    
    Orders[userName]=foodname
    
    print Orders

    f=open('orderDB.pkl','wb')
    pickle.dump(Orders,f,pickle.HIGHEST_PROTOCOL)
    f.close()
    
    f=open('mainMenu.pkl','rb')
    mainMenu=pickle.load(f)
    f.close()
    
    foodname=mainMenu[foodname]['foodname']
    foodimage=mainMenu[foodname]['foodimage']

    return render_template('orderSuccessful.html',username=userName,foodname=foodname,foodimage=foodimage)

@app.route('/getOrder')
def getOrder():
    if request.cookies.get('userName')!='admin':
        return redirect('/accessDenied')
    orders=readOrders()
    
    finalOrder={}
    for person,food in orders.items():
        foodOrderers=finalOrder.get(food,[])
        foodOrderers.append(person)
        finalOrder[food]=foodOrderers
        
    return str(finalOrder)

@app.route('/menuDesign', methods = ['GET'])
def menuDesign():
    f=open('mainMenu.pkl','rb')
    mainMenu=pickle.load(f)
    f.close()

    return render_template('menuDesign.html',mainMenu=mainMenu)

@app.route('/setMenu', methods = ['POST'])
def setMenu():
    if request.cookies.get('userName')!='admin':
        return redirect('/accessDenied')
    orders = request.form
    f=open('mainMenu.pkl','rb')
    mainMenu=pickle.load(f)
    f.close()
    f=open('menu.pkl','wb')
    AvailableOrders=[mainMenu[i] for i in orders]
    pickle.dump(AvailableOrders,f,pickle.HIGHEST_PROTOCOL)
    f.close()
    return str(AvailableOrders)
@app.route('/accessDenied')
def accessDenied():
    return render_template('accessDenied.html')
    
    
@app.route('/Admin')
def adminAcces():
    if request.cookies.get('userName')!='admin':
        return redirect('/accessDenied')
    f=open('sessionStatus.pkl','rb')
    sessionStatus=pickle.load(f)['sessionStatus']
    f.close()
    return render_template('Admin1.html',sessionStatus=sessionStatus)

@app.route('/OpenSession', methods = ['POST'])    
def OpenSession():
    
    f = open('orderDB.pkl', 'wb')
    pickle.dump({},f,pickle.HIGHEST_PROTOCOL)
    f.close()
    
    f = open('sessionStatus.pkl', 'wb')
    sessionStatus={'sessionStatus':'Open'}
    pickle.dump(sessionStatus,f,pickle.HIGHEST_PROTOCOL)
    f.close()
    return redirect('/Admin')

@app.route('/CloseSession', methods = ['POST'])
def CloseSession():
    f = open('sessionStatus.pkl', 'wb')
    sessionStatus={'sessionStatus':'Close'}
    pickle.dump(sessionStatus,f,pickle.HIGHEST_PROTOCOL)
    f.close()
    return redirect('/getOrder')

@app.route('/kCafeClosed')
def kCafeClosed():
    return render_template('kCafeClosed1.html')
    
if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 8080)
