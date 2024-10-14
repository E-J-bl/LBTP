# each esp_ins will be a instance of a simulated esp32 board so that
# i can develop any algorithms in python before transferring to c++

class memory():
    def __init__(self, address_count, register_size):
        self.size = address_count
        self.sreg = register_size
        self.aloc = dict()

    def __getitem__(self, key: int):
        if key > self.size:
            raise IndexError
        if key == None:
            raise KeyError
        return self.aloc[key]

    def __setitems__(self, key: int, value: int):
        #         abstract so that the process setting the value
        #         does not need to know the address that it is setting to
        #
        #         this is to prevent the coder from
        #         having to know which spaces in memory are already allocated
        #         this reduces the chance of errors in processes such as the protocol
        #         which require space allocated to them to be unchanged
        #         however the user may not know which space has been allocated
        #         to each protocol

        if key > self.size:
            raise IndexError
        if key == None:
            raise KeyError
        if value > 2 ** 32:
            raise ValueError

        self.aloc[key] = value


#         change so that the code return a key (a pointer)
#         to where ever called it to act as the reference to that variable
#


#     to implement:
#         a way to allocate bulk amount of memory for
#         a process, so it does not need to claim
#         that space in individual address calls

#         and so that they can claim continuous space after
#         i have refactored the code to the specification above

class pin():
    def __init__(self, board_name):
        # A unique class was made for the pin so that when the esp_ins
        # sends data to a pin it literally sends the data out of its memory into another place
        # this better reflects reality making thereby the system more intuitive

        # it also allows me to avoid errors if the esp_ins tried to send data along a path that does not exist
        # as can often happen when the esp_ins is in its initialisation process
        # In reality an esp32 experiences no issue with turning on a pin without it being connected however if
        # i allowed the esp_ins to send data directly along paths that are static and innate to the class then it
        # would crash as it tries to address a place in memory that is not initialised
        # therefore creating a layer of abstraction in a separate class for the pin would protect the system
        # from errors and would allow me to define the behavior of a pin in a cleaner layer

        self.destination:pin
        self.board = board_name
        # this is to let the pin know which board it is bound
        # to the board will always know which pins it has however
        # when the pin receives data it needs to know where to send the data to


        self.received_data = []

    def send_data(self, data):
        self.destination.received_data.append(data)
    # the actual functionality of what happens when a pin receives data will be covered by the protocol


class esp_ins():
    # the structure of this simulated network is
    # nodes of esp_ins (which stand for esp32 instances)
    # which are connected directly to their neighbours

    # each esp_ins has a global address which will be determined
    # after it is connected to the network
    # each node will refer to its neighbours by the pin address they are connected by
    # therefore the local name is different to the global address

    # to send data the esp_ins calls a pin
    # and that pin may or may not be connected
    # if it is the data is sent to
    # the memory of the other node

    # a simplified version of the network can be shown in simplified_network

    def __init__(self):
        # esp32 have 320 kb of dram
        # the esp32 is a 32 bit system so there are
        # 80000 addresses
        self.memory = memory(80000, 32)

        # the esp32 has 40 pins total not all are ATD and some are only input
        # the exact function of each pin is shown here:
        #         https://www.flux.ai/p/blog/esp32-pinout-everything-you-need-to-know

        # only 18 are GPIO with ATD and more information about those are in
        # the definition of LBTP in the protocol directory
        self.pins = {i: pin(self) for i in range(0, 39)}

        # each pin is bound to the board but some will also be bound to some other board later

    def connect_pin(self, pin, address) -> int:
        # As this is a emulator of an esp32 i have to create a function to
        # represent the act of plugging a pin into a wire
        self.pins[pin] = address
        # An address will be a custom data type representing a board and a specific pin
        # however for now the address with be the individual memory address of the pin it wants to connect to

        return 0

    def send(self, pin, data):
        self.pins[pin].send_data(data)
