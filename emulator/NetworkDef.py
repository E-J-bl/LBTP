# each esp_ins will be an instance of a simulated esp32 board so that
# i can develop any algorithms in python before transferring to c++
import math
import numpy as np


class Memory():
    """
    A representation of DRAM that simulates direct memory editing that is commonly used in c and other middle level langauges

    Attributes
    ----------
    size: int
        The number of addresses 
    sreg: int
        the number of bits at each address
    aloc: dict
        The representation of which spaces in memory are allocated
    Methods
    -------
    __getitem__(key:int)
        How the user addresses into memory 
        
    __setitems__(key:int,value:int)
        How the user sets the memory value at a given address (given by key)
        does not support bulk allocation and does not protect the user from writing over previous data 
        WARNING
        _______
            Do not use. it does not protect the user and does not abstract away any proccess 
            if misused it will cause memory issues and can cause your program to start behaving unexpected 
            
    malloc(buffer:int)
        How to allocate a number of addresses to a process 
        buffer is the number of memory spaces you want
        Returns
        _______
            returns a start and end address where the buffer is set
    """

    def __init__(self, address_count, register_size):
        self.size = address_count
        self.sreg = register_size
        self.aloc = dict()
        # for explanation of this look at the malloc implementation
        for i in range(math.ceil(address_count / (register_size + 1))):
            self.aloc[i] = bin(0)

    def __getitem__(self, key: int):
        if key > self.size:
            raise IndexError
        if key == None:
            raise KeyError
        return self.aloc[key]

    def __setitem__(self, key: int, value: int):
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

        self.aloc[key] = bin(value)

    def malloc(self, buffer):
        found_space = False

        adre = 0
        while found_space:
            continuous_found = 0
            for i in range(self.sreg):
                if self.aloc[adre][i] == "0":
                    continuous_found += 1
                else:
                    continuous_found = 0
                if continuous_found == buffer:
                    mask = "0" * 32
                    for k in range(i - continuous_found, i):
                        mask[k] = 1

                    self.aloc[adre] = bin(int(self.aloc[adre], 2) + int(mask, 2))
                    print(True)
                    return adre * 32 + i
            adre += 1
            if adre > math.ceil(self.size / self.sreg + 1):
                found_space = True
                # that is not working  ahhhhhh

        return bin(0)


    def __str__(self):

        output = ()

        for address in range(1, self.size + 1):
            if address in self.aloc:
                output= output + (f"{self.aloc[address]:<{self.sreg + 3}}{address:<12}|",)
            else:
                output= output + (f"{bin(0):<{self.sreg + 3}}{address:<12}|",)

        output = [output[i:i + 100] for i in range(0, len(output), 100)]
        for part in range(len(output)):
            output[part] = [output[part][i:i + 20] for i in range(0, len(output[part]), 20)]

            output[part] = tuple(zip(*output[part]))

            output[part] = tuple("".join(output[part][i]) for i in range(len(output[part])))

            output[part] = "\n".join(output[part]+(("-" * 130)+"\n",))

        outp = "Current memory state:\n"+"_"*130+"\n"+"".join(output)

        return outp


#         change so that the code return a key (a pointer)
#         to where ever called it to act as the reference to that variable
#


#     to implement:
#         a way to allocate bulk amount of memory for
#         a process, so it does not need to claim
#         that space in individual address calls

#         and so that they can claim continuous space after
#         i have refactored the code to the specification above

class Pin():
    """
    A class to simulate a pin of the board 

    Attributes
    ----------
    board:
        this is the esp_ins board the pin is bound to 
    destination:
        this is the pin that it may be linked to. does not need to be defined at initialisation
    Methods
    -------
    send_data(data:any)
        This function is left undefined untill the protocol called to define it
        it would typically look like 
            self.destination.interrupt(data)
            
    interrupt()
        this is completely undefined until any process is allocated to the pin
        it is called by any process or simulated deviced that sends data to another pin 
    """

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

        self.destination: Pin
        self.board = board_name
        # this is to let the pin know which board it is bound
        # to the board will always know which pins it has however
        # when the pin receives data it needs to know where to send the data to

        self.received_data = []

    def send_data(self, data):
        pass
        # the actual functionality of what happens when a pin receives data will be covered by the protocol

    def interrupt(self):
        pass


class EspIns():
    """
    This is a simulated board and is used to simulate the network
    at the current version it can not execute code on itself and is only useful for simulating network structures

    Attributes
    ----------
    memory:
        this is a instance of a memory class which has 80000 addresses each are 32 bit
        for a overall DRAM of 320kb
    pins:
        this is a dictionary of 40 pin instances 
        all the pins are defined with the same behaviour unlike the real board however you are only advised to use
        certain pins to ensure any behaviour on the emulation lines up with your experience with real esp 32s
        the exact pins that should be used can be found at the protocol definition in the protocol file 

        
    Methods
    _______
    connect_pin(pin, address)
        this acts like wiring up two pins 
        the pin argument is a number from 0-39
        the address can be given in a few ways
            the pin itself can be entered as a pointer to the address
            or a reference to the pin can be provided in this format
                Destination_Board.pins[Pin_number]
    send(pin, data)
        to send data you select a pin and the data you want to send along that pin
        the pin does not need to be connected and the program will have no issue with sending data to a pin that is not connected
    """

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
        self.memory = Memory(80000, 32)

        # the esp32 has 40 pins total not all are ATD and some are only input
        # the exact function of each pin is shown here:
        #         https://www.flux.ai/p/blog/esp32-pinout-everything-you-need-to-know

        # only 18 are GPIO with ATD and more information about those are in
        # the definition of LBTP in the protocol directory
        self.pins = {i: Pin(self) for i in range(0, 39)}

        # each pin is bound to the board but some will also be bound to some other board later

    def connect_pin(self, pin, address) -> int:
        # As this is a emulator of an esp32 i have to create a function to
        # represent the act of plugging a pin into a wire
        self.pins[pin] = address

        return 0

    def send(self, pin, data):
        self.pins[pin].send_data(data)
