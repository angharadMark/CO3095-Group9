class Actor:
    def __init__(self, name=None, role=None):
        self.name = name
        self.role = role

    def set_name(self):
        self.name = input("input the name of the actor")
    
    def set_role(self):
        self.role = input("input the role of the actor")

    def display_actor(self):
        print("Name:",self.name)
        print("Role:",self.role)
