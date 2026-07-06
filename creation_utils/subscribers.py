class Subscriber:
    def __init__(self, sid, role, phone, country):
        self.sid = sid
        self.role = role
        self.phone = phone
        self.country = country
        self.contacts = []