from flask import Flask, render_template, make_response, redirect, request
import pickle 
import os, time
from time import gmtime, strftime
from Database import UDB

app = Flask(__name__)

#checkin permissions
def permision(f):
    username=request.cookies.get('username')
    
    if username=='admin':
        if not(f in ['setMenu','signup','menuDesign','getOrder','staffsDesign']):
            return redirect('/AccessDenied')
    elif username!='admin' and not(f in ['index','login','menuDesign','orderpage']):
        return redirect('/AccessDenied')
    #if user not in allowed users: access denied


#Main Page this is where you login
@app.route('/')
def index():
    #permision('index')
    username=request.cookies.get('username')
    if username==None or username=='guest':
        return render_template('index1.html')
    elif username=="admin":
        return redirect('/Admin')

    menu=readMenu()
    return render_template('menutemplate1.html',username=username,menuItems=menu,userimage='/static/kidocode.png')

# to set the cookie and redirect to the main page
@app.route('/setCookie', methods=['POST','GET'])
def setCookie():
    if request.methods=='POST':
        username=request.form['username']
    resp=make_response(redirect('/'))
    resp.set_cookie('username',username)
    return resp
    
    
# the Admin Finalizez the Orders
@app.route("/finalizedOrder", methods=["POST"])
def finalizedOrder():
    f=open('orderDB.pkl','rb')
    lastOrder=str(pickle.load(f))
    f.close()
    
    #messageItTo('Admin',lastOrder,'0183552313')
    CloseTheSession()
    return 'the order is set! wait for your foods! hahahahaha  <a href = "/Admin"> Back</a>'

# to get the cookie and return it
@app.route('/getCookie', methods=['POST', 'GET'])
def getCookie():
    username=request.cookies.get('username')
    return username

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
    username=request.form['username'].lower()
    password=request.form['Password']
    
    f=open('sessionStatus.pkl','rb')
    sessionStatus=pickle.load(f)['sessionStatus']
    f.close()
    
    f=open('entitledStaffs.pkl','rb')
    entitledStaffs=pickle.load(f)
    f.close()
    
    if UDB.access(username,password):
        if username == 'admin':
            resp=make_response(redirect('/Admin'))
            resp.set_cookie('username',username)
        elif not(username in entitledStaffs):
            return redirect('/accessDenied')
        elif sessionStatus == 'Open':
            resp=make_response(redirect('/'))
            resp.set_cookie('username',username)
        else:
            resp=make_response(redirect('/'))
            resp.set_cookie('username',username)
            return redirect('/kCafeClosed')
        return resp
    else:
        return redirect('/login/1')

#Sign OUT
@app.route('/signOut')
def signOut():
    resp=make_response(redirect('/'))
    resp.set_cookie('username','guest')
    return resp

# SIGN UP PAGE
@app.route('/signup/<errNumber>')
def signup(errNumber):
    message=''
    if errNumber=='1':
        message='The Username is Taken'
    if errNumber=='2':
        message='The Password Does Not Match'
    if errNumber=='3':
        message='The Password is Too Short'
    if errNumber=='3':
        message='The Phone Number is Either Too long or Short'
    return render_template('signup1.html', message=message)

# sIGNUP EXECUTER
@app.route('/signupExe', methods=['POST'])
def signupExe():
    username=request.form['username']
    password=request.form['Password']
    ConfirmPassword=request.form['ConfirmPassword']
    email=request.form['email']
    phoneNumber=request.form['phoneNumber']
    
    if UDB.getUserByName(username):
        return redirect('/signup/1')
    elif len(password)<8:
        return redirect('/signup/3')
    elif password!=ConfirmPassword:
        return redirect('/signup/2')
    elif 9<len(phoneNumber)<12:
        return redirect('/signup/4')
    else:
        newUser=UDB.User({'username':username.lower(),'password':password, 'email':email, 'phoneNumber':phoneNumber})
        UDB.add(newUser)
        
    return redirect('/success')

