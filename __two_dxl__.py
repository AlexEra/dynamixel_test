from dynamixel import *
from serialsupport import *
import time


if __name__ == '__main__':
    print("available ports: ", *serial_ports())
    port = input("input dynamixel port, or print <<e>> to shutdown: ")
    if port == 'e':
        print("quit")
        quit()

    dxl_goal_positions_0 = [900, 1000, 1100, 1200, 2300, 2400, 2500, 3000, 3100]
    dxl_goal_positions_1 = [3100, 3000, 2500, 2400, 2300, 1200, 1100, 1000, 900]

    addresses = [24, 30, 36]  # Dynamixel MX-28AR
    dxl = Dynamixel(addresses, 1, 10, port, 830, 3210, 20)

    packetHandler = PacketHandler(1)

    if dxl.open_port():
        dxl.enable_dynamixel_torque()
        dxl.dxl_id = 6
        dxl.enable_dynamixel_torque()
        while True:
            if input("Press any key to continue! (or <<e>> to quit!)") == 'e':
                break

            for p_0, p_1 in zip(dxl_goal_positions_0, dxl_goal_positions_1):
                if not (830 <= p_0 <= 3210 and 830 <= p_1 <= 3210):
                    break
                dxl.dxl_id = 10
                dxl.move_position(p_0)
                dxl.dxl_id = 6
                dxl.move_position(p_1)
                time.sleep(1)

            dxl.dxl_id = 10
            dxl.disable_dynamixel_torque()
            dxl.dxl_id = 6
            dxl.disable_dynamixel_torque()
    dxl.close_dxl_port()
