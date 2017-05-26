import pickle

class Question(object):
    def GenerateQid(self):
        qs=read()
        if qs:
            return len(qs)+1
        else:
            return 1
        
    def __init__(self, questionInfo):
        self.questionText = questionInfo.get("questionText")
        self.QID = questionInfo.get("QID",self.GenerateQid())
        self.votes= questionInfo.get('votes',0)
        self.date=questionInfo.get('date',0) 
        self.views=questionInfo.get('views',0)
        self.answers=questionInfo.get('answers',0)
        self.by=questionInfo.get('by',0)
        self.cat=questionInfo.get('cat',[])
'''
def update(QUESTIONS):
    QS=[]
    for q in QUESTIONS:
        QS.append(Question(q.__dict__))
    return QS
'''

def read():
    try:
        f=open('questionDB.pkl','rb')
        QUESTIONS=pickle.load(f)
        f.close()
        return QUESTIONS
    except:
        f=open('questionDB.pkl','wb')
        pickle.dump([], f , pickle.HIGHEST_PROTOCOL)
        f.close() 
        return []

def add(Q):
    qs=read()
    qs.append(Q)

    f=open('questionDB.pkl','wb')
    pickle.dump(qs, f , pickle.HIGHEST_PROTOCOL)
    f.close()
    
    return 'question added to db successfully'


def Qupdate(editedQuestion):
    qs=read()
    otherQ=[]
    for q in qs:
        if q.QID==editedQuestion.QID:
            myQ=q
        else:
            otherQ.append(q)
    
    otherQ.append(editedQuestion)
    f=open('questionDB.pkl','wb')
    pickle.dump(otherQ, f , pickle.HIGHEST_PROTOCOL)
    f.close()

def getQuestionByID(QID):
    qs=read()
    for q in qs:
        if q.QID==QID:
            return q
    return 'There is not such a question sir!'
    
def getQuestionByIDs(QIDs):
    qs=read()
    qlist=[]
    for q in qs:
        if q.QID in QIDs:
            qlist.append(q)
    return qlist