# this is when the admin adds a new member and it gives the success
@app.route('/success')
def success():
    return render_template('success1.html')

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
    
# This is where the orsders will come in to a page and the admin can see the orders
def readMenu():
    f = open('menu.pkl','rb')
    order=pickle.load(f)
    f.close()
    return order

#this is the part of the code that reads the menu
def readOrders():
    f = open('orderDB.pkl','rb')
    order=pickle.load(f)
    f.close()
    return order

#this is where when you click the food you want then it orders it for you
@app.route('/order/<foodname>')
def orderpage(foodname):
    Orders = readOrders()
    username=request.cookies.get('username')
    
    Orders[username]=foodname
    
    print Orders

    f=open('orderDB.pkl','wb')
    pickle.dump(Orders,f,pickle.HIGHEST_PROTOCOL)
    f.close()
    
    f=open('mainMenu.pkl','rb')
    mainMenu=pickle.load(f)
    f.close()
    
    foodname=mainMenu[foodname]['foodname']
    foodimage=mainMenu[foodname]['foodimage']

    return render_template('orderSuccessful.html',username=username,foodname=foodname,foodimage=foodimage)
    
#this part gets the orders
@app.route('/getOrder')
def getOrder():
    if request.cookies.get('username')!='admin':
        return redirect('/accessDenied')
    orders=readOrders()
    
    finalOrder={}
    for person,food in orders.items():
        foodOrderers=finalOrder.get(food,[])
        foodOrderers.append(person)
        finalOrder[food]=foodOrderers

    return render_template("GetOrder.html",finalOrder=str(finalOrder))
    
#this is the part where you pick your food only staffs can access this
@app.route('/menuDesign', methods = ['GET'])
def menuDesign():
    f=open('mainMenu.pkl','rb')
    mainMenu=pickle.load(f)
    f.close()
    return render_template('menuDesign.html',mainMenu=mainMenu)

#this is where you see if staff are present
@app.route('/staffsDesign', methods = ['GET'])
def staffsDesign():
    f=open('mainStaffs.pkl','rb')
    staffs=pickle.load(f)
    f.close()
    return render_template('staffsDesign.html',staffs=staffs)

#this is the part when you say if the staffs are apsent or not
@app.route('/setStaffs', methods = ['POST'])
def setStaffs():
    if request.cookies.get('username')!='admin':
        return redirect('/accessDenied')
    staffs = request.form
    AvailableStaffs=[name.lower() for item, name in staffs.iteritems()]

    f=open('entitledStaffs.pkl','wb')
    pickle.dump(AvailableStaffs,f,pickle.HIGHEST_PROTOCOL)
    f.close()
    return redirect('/menuDesign')

#this is where the admin sets the menu of whats avalable 
@app.route('/setMenu', methods = ['POST'])
def setMenu():
    if request.cookies.get('username')!='admin':
        return redirect('/accessDenied')
    orders = request.form
    f=open('mainMenu.pkl','rb')
    mainMenu=pickle.load(f)
    f.close()
    f=open('menu.pkl','wb')
    AvailableOrders=[mainMenu[i] for i in orders]
    pickle.dump(AvailableOrders,f,pickle.HIGHEST_PROTOCOL)
    f.close()
    OpenThisSession()
    return render_template('setMenu.html', AvailableOrders = AvailableOrders)

#it brings you to access denied when you login as Admin 
@app.route('/accessDenied')
def accessDenied():
    return render_template('accessDenied.html')
    
@app.route('/Admin')
def adminAcces():
    if request.cookies.get('username')!='admin':
        return redirect('/accessDenied')
    f=open('sessionStatus.pkl','rb')
    sessionStatus=pickle.load(f)['sessionStatus']
    f.close()
    return render_template('Admin1.html',sessionStatus=sessionStatus)

@app.route('/Message/<message>')
def Message(message):
    messageIt(message)
    return 'fine!'

