#!/usr/bin/python
import smbus
import time

class mpuSensor(object):
	"""docstring for mpuSensor"""
	MPU9150A_I2C_ADDR           = 0x69   #Device address jumper pos 1 (0xD2 >> 1)
	MAG_I2C_ADDR                = 0x0C       # Address of the magnetometer in bypass mode
	# MPU 9150A registers
	
	MPUREG_WHOAMI               = 0x75
	MPUREG_SMPLRT_DIV           = 0x19
	MPUREG_CONFIG               = 0x1A
	MPUREG_GYRO_CONFIG          = 0x1B
	MPUREG_ACCEL_CONFIG         = 0x1C
	MPUREG_FIFO_EN              = 0x23
	MPUREG_INT_PIN_CFG          = 0x37
	MPUREG_INT_ENABLE           = 0x38
	MPUREG_INT_STATUS           = 0x3A
	MPUREG_ACCEL_XOUT_H         = 0x3B
	MPUREG_ACCEL_XOUT_L         = 0x3C
	MPUREG_ACCEL_YOUT_H         = 0x3D
	MPUREG_ACCEL_YOUT_L         = 0x3E
	MPUREG_ACCEL_ZOUT_H         = 0x3F
	MPUREG_ACCEL_ZOUT_L         = 0x40
	MPUREG_TEMP_OUT_H           = 0x41
	MPUREG_TEMP_OUT_L           = 0x42
	MPUREG_GYRO_XOUT_H          = 0x43
	MPUREG_GYRO_XOUT_L          = 0x44
	MPUREG_GYRO_YOUT_H          = 0x45
	MPUREG_GYRO_YOUT_L          = 0x46
	MPUREG_GYRO_ZOUT_H          = 0x47
	MPUREG_GYRO_ZOUT_L          = 0x48
	MPUREG_USER_CTRL            = 0x6A
	MPUREG_PWR_MGMT_1           = 0x6B
	MPUREG_PWR_MGMT_2           = 0x6C
	MPUREG_FIFO_COUNTH          = 0x72
	MPUREG_FIFO_COUNTL          = 0x73
	MPUREG_FIFO_R_W             = 0x74

	#Magnetometer registers
	MAGREG_WIA            	    = 0x00    # Mag Who I Am
	MAGREG_AKM_ID         	    = 0x48    # Mag device ID
	MAGREG_ST1            	    = 0x02    # Magnetometer status 1
	MAGREG_HXL            	    = 0x03    # Mag X axis Low
	MAGREG_HXH            	    = 0x04    # Mag X axis High
	MAGREG_HYL            	    = 0x05    # Mag Y axis Low
	MAGREG_HYH            	    = 0x06    # Mag Y axis High
	MAGREG_HZL            	    = 0x07    # Mag Z axis Low
	MAGREG_HZH            	    = 0x08    # Mag Z axis High
	MAGREG_ST2            	    = 0x09    # Magnetometer status 2
	MAGREG_CNTL           	    = 0x0A    # Magnetometer control
	
	# Configuration bits
	BIT_SLEEP                   = 0x40
	BIT_H_RESET                 = 0x80
	BITS_CLKSEL                 = 0x07
	MPU_CLK_SEL_PLLGYROX        = 0x01
	MPU_CLK_SEL_PLLGYROZ        = 0x03
	MPU_EXT_SYNC_GYROX          = 0x02
	BITS_AFSL_SEL_2G            = 0x00
	BITS_AFSL_SEL_4G            = 0x08
	BITS_AFSL_SEL_8G            = 0x10
	BITS_AFSL_SEL_16G           = 0x18
	BITS_FS_250DPS              = 0x00
	BITS_FS_500DPS              = 0x08
	BITS_FS_1000DPS             = 0x10
	BITS_FS_2000DPS             = 0x18
	BITS_FS_MASK                = 0x18
	BITS_DLPF_CFG_256HZ_NOLPF2  = 0x00
	BITS_DLPF_CFG_188HZ         = 0x01
	BITS_DLPF_CFG_98HZ          = 0x02
	BITS_DLPF_CFG_42HZ          = 0x03
	BITS_DLPF_CFG_20HZ          = 0x04
	BITS_DLPF_CFG_10HZ          = 0x05
	BITS_DLPF_CFG_5HZ           = 0x06
	BITS_DLPF_CFG_2100HZ_NOLPF  = 0x07
	BITS_DLPF_CFG_MASK          = 0x07
	BIT_INT_ANYRD_2CLEAR        = 0x10
	BIT_RAW_RDY_EN              = 0x01
	BIT_I2C_IF_DIS              = 0x10
	BIT_INT_STATUS_DATA         = 0x01
	BIT_FIFO_EN                 = 0x78
	BIT_FIFO_DIS                = 0x00

	def __init__(self):
		self.accel= [0, 0, 0]
		self.gyro = [0, 0, 0]
		self.mag = [0, 0, 0]
		self.temp = 0.0;
		self.gdt = 0;
		self.calibAccel = [0, 0, 0]
		self.calibGyro =[0, 0, 0]
		self.magOff = [0, 0, 0]
		self.magScale = [0, 0, 0]
		bus= smbus.SMBus(1)
		bus.write_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_PWR_MGMT_1,self.BIT_H_RESET)
		time.sleep(0.01)
		bus.write_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_SMPLRT_DIV,0X00)
		bus.write_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_CONFIG, self.BITS_DLPF_CFG_42HZ)
		bus.write_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_GYRO_CONFIG,self.BITS_FS_1000DPS)
		bus.write_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_ACCEL_CONFIG,0X10)
		bus.write_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_FIFO_EN,self.BIT_FIFO_DIS)
		bus.write_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_INT_PIN_CFG,0X02)
		bus.write_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_INT_ENABLE,0X00)
		bus.write_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_USER_CTRL,0X00)
		bus.write_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_PWR_MGMT_1,0X00)
		bus.write_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_PWR_MGMT_2,0X00)
		bus.write_byte_data(self.MAG_I2C_ADDR,self.MAGREG_CNTL,0X01)
		time.sleep(0.01)

	def detect(self):
		bus= smbus.SMBus(1)
		d = bus.read_byte_data(self.MPU9150A_I2C_ADDR, self.MPUREG_WHOAMI)
		if d&0x7E == 0x68:
			return True
		return False		
	
	def readAccel(self):
		bus= smbus.SMBus(1)
		valueH=bus.read_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_ACCEL_XOUT_H)
		valueL=bus.read_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_ACCEL_XOUT_L)
		
		self.accel[0]=int(((valueH<<8) | valueL))


		valueH=bus.read_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_ACCEL_YOUT_H)
		valueL=bus.read_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_ACCEL_YOUT_L)
		self.accel[1]=int(((valueH<<8) | valueL))

		valueH=bus.read_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_ACCEL_ZOUT_H)
		valueL=bus.read_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_ACCEL_ZOUT_L)
		self.accel[2]=int(((valueH<<8) | valueL))

	def readGyro(self):
		bus= smbus.SMBus(1)
		valueH=bus.read_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_GYRO_XOUT_H)
		valueL=bus.read_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_GYRO_XOUT_L)
		self.gyro[0]=int(((valueH<<8) | valueL))

		valueH=bus.read_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_GYRO_YOUT_H)
		valueL=bus.read_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_GYRO_YOUT_L)
		self.gyro[1]=int(((valueH<<8) | valueL))

		valueH=bus.read_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_GYRO_ZOUT_H)
		valueL=bus.read_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_GYRO_ZOUT_L)
		self.gyro[2]=int(((valueH<<8) | valueL))

	def readTemp(self):
		bus = smbus.SMBus(1)
		valueH=bus.read_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_TEMP_OUT_H)
		valueL=bus.read_byte_data(self.MPU9150A_I2C_ADDR,self.MPUREG_TEMP_OUT_L)
		print hex(valueH)
		print hex(valueL)
		print hex(valueH<<8)
		print int((valueH<<8) | valueL,16)
		t= (valueH<<8) | valueL
		self.temp = (t/340)+36.5

	def readMagnetometer(self):
		bus = smbus.SMBus(1)
		dataReady=bus.read_byte_data(self.MAG_I2C_ADDR,self.MAGREG_ST1)
		if dataReady:
			valueH=bus.read_byte_data(self.MAG_I2C_ADDR,self.MAGREG_HXH)
			valueL=bus.read_byte_data(self.MAG_I2C_ADDR,self.MAGREG_HXL)
			self.mag[0]= int(((valueH<<8) | valueL))

			valueH=bus.read_byte_data(self.MAG_I2C_ADDR,self.MAGREG_HYH)
			valueL=bus.read_byte_data(self.MAG_I2C_ADDR,self.MAGREG_HYL)
			self.mag[1]= int(((valueH<<8) | valueL))

			valueH=bus.read_byte_data(self.MAG_I2C_ADDR,self.MAGREG_HZH)
			valueL=bus.read_byte_data(self.MAG_I2C_ADDR,self.MAGREG_HZL)
			self.mag[2]= int(((valueH<<8) | valueL))
			print self.mag
		else:
			self.mag = [0,0,0]
		bus.write_byte_data(self.MAG_I2C_ADDR,self.MAGREG_CNTL,0X01)



mpu = mpuSensor()
mpu.readGyro()
print mpu.gyro

print mpu.detect()
mpu.readTemp()
print mpu.temp
mpu.readMagnetometer()



#bus = smbus.SMBus(1)
#DEVICE_ADD = 0X69
#bus.write_byte_data(MPU9150A_I2C_ADDR,0X6B,0X80)
#time.sleep(0.01)



