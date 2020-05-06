import logging
import sys
import time
import csv
import os

from pyfirmata import Arduino, util
from Adafruit_BNO055 import BNO055


def write_to_register(bno, address, value, id_text):
	bno._config_mode()
	val = bno._read_bytes(address, length=1)
	bno._write_byte(address, value, ack=True)
	bno._operation_mode()
	print('{0}: Address {1} changed from {2:08b} to {3:08b}.'.format(id_text, hex(address), val[0], value))
	time.sleep(0.3)

def create_command(address, length):
	com = bytearray(4)
	com[0] = 0xAA  # Start byte
	com[1] = 0x01  # Read
	com[2] = address & 0xFF
	com[3] = length & 0xFF
	return com

def read_raw_data(bno, command, length=6):
	resp = bno._serial_send(command)
	resp = bytearray(bno._serial.read(length))
	return resp

BNO055_PAGE_ID_ADDR = 0x07
BNO055_OPR_MODE_ADDR = 0x3D               #Page 0
BNO055_ACCEL_DATA_X_LSB_ADDR = 0x08       #Page 0
BNO055_GYRO_DATA_X_LSB_ADDR = 0x14        #Page 0
BNO055_MAG_DATA_X_LSB_ADDR = 0x0E         #Page 0
BNO055_EULER_H_LSB_ADDR = 0x1A            #Page 0
BNO055_QUATERNION_DATA_W_LSB_ADDR = 0x20  #Page 0
BNO055_ACC_CONFIG_ADDR = 0x08             #Page 1
BNO055_GYR_CONFIG_ADDR = 0x0A             #Page 1
BNO055_MAG_CONFIG_ADDR = 0x09             #Page 1

BNO055_MODE_ACCONLY = 0x01
BNO066_MODE_AMG = 0x07

com_acc = create_command(BNO055_ACCEL_DATA_X_LSB_ADDR, 6)
com_gyr = create_command(BNO055_GYRO_DATA_X_LSB_ADDR, 6)
com_mag = create_command(BNO055_MAG_DATA_X_LSB_ADDR, 6)
com_ori = create_command(BNO055_EULER_H_LSB_ADDR, 6)
com_quat = create_command(BNO055_QUATERNION_DATA_W_LSB_ADDR, 8)
com_all_data = create_command(BNO055_ACCEL_DATA_X_LSB_ADDR, 32)


board = Arduino('/dev/ttyACM0')
print('IR Sensor init...')
it = util.Iterator(board)
it.start()
board.analog[0].enable_reporting()

bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
bno.begin()#mode=BNO055_MODE_ACCONLY)

f = open('innovators.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(['time', 'acc raw', '', '', '', '', '', 'mag raw', '', '',  '', '', '', 'gyr raw', '', '', \
		'', '', '', 'orientation fusion', '', '', '', '', '',  'quaternion fusion', '', '', '', '', '', \
		'', '', 'IR on A0', 'IR on A1', 'IR on A2'])

#write_to_register(bno, BNO055_PAGE_ID_ADDR, 0x01, 'Page ID')
#write_to_register(bno, BNO055_ACC_CONFIG, 0b00011101, 'Acc Config')
#write_to_register(bno, BNO055_MAG_CONFIG, 0b00000000, 'Mag Config')
#write_to_register(bno, BNO055_PAGE_ID_ADDR, 0x00, 'Page ID')

calibration = False
while not calibration:
	sys, gyro, accel, mag = bno.get_calibration_status()
	print('Sys_cal={0} Gyro_cal={1} Accel_cal={2} Mag_cal={3}'.format(sys, gyro, accel, mag))
	if sys == 3 & gyro == 3 & accel == 3 & mag == 3:
		os.system('clear')
		print('Writing .csv file...')
		calibration = True

while True:
	# Write data in terminal to verify
	#acc_x, acc_y, acc_z = bno.read_accelerometer()
	#gyr_x, gyr_y, gyr_z = bno.read_gyroscope()
    	# Print everything out.
	#print(time.time(), end='\t')
	#print('Acc_x={0:0.2F} Acc_y={1:0.2F} Acc_z={2:0.2F}\t Gyr_x={3:0.2F} Gyr_y={4:0.2F} Gyr_z={5:0.2F}'.format(acc_x, \
	#	acc_y, acc_z, gyr_x, gyr_y, gyr_z))

	# Read data one by one and write to csv file
	#acc_raw = read_raw_data(bno, com_acc)
	#mag_raw = read_raw_data(bno, com_mag)
	#gyr_raw = read_raw_data(bno, com_gyr)
	#ori = read_raw_data(bno, com_ori)
	#quat = read_raw_data(bno, com_quat, length=8)
	#writer.writerow([time.time(), *acc_raw, *mag_raw, *gyr_raw, *ori, *quat])

	# Read all data at once and write to scv file
	all_data = read_raw_data(bno, com_all_data, length=32)
	writer.writerow([time.time(), *all_data, board.analog[0].read(), board.analog[1].read(), board.analog[2].read()])
