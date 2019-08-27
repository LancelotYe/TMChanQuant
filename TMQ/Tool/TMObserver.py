class Publisher:
    def __init__(self, *args, **kwargs):
        pass

    def register(self, *args, **kwargs):
        pass

    def unregister(self, *args, **kwargs):
        pass

    def notifyAll(self, *args, **kwargs):
        pass


class TechForum(Publisher):
    def __init__(self):
        super(TechForum, self).__init__()
        self._listOfUsers = []
        self.postname = None
        
    def register(self, userObj):
        if userObj not in self._listOfUsers:
            self._listOfUsers.append(userObj)

    def unregister(self, userObj):
        self._listOfUsers.remove(userObj)

    def notifyAll(self):
        for objects in self._listOfUsers:
            objects.notify(self.postname)

    def writeNewPost(self , postname):
        self.postname = postname
        self.notifyAll()


class Subscriber:
    def __init__(self, *args, **kwargs):
        pass

    def notify(self, *args, **kwargs):
        pass


class User1(Subscriber):
    def notify(self, postname):
        print("User1 notified of a new post %s" % postname)


class User2(Subscriber):
    def notify(self, postname):
        print("User2 notified of a new post %s" % postname)


class SisterSites(Subscriber):
    def __init__(self):
        super(SisterSites, self).__init__()
        self._sisterWebsites = ["Site1" , "Site2", "Site3"]

    def notify(self, postname):
        for site in self._sisterWebsites:
                print("Send nofication to site:%s " % site)



if __name__ == "__main__":
    techForum = TechForum()

    user1 = User1()
    user2 = User2()
    sites = SisterSites()

    techForum.register(user1)
    techForum.register(user2)
    techForum.register(sites)


    techForum.writeNewPost("Observe Pattern in Python")

    techForum.unregister(sites)

    techForum.writeNewPost("MVC Pattern in Python")