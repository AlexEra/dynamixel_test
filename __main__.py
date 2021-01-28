from dynamixel import *
from serialsupport import *


if __name__ == '__main__':
    while True:
        print("available ports: ", *serial_ports())
        port = input("input dynamixel port, or print <<e>> to shutdown: ")
        if port == 'e':
            print("quit")
            quit()

        addresses = [64, 116, 132]
        dxl = Dynamixel(addresses, 1, 1, port, 100, 4000, 10)

        if dxl.open_port():
            dxl.enable_dynamixel_torque()

            while True:
                print("Press any key to continue! (or press ESC to quit!)")
                if getch() == chr(0x1b):
                    break

                dxl_goal_position = 4000
                dxl.move_position(dxl_goal_position)

                while True:
                    dxl_present_position = dxl.read_position()
                    if not (abs(dxl_goal_position - dxl_present_position) > dxl.dxl_threshold):
                        break

                dxl.torque_disable()
                dxl.close_dxl_port()
