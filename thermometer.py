import os
import glob
import time
import subprocess
import lcddriver
import datetime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw( adr ):
    f = open(base_dir+adr+'/w1_slave', 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp_raw_subprocess( adr ):
	catdata = subprocess.Popen(['cat',base_dir+adr+'/w1_slave'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out,err = catdata.communicate()
	out_decode = out.decode('utf-8')
	lines = out_decode.split('\n')
	return lines


def read_temp( adr ):
    lines = read_temp_raw_subprocess( adr )
    if lines[0].strip()[-3:] != 'YES':
        return 999,999
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
	
lcd = lcddriver.lcd()
time.sleep(1)

while True:
	lcd.lcd_display_string("Bastu   "+str(round(read_temp('28-0000043796b1')[0], 1))+"C", 1)
	lcd.lcd_display_string("Ute     "+str(round(read_temp('28-000004374902')[0], 1))+"C", 2)
	lcd.lcd_display_string("Vatten  "+str(round(read_temp('28-0000045d8f34')[0], 1))+"C", 3)
	now = datetime.datetime.now()
#	lcd.lcd_display_string(now.strftime("%Y-%m-%d %H:%M:%S"), 4)
	time.sleep(30)

