import threading
# 消息发布
class Publisher:
    def __init__(self, *args, **kwargs):
        pass

    def register(self, *args, **kwargs):
        pass

    def unregister(self, *args, **kwargs):
        pass

    def notifyAll(self, *args, **kwargs):
        pass

# 通知中心（单利）
class NotificationCenter(Publisher):
    _instance_lock = threading.Lock()

    def __init__(self):
        super(NotificationCenter, self).__init__()
        self._listOfUsers = []
        self.notifiation = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(NotificationCenter, "_instance"):
            with NotificationCenter._instance_lock:
                if not hasattr(NotificationCenter, "_instance"):
                    NotificationCenter._instance = object.__new__(cls)
        return NotificationCenter._instance

    def register(self, userObj):
        if userObj not in self._listOfUsers:
            self._listOfUsers.append(userObj)

    def unregister(self, userObj):
        self._listOfUsers.remove(userObj)

    def notifyAll(self):
        print(self._listOfUsers)
        for objects in self._listOfUsers:
            objects.notify(self.notifiation)

    def postNotification(self, notifiation):
        self.notifiation = notifiation
        self.notifyAll()


# 接受者
class Receiver:
    def __init__(self, *args, **kwargs):
        pass

    def notify(self, *args, **kwargs):
        pass

# 通知
# class Notification(Receiver):
#     def notify(self, notifiation):
#         pass
#
#
# class User2(Receiver):
#     def notify(self, notifiation):
#         print("User2 notified of a new post %s" % notifiation)
#
#
# class SisterSites(Receiver):
#     def __init__(self):
#         super(SisterSites, self).__init__()
#         self._sisterWebsites = ["Site1" , "Site2", "Site3"]
#
#     def notify(self, postname):
#         for site in self._sisterWebsites:
#                 print("Send nofication to site:%s " % site)


#
# if __name__ == "__main__":
#     notificationCenter = NotificationCenter()
#
#     user1 = User1()
#     user2 = User2()
#     sites = SisterSites()
#
#     notificationCenter.register(user1)
#     notificationCenter.register(user2)
#     notificationCenter.register(sites)
#
#
#     notificationCenter.writeNewPost("Observe Pattern in Python")
#
#     notificationCenter.unregister(sites)
#
#     notificationCenter.writeNewPost("MVC Pattern in Python")