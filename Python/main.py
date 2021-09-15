
import egm_pb2
import select
import numpy as np
import socket

Robot_Position_Flag = False  # For saving current robot coordinates

class EGM(object):

    def __init__(self, port=6511):

        self.socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('',port))
        self.send_sequence_number=0
        self.egm_addr=None
        self.count=0

    def receive_from_robot(self, timeout=0):

        s=self.socket
        s_list=[s]
        try:
            res=select.select(s_list, [], s_list, timeout)
        except select.error as err:
            if err.args[0] == errno.EINTR:
                return False, None
            else:
                raise

        if len(res[0]) == 0 and len(res[2])==0:
            return False, None
        try:
            (buf, addr)=s.recvfrom(65536)
        except:
            self.egm_addr=None
            return False, None

        self.egm_addr=addr

        robot_message=egm_pb2.EgmRobot()
        robot_message.ParseFromString(buf)

        Robot_pos = None
        joint_angles=None
        rapid_running=False
        motors_on=False
        global Robot_Position_Flag

        if robot_message.HasField('feedBack'):
            if Robot_Position_Flag == False:
                Robot_pos = robot_message.feedBack.cartesian.pos
                Robot_Position_Flag = True
            Joints = robot_message.feedBack.joints.joints
            print(robot_message.feedBack.joints.joints)
        if robot_message.HasField('rapidExecState'):
            rapid_running = robot_message.rapidExecState.state == robot_message.rapidExecState.RAPID_RUNNING
        if robot_message.HasField('motorState'):
            motors_on = robot_message.motorState.state == robot_message.motorState.MOTORS_ON

        return True, Robot_pos,Joints

    def send_to_robot_joints(self, joint_angles):

        if not self.egm_addr:
            return False

        self.send_sequence_number+=1

        sensorMessage=egm_pb2.EgmSensor()

        header=sensorMessage.header
        header.mtype=egm_pb2.EgmHeader.MessageType.Value('MSGTYPE_CORRECTION')
        header.seqno=self.send_sequence_number
        self.send_sequence_number+=1

        planned=sensorMessage.planned

        if joint_angles is not None:
            joint_angles2 = list(np.rad2deg(cartesian))
            print(joint_angles2)
            print(planned.joints.joints)
        buf2=sensorMessage.SerializeToString()

        try:
            self.socket.sendto(buf2, self.egm_addr)
        except:
            return False

        return True

    def send_to_robot_cartesian(self, Position, Rob_pos):

        if not self.egm_addr:
            return False

        self.send_sequence_number+=1

        sensorMessage=egm_pb2.EgmSensor()

        header=sensorMessage.header
        header.mtype=egm_pb2.EgmHeader.MessageType.Value('MSGTYPE_CORRECTION')
        header.seqno=self.send_sequence_number
        self.send_sequence_number+=1

        planned=sensorMessage.planned

        if Position is not None:
            planned.cartesian.pos.x = Rob_pos.x + Position[2]
            planned.cartesian.pos.y = Rob_pos.y + Position[0]
            planned.cartesian.pos.z = Rob_pos.z + Position[1]
            planned.cartesian.euler.x = -90
            planned.cartesian.euler.y = 180
            planned.cartesian.euler.z = 0
            print(planned.cartesian.pos)
        buf2=sensorMessage.SerializeToString()

        try:
            self.socket.sendto(buf2, self.egm_addr)
        except:
            return False

        return True

EGM1 = EGM()

Current_Position = EGM1.receive_from_robot()[1]
print(Current_Position)

Position = (10,100,10)  # Random x y z for testing

Joints = [0,0,0,0,0,0]  # Random joint angles for testing

while True:
    
    EGM1.send_to_robot_cartesian(Position,Current_Position)
    #Egm.send_to_robot_cartesian(Position)
