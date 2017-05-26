import pickle

class User(object):
    def GenerateUID(self):
        MyUsers=users()
        if MyUsers:
            return len(MyUsers)+1
        else:
            return 1
    def __init__(self, userdata):
        self.UID = userdata.get("username",self.GenerateUID())
        self.username = userdata.get("username","NA")
        self.DOB = userdata.get("dob","NA")
        self.email= userdata.get("email","NA")
        self.nationality = userdata.get("nationality","NA")
        self.phoneNumber = userdata.get("phoneNumber","NA")
        self.password = userdata.get("password","NA")
        self.votes= userdata.get("voteID",[])
        self.regDate= userdata.get("regDate",0) #Today
        self.viewsID=userdata.get("viewsID",[])
        self.userimage=userdata.get("userimage","NA")
        self.questionsID=userdata.get("questionsID",[])
        self.answersID=userdata.get("answersID",[])
        self.active=userdata.get("active",True)

def users():
    try:
        f=open('usernameDB.pkl','rb')
        USERS=pickle.load(f)
        f.close()
    except:
        return False
    return USERS

def getUserByName(username):
    MyUsers=users()
    if MyUsers:
        for u in MyUsers:
            if u.username==username:
                return u
        else:
            return False
    else:
        return False


def getUserByID(UID):
    MyUsers=users()
    if MyUsers:
        for u in MyUsers:
            if u.UID==UID:
                return u
        else:
            return False
    else:
        return False
    
    
def update(editedUser):
    allUsers=users()
    newUsers=[]
    if allUsers:
        for user in allUsers:
            if user.username==editedUser.username:
                newUsers.append(editedUser)
            else:
                newUsers.append(user)

        f=open('usernameDB.pkl','wb')
        pickle.dump(newUsers, f , pickle.HIGHEST_PROTOCOL)
        f.close()
        return 'database successfully updated'
    else:
        return 'database is empty dude!'

def access(username,password):
    allUsers=users()
    if allUsers:
        for user in allUsers:
            if user.username==username and user.password==password:
                return True
    return False    
        

def add(user):
    if getUserByName(user.username):
        return 'username already exist'
    elif user.email=="NA":
        return 'user email is a must'
    elif user.password=="NA":
        return 'so how come! you need a password idiot!'
    else:    
        MyUsers=users()
        if MyUsers:
            MyUsers.append(user)
        else:
            MyUsers=[]
            MyUsers.append(user)
            
        f=open('usernameDB.pkl','wb')
        pickle.dump(MyUsers, f , pickle.HIGHEST_PROTOCOL)
        f.close()
        return 'user added to db successfully'