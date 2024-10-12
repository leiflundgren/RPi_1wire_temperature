import os
import glob
import time
import subprocess
import lcddriver
import datetime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


base_dir = '/sys/bus/w1/devices'
print base_dir
glob_res = glob.glob(os.path.join(base_dir, '28*'))
print glob_res
device_folder = glob_res[0]
device_file = os.path.join(device_folder, 'w1_slave')
print 'device_file ' + device_file

def read_temp_raw( adr ):
    f = open(base_dir+adr+'/w1_slave', 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp_raw_subprocess( adr ):
        devfile = os.path.join(base_dir, adr, 'w1_slave')
        print 'Readin from ' + devfile
        try:
            with open(devfile, "r") as fil:
                lines = fil.readlines()
                print 'raw data ' + adr
                print lines
                return lines
        except IOError, e:
            print "Read fail", e
            return "read fail"

def read_temp( adr ):
    lines = read_temp_raw_subprocess( adr )
    try:
        if lines[0].strip()[-3:] != 'YES':
            print 'CRC failed'
            return "Vem vet?"
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return str(round(temp_c, 1)) + " C"
        else:
            return "to temp found"
    except:
        return "parse error"

def format_lcd(s):
  return s.ljust(20, ' ')

lcd = lcddriver.lcd()
time.sleep(1)

while True:
        lcd.lcd_display_string(format_lcd("Bastu   " + read_temp('28-0301a279a212')), 1)
        lcd.lcd_display_string(format_lcd("Ute     " + read_temp('28-000004374902')), 2)
        lcd.lcd_display_string(format_lcd("Vatten1 " + read_temp('28-e9d37d1f64ff')), 3)
        lcd.lcd_display_string(format_lcd("Vatten2 " + read_temp('28-f2d77d1f64ff')), 4)
        now = datetime.datetime.now()
#       lcd.lcd_display_string(now.strftime("%Y-%m-%d %H:%M:%S"), 4)
        time.sleep(30)