def messageItTo(messagee,message,phoneNumber):
    f=open('SMSMessages.pkl','rb')
    previousMessages=pickle.load(f)
    f.close()
    
    newMessage=str(previousMessages)+','+'|'.join((messagee,message,phoneNumber))


    f = open('SMSMessages.pkl', 'wb')
    pickle.dump(newMessage,f,pickle.HIGHEST_PROTOCOL)
    f.close()
    

def messageIt(message):
    
    f=open('entitledStaffs.pkl','rb')
    entitledStaffs=pickle.load(f)
    f.close()
    messageList=['|'.join((staff,message,str(UDB.getUserByName(staff).phoneNumber))) for staff in entitledStaffs]
 
    f = open('SMSMessages.pkl', 'wb')
    pickle.dump(str(messageList)[1:-1],f,pickle.HIGHEST_PROTOCOL)
    f.close()
    
def OpenThisSession():
    f=open('entitledStaffs.pkl','rb')
    entitledStaffs=pickle.load(f)
    f.close()
    #insert a message to b e sent
    messageIt(' Go Get Your Food At K-Cafe. URL ---> https://goo.gl/RyPm8e')
    
    f = open('orderDB.pkl', 'wb')
    pickle.dump({},f,pickle.HIGHEST_PROTOCOL)
    f.close()
    f = open('sessionStatus.pkl', 'wb')
    sessionStatus={'sessionStatus':'Open'}
    pickle.dump(sessionStatus,f,pickle.HIGHEST_PROTOCOL)
    f.close()
    return redirect('/Admin')

def CloseTheSession():
    #send the orders to the admin
    backupOrders() 
    f = open('sessionStatus.pkl', 'wb')
    sessionStatus={'sessionStatus':'Close'}
    pickle.dump(sessionStatus,f,pickle.HIGHEST_PROTOCOL)
    f.close()


@app.route('/OpenSession', methods = ['POST'])    
def OpenSession():
    OpenThisSession()
    return redirect('/getOrder')

    
@app.route('/CloseSession', methods = ['POST'])
def CloseSession():
    CloseTheSession()
    return redirect('/')

#this is when the session is closed and it brings you to 
@app.route('/kCafeClosed')
def kCafeClosed():
    return render_template('kCafeClosed1.html')
    
#this is where the mobile app comes in
@app.route('/mobile/<flag>')
def mobile(flag):
    if flag=='get':
        f=open('SMSMessages.pkl','rb')
        d = pickle.load(f)
        f.close()
        return str(d)
    elif flag=='done':
        f=open('SMSMessages.pkl','wb')
        pickle.dump([],f,pickle.HIGHEST_PROTOCOL)
        f.close()
        return 'good job'
def backupOrders():

    f=open('orderDB.pkl','rb')
    lastOrder=pickle.load(f)
    f.close()

    f=open('orderDB.pkl','wb')
    pickle.dump([],f,pickle.HIGHEST_PROTOCOL)
    f.close()
    

    f=open('backupDB.pkl','rb')
    backup=pickle.load(f)
    f.close()
    
    if lastOrder:
        print strftime("%a, %d %b %Y %H:%M:%S +1200", gmtime(time.time()+8*3600))
        backup.append({strftime("%a, %d %b %Y %H:%M:%S +1200", gmtime(time.time()+8*3600)):lastOrder})    
        print backup
        f=open('backupDB.pkl','wb')
        pickle.dump(backup,f,pickle.HIGHEST_PROTOCOL)
        f.close()
    
@app.route('/viewBackups')
def viewBackups():
    f=open('backupDB.pkl','rb')
    backup=pickle.load(f)
    f.close()
    import collections
    review=collections.OrderedDict({})
    for orders in backup:
        date= orders.keys()[0]
        order= orders.values()[0]
        fr = {}
        if order:
            for key,values in order.iteritems():
                try:
                    fr[values].append(key)
                except:
                    fr[values]=[key]
            review[date]=fr
    menu=readMenu()
    return render_template('reviewOrders.html',orders=review,menuItems=menu)

