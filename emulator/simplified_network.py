class node():
    def __init__(self, val):
        # when a node is created it has some data in it
        # it also has a register which acts like the memory in the full esp32
        # and it only has one pin because i do not need any more for a demonstration

        self.val = val
        self.reg = 0
        self.pin = 0

    def connect(self, address):
        # this tells both nodes that they are connected to each other
        self.pin = address
        address.pin=self

    def send(self, address):
        address.receive(self.val)

    def receive(self, value):
        self.reg = value

    def __str__(self):
        # this just tells python how to print a node

        pindef = 0
        if self.pin != 0:
            pindef = id(self.pin)
        return f"val {self.val} reg {self.reg} pin {pindef}"




n1 = node(1)

n2 = node(2)


print(f"n1 is equal to {n1}")
print(f"n2 is equal to {n2}")
n1.connect(n2)
print(f"\nAfter the two are connected then \n n1 is this {n1}\n n2 is this {n2}"
      f"\n the pins are set to this number because that is a literal place in memory that they are pointing to")


n1.send(n2)
print(f"\nAfter n1 sends some data they look like \n"
      f"{n1}\n"
      f"{n2}")

n2.send(n1)
print(f"\nAfter n2 sends some data they look like: \n"
      f"{n1}\n"
      f"{n2}")
