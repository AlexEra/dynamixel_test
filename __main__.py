from dynamixel import *
from serialsupport import *


if __name__ == '__main__':
    while True:
        print("available ports: ", *serial_ports())
        port = input("input dynamixel port, or print <<e>> to shutdown: ")
        if port == 'e':
            print("quit")
            break

        addresses = [24, 30, 36]  # [64, 116, 132], Dynamixel MX-28AR
        dxl = Dynamixel(addresses, 1, 6, port, 830, 3210, 20)

        if dxl.open_port():
            dxl.enable_dynamixel_torque()
            while True:
                if input("Press any key to continue! (or <<e>> to quit!)") == 'e':
                    break

                dxl_goal_position = int(input("\ninput goal position: "))
                if not (830 <= dxl_goal_position <= 3210):
                    break
                dxl.move_position(dxl_goal_position)

                while True:
                    dxl_present_position = dxl.read_position()
                    if not (abs(dxl_goal_position - dxl_present_position) > dxl.dxl_threshold):
                        break

                dxl.disable_dynamixel_torque()
    dxl.close_dxl_port()