@app.route('/lastOrder')
def lastOrder():
    f=open('backupDB.pkl','rb')
    backup=pickle.load(f)
    f.close()
    import collections
    review=collections.OrderedDict({})
    for orders in backup:
        date= orders.keys()[0]
        order= orders.values()[0]
        fr = {}
        if order:
            for key,values in order.iteritems():
                try:
                    fr[values].append(key)
                except:
                    fr[values]=[key]
    review[date]=fr
    menu=readMenu()
    return render_template('reviewOrders.html',orders=review,menuItems=menu)

    
def initiate():
    backupOrders()    
    
    files=['usernameDB.pkl','sessionStatus.pkl','mainMenu.pkl','entitledStaffs.pkl','mainStaffs.pkl','orderDB.pkl','SMSMessages.pkl','menu.pkl']    
    for file in files:
        f=open(file,'wb')
        pickle.dump([],f,pickle.HIGHEST_PROTOCOL)
        f.close()

    def loadStaffs():
        f = open('mainStaffs.pkl', 'wb')
        Users=[
            {'phoneNumber':'','username':'admin','password':'kidocode', 'email':'email', 'userimage':'/static/theCreators.jpg'},
            {'phoneNumber':'0183552313','username':'maysam','password':'kidocode', 'email':'email', 'userimage':'/static/maysam.JPG'},
            {'phoneNumber':'01133443493','username':'arsham','password':'kidocode', 'email':'email', 'userimage':'/static/arsham.jpg'},
            {'phoneNumber':'0123896712','username':'kirshan','password':'kidocode', 'email':'email', 'userimage':'/static/kirshan.jpg'},
            {'phoneNumber':'0192529752','username':'mojgan','password':'kidocode', 'email':'email', 'userimage':'/static/mojgan.jpg'},
            {'phoneNumber':'0162436059','username':'unclecode','password':'kidocode', 'email':'email', 'userimage':'/static/unclecode.JPG'},
            {'phoneNumber':'0196947169','username':'hada','password':'kidocode', 'email':'email', 'userimage':'/static/hada.JPG'},
            {'phoneNumber':'0145875236','username':'jack','password':'kidocode', 'email':'email', 'userimage':'/static/jack.JPG'},
            {'phoneNumber':'0173299465','username':'diyana','password':'kidocode', 'email':'email', 'userimage':'/static/diyana.JPG'},
            {'phoneNumber':'0172930445','username':'dayana','password':'kidocode', 'email':'email', 'userimage':'/static/dayana.JPG'},
            {'phoneNumber':'0164100813','username':'oh kee hau','password':'kidocode', 'email':'email', 'userimage':'/static/ohkeehau.JPG'},
            {'phoneNumber':'0146326880','username':'sin jun lou','password':'kidocode', 'email':'email', 'userimage':'/static/sinjunlou.JPG'},
            {'phoneNumber':'01123638583','username':'son','password':'kidocode', 'email':'email', 'userimage':'/static/son.JPG'},
            {'phoneNumber':'0102184992','username':'thivya darshini','password':'kidocode', 'email':'email', 'userimage':'/static/thivyadarshini.JPG'},
            {'phoneNumber':'0163481917','username':'paulinelow','password':'kidocode', 'email':'email', 'userimage':'/static/paulinelow.JPG'},
            {'phoneNumber':'0149155023','username':'pavitra sheilian','password':'kidocode', 'email':'email', 'userimage':'/static/pavitrasheilian.JPG'},
            {'phoneNumber':'0183769177','username':'tabihta','password':'kidocode', 'email':'email', 'userimage':'/static/tabihta.JPG'},
            {'phoneNumber':'01136944320','username':'mohammed','password':'kidocode', 'email':'email', 'userimage':'/static/mohammed.JPG'},
            {'phoneNumber':'0127113659','username':'vee','password':'kidocode', 'email':'email', 'userimage':'/static/vee.JPG'},
            {'phoneNumber':'0167735612','username':'yvonne','password':'kidocode', 'email':'email', 'userimage':'/static/yvonne.JPG'},
            {'phoneNumber':'0176207706','username':'arash','password':'kidocode', 'email':'email', 'userimage':'/static/arash.JPG'},
            {'phoneNumber':'0133592566','username':'ash','password':'kidocode', 'email':'email', 'userimage':'/static/ash.JPG'},
            {'phoneNumber':'0193196261','username':'cho jian wei','password':'kidocode', 'email':'email', 'userimage':'/static/chojianwei.JPG'},
            {'phoneNumber':'0172594871','username':'cathy','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
            {'phoneNumber':'01126114850','username':'rocill','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
            {'phoneNumber':'0172324358','username':'anne','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
            {'phoneNumber':'0173217897','username':'ray','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
            {'phoneNumber':'0132632245','username':'zul','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
            {'phoneNumber':'0102000236','username':'sherrie','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
            {'phoneNumber':'01263441361','username':'shema','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
            {'phoneNumber':'0126108055','username':'adrian','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
            {'phoneNumber':'0173653623','username':'ani','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
            {'phoneNumber':'0123189266','username':'jacky','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
            {'phoneNumber':'01127669495','username':'erick','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
            {'phoneNumber':'0194549709','username':'muaz','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
            {'phoneNumber':'01139983301','username':'idris','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
            {'phoneNumber':'01121486100','username':'fatima','password':'kidocode', 'email':'email', 'userimage':'/static/kidocode.png'},
        ]
        pickle.dump(Users,f,pickle.HIGHEST_PROTOCOL)
        f.close()
        for new in Users:
            newUser=UDB.User(new)
            UDB.add(newUser)
    
    def loadFood():
        f = open('mainMenu.pkl', 'wb')
        mainMenu={
            'VegetablePasta':{'foodname':'VegetablePasta','foodimage':'/static/VegetablePasta.jpg'},
            'VegetableKebab':{'foodname':'VegetableKebab','foodimage':'/static/VegetableKebab.jpg'},
            'Tahchin':{'foodname':'Tahchin','foodimage':'/static/Tahchin.jpg'},
            'Kotlet':{'foodname':'Kotlet','foodimage':'/static/Kotlet.jpg'},
            'KhashKhashKebab':{'foodname':'KhashKhashKebab','foodimage':'/static/KhashKhashKebab.jpg'},
            'KebabKoobide':{'foodname':'KebabKoobide','foodimage':'/static/KebabKoobide.jpg'},
            'JoojeKebab':{'foodname':'JoojeKebab','foodimage':'/static/JoojeKebab.jpg'},
            'HotDog':{'foodname':'HotDog','foodimage':'/static/HotDog.jpg'},
            'GhormesabziStew':{'foodname':'GhormesabziStew','foodimage':'/static/GhormesabziStew.jpg'},
            'GheymeStew':{'foodname':'GheymeStew','foodimage':'/static/GheymeStew.jpg'},
            'GheymeAndEggPlantStew':{'foodname':'GheymeAndEggPlantStew','foodimage':'/static/GheymeAndEggPlantStew.jpg'},
            'CheeseBurger':{'foodname':'CheeseBurger','foodimage':'/static/CheeseBurger.jpg'},
            'CeleryStew':{'foodname':'CeleryStew','foodimage':'/static/CeleryStew.jpg'},
            'BreastChickenLari':{'foodname':'BreastChickenLari','foodimage':'/static/BreastChickenLari.jpg'},
            'BeefTongue':{'foodname':'BeefTongue','foodimage':'/static/BeefTongue.jpg'},
            'BeefTomatoPasta':{'foodname':'BeefTomatoPasta','foodimage':'/static/BeefTomatoPasta.jpg'},
            'LobiyaPolo':{'foodname':'LobiyaPolo','foodimage':'/static/LobiyaPolo.jpg'},
            'BarberryRiceChickenStew':{'foodname':'BarberryRiceChickenStew','foodimage':'/static/BarberryRiceChickenStew.jpg'},
            'JumboCheeseChickenHotDog':{'foodname':'JumboCheeseChickenHotDog','foodimage':'/static/JumboCheeseChickenHotDog.jpg'},
            'PepperoniBeefPizza7-Inch':{'foodname':'PepperoniBeefPizza7-Inch','foodimage':'/static/BeefPepperoniPizza.jpg'},
            'ChickenHawaiianPizza7-Inch':{'foodname':'ChickenHawaiianPizza7-Inch','foodimage':'/static/HawianChickenPizza.jpg','price':'RM13.50'},
            'AglioOlioMushroomSpaghetti':{'foodname':'AglioOlioMushroomSpaghetti','foodimage':'/static/AglioOlioMushroomSpaghetti.jpg'},
            'CheesyMushroomChickenBakedRice':{'foodname':'CheesyMushroomChickenBakedRice','foodimage':'/static/CheesyMushroomChickenBakedRice.jpg'},
            'BeefCarbonaraSpaghetti':{'foodname':'BeefCarbonaraSpaghetti','foodimage':'/static/beefCarbonaraSpaghetti.jpg'},
            'BologneseChickenSpaghetti':{'foodname':'BologneseChickenSpaghetti','foodimage':'/static/BologneseChickenSpaghetti.jpg'},
            'PadThaiSpicy':{'foodname':'PadThaiSpicy','foodimage':'/static/padThai.jpg'},
            'ChickenFriedRice':{'foodname':'ChickenFriedRice','foodimage':'/static/chickenFriedRice.jpg'},
            'Stir-FriedChickenBasilLeafSpicy':{'foodname':'Stir-FriedChickenBasilLeafSpicy','foodimage':'/static/Stir-FriedChickenBasilLeaf(Spicy).jpg'},
            'TomYamBihun':{'foodname':'TomYamBihun','foodimage':'/static/tomyamBihun.jpg'},
            'TomYamRice':{'foodname':'TomYamRice','foodimage':'/static/tomyamrice.jpg'},
            'FriedHorFun':{'foodname':'FriedHorFun','foodimage':'/static/friedhorfun.jpg'},
            'MushroomSoup':{'foodname':'MushroomSoup','foodimage':'/static/mushroomsoup.jpg'},
            'ChickenSliceAndCheeseCiabatta':{'foodname':'ChickenSliceAndCheeseCiabatta','foodimage':'/static/chickenslicecheeseciabatta.jpg'},
            'Bobcat(Beef)':{'foodname':'Bobcat(Beef)','foodimage':'/static/bobcatBeef.JPG'},
            'Bobcat(Chicken)':{'foodname':'Bobcat(Chicken)','foodimage':'/static/BobcatChicken.jpg'},
            'Tornado(Chicken)':{'foodname':'Tornado(Chicken)','foodimage':'/static/tornado.jpg'},
            'Bash(Beef)':{'foodname':'Bash(Beef)','foodimage':'/static/bashbeef.jpg'}
        }
        pickle.dump(mainMenu,f,pickle.HIGHEST_PROTOCOL)
        f.close()
        
        f = open('sessionStatus.pkl', 'wb')
        sessionStatus={'sessionStatus':'close'}
        pickle.dump(sessionStatus,f,pickle.HIGHEST_PROTOCOL)
        f.close()
        
        return 'done!'
        
    def loadMessages():
        f=open('SMSMessages.pkl','wb')
        pickle.dump([],f,pickle.HIGHEST_PROTOCOL)
        f.close()
    
    loadMessages()
    loadFood()
    loadStaffs()

#OpenThisSession()
initiate()

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 8080)
