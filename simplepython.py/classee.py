tab=[]
class person:
    def __init__(self, a='admin'):
        self.loginname=a
        tab.insert(len(tab),a)
        print(tab)
    def get_loginname(self):
        return self._loginname
    def set_loginname(self, a):
        tab.insert(len(tab),a)
        if a in tab:
            print("already taken")
        else:
            self._speed=a
            print(a)
            return
    loginname=property(get_loginname, set_loginname)
    
c1=person()
c1.loginname=input('your login name:')

