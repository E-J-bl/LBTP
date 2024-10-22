# the Protocol is called LBTP for Low Bandwidth Transfer Protocol

# the end goal is a protocol that can be called like the bluetooth:
# include "BluetoothSerial.h"
# BluetoothSerial SerialBT;
#
# void setup() {
#  Serial.begin(115200);
#  SerialBT.begin("ESP32test"); //Bluetooth device name
#  Serial.println("The device started, now you can pair it with bluetooth!");
# }
# therefore any device in the network would have the protocol declared as part of the creation oof the application

class connected():
    """
    This is a class made to make the code more readable nothing else
    IT IS NOT FOR THE USER AND DOES NOTHING EXCEPT HOLD A TRUE OR FLASE
    Attributes 
    _________
    val
        true or false 
    """
    def __init__(self):
        self.val = False


class LBTP():
    def __init__(self, pins: list[int] = (37, 38, 39)):
        # the esp 32 board has 18 ATD pins
        # the protocol takes three to use for data transfer
        # like UART, I2C, SPI, PWM you can assign pins apon the
        # creation of the application for the esp32
        # by default the protocol uses GPIO 37,38,39

        # the following pins are available:
        # 1(GPIO 36)
        # 2(GPIO 37)
        # 3(GPIO 38)
        # 4(GPIO 39)
        # 5(GPIO 32)
        # 6(GPIO 33)
        # 7(GPIO 34)
        # 8(GPIO 35)
        # 9(GPIO 4)
        # 10(GPIO 0)
        # 11(GPIO 2)
        # 12(GPIO 15)
        # 13(GPIO 13)
        # 14(GPIO 12)
        # 15(GPIO 14)
        # 16(GPIO 27)
        # 17(GPIO 25)
        # 18(GPIO 26)
        self.pins = {i: [pins[i], connected()] for i in range(len(pins))}
        # i need to rewrite this so it can write to the pin on the board
        SET_UP_PINS()
        self.address_list = PING_LOCAL()
        self.address = CREATE_GLOBAL_ADDRESS(self.address_list)

    def set_up_pins(self):
        
#     i need to write a function to ping all pins and see if any are connected
#     once a connection is confirmed request the list of addresses
#     from the connected esp32.
#     from there create an address given the list of all addresses
#


"""
List of special characters that are used in the data transfer
i will be using a subset of the uni-code characters called the utf-32 that is specialised for 32 bits

"""
