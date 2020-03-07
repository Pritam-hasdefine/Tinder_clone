from GUIhelper import GUIhelper
from DBhelper import DBhelper


class Tinder(GUIhelper):
    def __init__(self):
        self.db = DBhelper()
        super(Tinder, self).__init__(self.loginListner, self.loadRegWindow)  # calling child by parent

    # creating a function
    def loginListner(self):
        data = self.db.search('email', self._emailInput.get(), 'password', self._passwordInput.get(), 'users')
        print(data)

        if len(data) == 1:
            self.sessionId=data[0][0]
            self.loadProfile()
        else:
            self.label5.configure(text="Login Failed")

    def loadRegWindow(self):
        self.regWindow(self.registrationHandler)

    def registrationHandler(self):
        if self._nameInput.get() == "" or self._emailInput.get() == "" or self._passwordInput.get() == "" or self._genderInput.get() == "" or self._ageInput.get() == "" or self._cityInput.get() == "":
            self.label2.configure(text="PLEASE FILL ALL DETAILS", bg="yellow", fg="red")
        else:
            regDict = {}
            regDict['user_id'] = "NULL"
            regDict['NAME'] = self._nameInput.get()
            regDict['EMAIL'] = self._emailInput.get()
            regDict['PASSWORD'] = self._passwordInput.get()
            regDict['GENDER'] = self._genderInput.get()
            regDict['AGE'] = self._ageInput.get()
            regDict['CITY'] = self._cityInput.get()

            print(regDict)
            response = self.db.insert(regDict, 'users')
            print('users')

            if response == 1:
                obj = GUIhelper(self.loginListner, self.loadRegWindow)
                self.label2.configure(text="Registration Successfull ", bg="white", fg="green")
            else:
                self.label2.configure(text="Registration Failed ", bg="red", fg="Yellow")


    def loadProfile(self):
        data=self.db.searchOne('user_id',self.sessionId,'users',"LIKE")
        self.mainWindow(self,data,mode=1)

    def viewProfile(self,num):
            title="Error"
            text="[+] Can't Load Data"
            data = self.db.searchOne('user_id', self.sessionId, 'users',"NOT LIKE")
            new_data=[]
            if num<0 or num>len(data)-1:
                self.message(title,text)
            else:
                new_data.append(data[num])
                self.mainWindow(self,new_data,mode=2,num=num)

    def propose(self,juliet_id):
        data=self.db.search('romeo_id',str(self.sessionId),'juliet_id',str(juliet_id),'proposals')
        if len(data)==0:
            proDict={}
            proDict['romeo_id']=str(self.sessionId)
            proDict['juliet_id']=str(juliet_id)
            response=self.db.insert(proDict,'proposals')
            if response ==1:
                self.message("Congrats","Proposal Sent Successfully")
            else:
                self.message("Tough Luck","Proposal Failed Try Again")
        else:
            self.message("Error","Despo")

obj = Tinder()
