# MIT License

# Copyright (c) 2021 Mobot

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys, signal
import numpy as np
from io import BytesIO
from concurrent import futures
import threading
import grpc

import matplotlib.image as mpimg

import mobot.proto.mobot_pb2 as pb2
import mobot.proto.mobot_pb2_grpc as pb2_grpc
from .utils import Rate, get_logger
from mobot.server.utils import get_ip_address

class Sensor:
    def __init__(self, stub, MetadataClass, callback_func_name, logger):
        self._stub = stub
        self._MetadataClass = MetadataClass
        self._CallbackFunc = getattr(self._stub, callback_func_name)

        self.metadata = None
        self._logger = logger
        
    def RegisterCallback(self):
        try:
            success = self._CallbackFunc(pb2.Register(register=True))
            return success.success
        except grpc.RpcError:
            self._logger.error("Unable to Connect to server!")
            sys.exit()

    def UnRegisterCallback(self):
        try:
            success = self._CallbackFunc(pb2.Register(register=False))
            return False
        except grpc.RpcError:
            self._logger.error("Unable to Connect to server!")
            sys.exit()

    def GetTimeStampFromStampedData(self, data_stamped):
        timestamp = data_stamped.timestamp.milliseconds_since_epoch / 1000
        return timestamp

    def GetDataFromStampedData(self, data_stamped):
        pass

class Chassis(Sensor):
    def __init__(self, stub, logger):
        Sensor.__init__(self, stub, pb2.ChassisMetadata, "OdometryDataCallback", logger)
        self._logger = logger

    def set_cmd_vel(self, v, w):
        cmd_vel = pb2.DiffDriveVelocity(v=v, w=w)
        try:
            success = self._stub.SetCmdVel(cmd_vel)
            if success.success:
                return
            else:
                self._logger.error("Chassis Not Available!")
        except grpc.RpcError:
            self._logger.error("Unable to Connect to server!")
            sys.exit()

    def GetDataFromStampedData(self, data_stamped):
        odometry = np.array([\
            data_stamped.odometry.pose.position.x,\
            data_stamped.odometry.pose.position.y,\
            data_stamped.odometry.pose.yaw,\
            data_stamped.odometry.velocity.v,\
            data_stamped.odometry.velocity.w])
        timestamp = self.GetTimeStampFromStampedData(data_stamped)
        return odometry, timestamp

class Accelerometer(Sensor):
    def __init__(self, stub, logger):
        Sensor.__init__(self, stub, pb2.SensorMetadata, "AccelerometerDataCallback", logger)

    def GetDataFromStampedData(self, data_stamped):
        linear_acceleration = np.array([\
            data_stamped.linear_acceleration.x,\
            data_stamped.linear_acceleration.y,\
            data_stamped.linear_acceleration.z])
        timestamp = self.GetTimeStampFromStampedData(data_stamped)
        return linear_acceleration, timestamp

class Gyroscope(Sensor):
    def __init__(self, stub, logger):
        Sensor.__init__(self, stub, pb2.SensorMetadata, "GyroscopeDataCallback", logger)

    def GetDataFromStampedData(self, data_stamped):
        angular_velocity = np.array([\
            data_stamped.angular_velocity.x,\
            data_stamped.angular_velocity.y,\
            data_stamped.angular_velocity.z])
        timestamp = self.GetTimeStampFromStampedData(data_stamped)
        return angular_velocity, timestamp

class Magnetometer(Sensor):
    def __init__(self, stub, logger):
        Sensor.__init__(self, stub, pb2.SensorMetadata, "MagnetometerDataCallback", logger)

    def GetDataFromStampedData(self, data_stamped):
        orientation = np.array([\
            data_stamped.orientation.x,\
            data_stamped.orientation.y,\
            data_stamped.orientation.z,\
            data_stamped.orientation.w])
        timestamp = self.GetTimeStampFromStampedData(data_stamped)
        return orientation, timestamp

class Camera(Sensor):
    def __init__(self, stub, logger):
        Sensor.__init__(self, stub, pb2.CameraMetadata, "CameraDataCallback", logger)

    def GetDataFromStampedData(self, data_stamped):
        compressed_image = data_stamped.compressed_image.data
        image = np.array(mpimg.imread(BytesIO(compressed_image), format="jpg"))
        image = np.rot90(image)
        timestamp = self.GetTimeStampFromStampedData(data_stamped)
        return image, timestamp

class Agent(pb2_grpc.MobotServicer):
    def __init__(self):
        self._logger = get_logger()
        try:
            self._ip = get_ip_address()
        except:
            self._logger.error("Not Connected to any network!")
            sys.exit()
        self._port = "50051"
        self._channel = grpc.insecure_channel(self._ip + ':' + self._port)
        self._stub = pb2_grpc.MobotStub(self._channel)

        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=30))
        pb2_grpc.add_MobotServicer_to_server(self, self._server)
        self._server.add_insecure_port(f"{self._ip}:50052")

        self._server_on = False
        signal.signal(signal.SIGINT, self._signal_handler)

        self.chassis = Chassis(self._stub, self._logger)
        self.accelerometer = Accelerometer(self._stub, self._logger)
        self.gyroscope = Gyroscope(self._stub, self._logger)
        self.magnetometer = Magnetometer(self._stub, self._logger)
        self.camera = Camera(self._stub, self._logger)

        self.control_thread = threading.Thread(target=self.ControlThread)

        self._odometry_cb_busy = False
        self._accelerometer_cb_busy = False
        self._gyroscope_cb_busy = False
        self._magnetometer_cb_busy = False
        self._camera_cb_busy = False

    def start(self):
        if not self._server_on:
            self._server.start()
            self._server_on = True

            self.chassis.RegisterCallback()
            self.accelerometer.RegisterCallback()
            self.gyroscope.RegisterCallback()
            self.magnetometer.RegisterCallback()
            self.camera.RegisterCallback()

            rate = Rate(20)
            while self.chassis.metadata == None\
                or self.accelerometer.metadata == None\
                or self.gyroscope.metadata == None\
                or self.magnetometer.metadata == None\
                or self.camera.metadata == None:
                rate.sleep()
            self.control_thread.start()

    def wait_for_termination(self):
        self._server.wait_for_termination()

    def _signal_handler(self, signum, frame):
        if self._server_on:
            self._server_on = False
            self.chassis.UnRegisterCallback()
            self.accelerometer.UnRegisterCallback()
            self.gyroscope.UnRegisterCallback()
            self.magnetometer.UnRegisterCallback()
            self.camera.UnRegisterCallback()
            self._server.stop(0)

    def ok(self):
        return self._server_on

