from dynamixel_sdk import *
import serial


class Dynamixel:
    def __init__(self, addresses, protocol, dxl_id, device_name, min_pos, max_pos, threshold, bd=57600):
        # Control table address
        self.address_mx_torque_enable = addresses[0]  # Control table address is different in Dynamixel model
        self.address_mx_goal_position = addresses[1]
        self.address_mx_pos = addresses[2]

        # Protocol version
        self.protocol_ver = protocol  # See which protocol version is used in the Dynamixel

        # Default setting
        self.dxl_id = dxl_id  # Dynamixel ID
        self.baud_rate = bd  # Dynamixel default baudrate : 57600
        self.device_name = device_name  # Check which port is being used on your controller
        # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

        self.torque_enable = 1  # Value for enabling the torque
        self.torque_disable = 0  # Value for disabling the torque
        self.dxl_min_pos = min_pos  # Dynamixel will rotate between this value
        self.dxl_max_pos = max_pos  # and this value
        self.dxl_threshold = threshold  # Dynamixel moving status threshold

        self.portHandler = PortHandler(self.device_name)  # get methods and members of Linux or Windows ports

        self.packetHandler = PacketHandler(self.protocol_ver)  # Protocol1PacketHandler or Protocol2PacketHandler

    def open_port(self):
        try:
            self.portHandler.openPort()
            print("Connected")
        except serial.SerialException:
            print("Failed to open the port")
            return False

        # Set port baud_rate
        if self.portHandler.setBaudRate(self.baud_rate):
            print("Succeeded to change the baudrate")
            return True
        else:
            print("Failed to change the baudrate")
            return False

    def move_position(self, dxl_goal_position):
        """Write Dynamixel goal position"""
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.dxl_id,
                                                                       self.address_mx_goal_position, dxl_goal_position)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))

    def read_position(self):
        """Read Dynamixel present position"""
        dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler,
                                                                                            self.dxl_id,
                                                                                            self.address_mx_pos)
        if dxl_comm_result != COMM_SUCCESS:
            print(self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print(self.packetHandler.getRxPacketError(dxl_error))

        print("[ID:%03d] PresPos:%03d\n" % (self.dxl_id, dxl_present_position))
        return dxl_present_position

    def _send_one_byte(self, address, byte):
        return self.packetHandler.write1ByteTxRx(self.portHandler, self.dxl_id, address, byte)

    def enable_dynamixel_torque(self):
        """Enable Dynamixel Torque"""
        dxl_comm_result, dxl_error = self._send_one_byte(self.address_mx_torque_enable, self.torque_enable)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("Dynamixel#%d has been successfully connected" % self.dxl_id)

    def disable_dynamixel_torque(self):
        """Disable Dynamixel Torque"""
        dxl_comm_result, dxl_error = self._send_one_byte(self.address_mx_torque_enable, self.torque_disable)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))

    def close_dxl_port(self):
        self.portHandler.closePort()

    def change_id(self, address, new_id):
        """Change Dynamixel id"""
        dxl_comm_result, dxl_error = self._send_one_byte(address, new_id)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("Dynamixel#%d has been change id to %d" % self.dxl_id % new_id)
