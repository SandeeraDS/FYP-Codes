class A:

    def __init__(self, id, name, availabilty):
        self.id = id
        self.name = name
        self.availabilty = availabilty


class B:
    my_objects = {}

    def __init__(self):
        pass

    def additem(self):
        for i in range(10):
            self.my_objects.update({i: A(i, "sandeera", True)})

    # later
    def viewitem(self):
        for obj in self.my_objects:
            print(self.my_objects[obj].id, end=" ")
            print(self.my_objects[obj].name, end=" ")
            print(self.my_objects[obj].availabilty)
        print("-------------------------------------------------------")

    def changevalue(self, id):
        # oldValue = self.my_objects[id]
        print(self.my_objects.__contains__(id))
        if self.my_objects.__contains__(id):
            self.my_objects.update({id: A(id, "sandeera_new", False)})
        else:
            self.my_objects.update({id: A(id, "sandeera_new_new", False)})


b = B()
b.additem()
b.viewitem()
b.changevalue(7)
b.viewitem()
b.changevalue(20)
b.viewitem()
