import pickle

class Answer(object):
    def GenerateAid(self):
        ans=read()
        if ans:
            return len(ans)+1
        else:
            return 1
        
    def __init__(self, ansInfo):
        self.answerText = ansInfo.get("answerText")
        self.AID = ansInfo.get("AID",self.GenerateAid())
        self.votes= ansInfo.get('votes',0)
        self.date=ansInfo.get('date',0) 
        self.QID=ansInfo.get('QID',0)
        self.by=ansInfo.get('by',0)
'''
def update(QUESTIONS):
    QS=[]
    for q in QUESTIONS:
        QS.append(Question(q.__dict__))
    return QS
'''

def read():
    try:
        f=open('answerDB.pkl','rb')
        ANSWERS=pickle.load(f)
        f.close()
        return ANSWERS
    except:
        f=open('answerDB.pkl','wb')
        pickle.dump([], f , pickle.HIGHEST_PROTOCOL)
        f.close() 
        return []

def add(A):
    ans=read()
    ans.append(A)

    f=open('answerDB.pkl','wb')
    pickle.dump(ans, f , pickle.HIGHEST_PROTOCOL)
    f.close()
    
    return 'answer added to db successfully'


def Aupdate(editedAnswer):
    ans=read()
    otherA=[]
    for a in ans:
        if a.AID==editedAnswer.AID:
            myA=a
        else:
            otherA.append(a)
    
    otherA.append(editedAnswer)
    f=open('answerDB.pkl','wb')
    pickle.dump(otherA, f , pickle.HIGHEST_PROTOCOL)
    f.close()

def getAnswerByIDs(AIDs):
    ans=read()
    answers=[]
    for a in ans:
        if a.AID in AIDs:
            answers.append(a)
    return answers