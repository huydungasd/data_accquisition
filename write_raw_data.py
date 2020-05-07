from utils import *
from pyfirmata import Arduino, util
from Adafruit_BNO055 import BNO055


com_all_data = create_command(BNO055_ACCEL_DATA_X_LSB_ADDR, 32)

board = Arduino('/dev/ttyACM0')
print('IR Sensor init...')
it = util.Iterator(board)
it.start()
board.analog[0].enable_reporting()
board.analog[1].enable_reporting()
board.analog[2].enable_reporting()

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
	# Read all data at once and write to scv file
	all_data = read_raw_data(bno, com_all_data, length=32)
	writer.writerow([time.time(), *all_data, board.analog[0].read(), board.analog[1].read(), board.analog[2].read()])