############## Grpc Callbacks #################
    def SetChassisMetaData(self, metadata, context):
        self.chassis.metadata = metadata
        return pb2.Success(success=True)

    def NewOdometryData(self, odometry_stamped, context):
        if not self._odometry_cb_busy:
            odometry, timestamp = self.chassis.GetDataFromStampedData(odometry_stamped)
            thread_odometry_cb = threading.Thread(target = self._OdometryCbThread, args=[odometry, timestamp])
            thread_odometry_cb.start()
        else:
            self._logger.warn("OdometryCb frame droped as it failed to meet target frame rate!")
        return pb2.Success(success=True)

    def SetAccelerometerMetaData(self, metadata, context):
        self.accelerometer.metadata = metadata
        return pb2.Success(success=True)

    def NewAccelerometerData(self, linear_acceleration_stamped, context):
        if not self._accelerometer_cb_busy:
            linear_acceleration, timestamp = self.accelerometer.GetDataFromStampedData(linear_acceleration_stamped)
            thread_accelerometer_cb = threading.Thread(target = self._AccelerometerCbThread, args=[linear_acceleration, timestamp])
            thread_accelerometer_cb.start()
        else:
            self._logger.warn("AccelerometerCb frame droped as it failed to meet target frame rate!")
        return pb2.Success(success=True)

    def SetGyroscopeMetaData(self, metadata, context):
        self.gyroscope.metadata = metadata
        return pb2.Success(success=True)

    def NewGyroscopeData(self, angular_velocity_stamped, context):
        if not self._gyroscope_cb_busy:
            angular_velocity, timestamp = self.gyroscope.GetDataFromStampedData(angular_velocity_stamped)
            thread_gytoscope_cb = threading.Thread(target = self._GyroscopeCbThread, args=[angular_velocity, timestamp])
            thread_gytoscope_cb.start()
        else:
            self._logger.warn("GyroscopeCb frame droped as it failed to meet target frame rate!")
        return pb2.Success(success=True)

    def SetMagnetometerMetaData(self, metadata, context):
        self.magnetometer.metadata = metadata
        return pb2.Success(success=True)

    def NewMagnetometerData(self, orientation_stamped, context):
        if not self._magnetometer_cb_busy:
            orientation, timestamp = self.magnetometer.GetDataFromStampedData(orientation_stamped)
            thread_magnetometer_cb = threading.Thread(target = self._MagnetometerCbThread, args=[orientation, timestamp])
            thread_magnetometer_cb.start()
        else:
            self._logger.warn("MagnetometerCb frame droped as it failed to meet target frame rate!")
        return pb2.Success(success=True)

    def SetCameraMetaData(self, metadata, context):
        self.camera.metadata = metadata
        return pb2.Success(success=True)

    def NewCameraData(self, compressed_image_stamped, context):
        if not self._camera_cb_busy:
            image, timestamp = self.camera.GetDataFromStampedData(compressed_image_stamped)
            thread_camera_cb = threading.Thread(target = self._CameraCbThread, args=[image, timestamp])
            thread_camera_cb.start()
        else:
            self._logger.warn("CameraCb frame droped as it failed to meet target frame rate!")
        return pb2.Success(success=True)
#################################################

############## Callbacks Threads #################
    def _OdometryCbThread(self, odometry, timestamp):
        self._odometry_cb_busy = True
        self.OdometryCb(odometry, timestamp)
        self._odometry_cb_busy = False
    def _AccelerometerCbThread(self, linear_acceleration, timestamp):
        self._accelerometer_cb_busy = True
        self.AccelerometerCb(linear_acceleration, timestamp)
        self._accelerometer_cb_busy = False
    def _GyroscopeCbThread(self, angular_velocity, timestamp):
        self._gyroscope_cb_busy = True
        self.GyroscopeCb(angular_velocity, timestamp)
        self._gyroscope_cb_busy = False
    def _MagnetometerCbThread(self, orientation, timestamp):
        self._magnetometer_cb_busy = True
        self.MagnetometerCb(orientation, timestamp)
        self._magnetometer_cb_busy = False
    def _CameraCbThread(self, image, timestamp):
        self._camera_cb_busy = True
        self.CameraCb(image, timestamp)
        self._camera_cb_busy = False
#################################################

############## To be Overridden #################
    def ControlThread(self):
        pass

    def OdometryCb(self, odometry, timestamp):
        pass

    def AccelerometerCb(self, linear_acceleration, timestamp):
        pass

    def GyroscopeCb(self, angular_velocity, timestamp):
        pass

    def MagnetometerCb(self, orientation, timestamp):
        pass

    def CameraCb(self, image, timestamp):
        pass
#################################################

