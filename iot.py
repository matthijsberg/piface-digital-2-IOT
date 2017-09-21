import pifacedigitalio 
import logging 
import logging.handlers 
from domoticzpython import pythonz
global device
device = []
boardno = bin(0b1111111)

#order <board> <pin> <description> <at rest status> <domotics ID> # starts with 0!
device.append({'board_num': 1, 'pin_num': 0,'description': 'meterkast deur','rest': 1, 'domoticz_id': '325'})
device.append({'board_num': 0, 'pin_num': 2,'description': 'Bewegingsmelder Woonkamer','rest': 0, 'domoticz_id': '328'})
device.append({'board_num': 0, 'pin_num': 3,'description': 'Bewegingsmelder Hal','rest': 0, 'domoticz_id': '329'})

#your cluster information. Ignore username and password if not in use (bogus or empty value will do)
cluster_IP = str ("192.168.1.123")
userName = str ("matthijs")
passWord = str ("master80")

######## NO EDITING BELOW THIS UNLESS  YOU KNOW WHAT YOU'RE DOING #######

#information about logging to syslog
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address = '/dev/log')

formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)

# You need to instantiate a class instance here, also logging in to Domoticz if auth in place
pz = pythonz(cluster_IP, userName, passWord)

def connected0(event):
    noconfig = 0
    boardno = 0
    #print(event) # to print all info from an event, determin pin, etc.
    for i in device:
        if i['pin_num'] == event.pin_num and i['board_num'] == boardno:
            noconfig = 1
            if i['rest'] == 0:
                log.info('Setting on / open / motion state for device %s',i['description'])
                pz.set_on(i['domoticz_id'])
                event.chip.output_pins[event.pin_num].turn_on() # turn on outputs, comment out if you do not want to switch anything with the onboard outputs
            elif i['rest'] == 1:
                log.info('Setting off / closed / no-motion state for device %s',i['description'])
                pz.set_off(i['domoticz_id'])
                event.chip.output_pins[event.pin_num].turn_off()
            else:
                log.error('invalid rest status detected, not 1 or 0')
    if noconfig == 0:
        log.warning('Connected event detected but no action performed, looks like there is no config for board / pin: {}/{} .'.format(boardno, event.pin_num))

def connected1(event):
    noconfig = 0
    boardno = 1
    #print(event) # to print all info from an event, determin pin, etc.
    for i in device:
        if i['pin_num'] == event.pin_num and i['board_num'] == boardno:
            noconfig = 1
            if i['rest'] == 0:
                log.info('Setting on / open / motion state for device %s',i['description'])
                pz.set_on(i['domoticz_id'])
                event.chip.output_pins[event.pin_num].turn_on() # turn on outputs, comment out if you do not want to switch anything with the onboard outputs
            elif i['rest'] == 1:
                log.info('Setting off / closed / no-motion state for device %s',i['description'])
                pz.set_off(i['domoticz_id'])
                event.chip.output_pins[event.pin_num].turn_off()
            else:
                log.error('invalid rest status detected, not 1 or 0')
    if noconfig == 0:
        log.warning('Connected event detected but no action performed, looks like there is no config for board / pin: {}/{} .'.format(boardno, event.pin_num))

def disconnected0(event):
    noconfig = 0
    boardno = 0
    for i in device:
        if i['pin_num'] == event.pin_num and i['board_num'] == boardno:
            noconfig = 1
            if i['rest'] == 1:
                log.info('Setting on / open / motion state for device %s',i['description'])
                pz.set_on(i['domoticz_id'])
                event.chip.output_pins[event.pin_num].turn_on() # turn on outputs, comment out if you do not want to switch anything with the onboard outputs
            elif i['rest'] == 0:
                log.info('Setting off / closed / no-motion state for device %s',i['description'])
                pz.set_off(i['domoticz_id'])
                event.chip.output_pins[event.pin_num].turn_off()
            else:
                log.error('invalid rest status detected, not 1 or 0')
    if noconfig == 0:
        log.warning('Disconnected event detected but no action performed, looks like there is no config for board / pin: {}/{} .'.format(boardno, event.pin_num))

def disconnected1(event):
    noconfig = 0
    boardno = 1
    for i in device:
        if i['pin_num'] == event.pin_num and i['board_num'] == boardno:
            noconfig = 1
            if i['rest'] == 1:
                log.info('Setting on / open / motion state for device %s',i['description'])
                pz.set_on(i['domoticz_id'])
                event.chip.output_pins[event.pin_num].turn_on() # turn on outputs, comment out if you do not want to switch anything with the onboard outputs
            elif i['rest'] == 0:
                log.info('Setting off / closed / no-motion state for device %s',i['description'])
                pz.set_off(i['domoticz_id'])
                event.chip.output_pins[event.pin_num].turn_off()
            else:
                log.error('invalid rest status detected, not 1 or 0')
    if noconfig == 0:
        log.warning('Disconnected event detected but no action performed, looks like there is no config for board / pin: {}/{} .'.format(boardno, event.pin_num))


if __name__ == "__main__":
#    listener.deactivate()
    pifacedigital0 = pifacedigitalio.PiFaceDigital(0)
    pifacedigital1 = pifacedigitalio.PiFaceDigital(1)

    listener0 = pifacedigitalio.InputEventListener(chip=pifacedigital0)
    listener1 = pifacedigitalio.InputEventListener(chip=pifacedigital1)
    for i in range(8):
        listener0.register(i, pifacedigitalio.IODIR_ON, connected0)
        listener1.register(i, pifacedigitalio.IODIR_ON, connected1)
        listener0.register(i, pifacedigitalio.IODIR_OFF, disconnected0)
        listener1.register(i, pifacedigitalio.IODIR_OFF, disconnected1)
    listener0.activate()
    listener1.activate()
