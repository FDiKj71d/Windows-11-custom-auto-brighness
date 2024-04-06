import winrt.windows.devices.sensors as ws
import subprocess
import time
from plyer import notification

def get_brightness():

    try:
        currentBrightness = subprocess.check_output(["powershell", "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness |  Select-Object -Property CurrentBrightness).CurrentBrightness"])
        currentBrightness = int(currentBrightness)
    except Exception as e:
        # usually happens when coming back from a power event, such as sleep or hibernate
        print(time.strftime("%H:%M:%S", time.localtime()), ": Failed to get brighness, sleeping 10 seconds. Exception:\n", e)

        notification.notify(
        title = "Auto-Brightness",
        message = str(time.strftime("%H:%M:%S", time.localtime())) + ": Failed to get current percentage brighness, sleeping 1 minute"
        )

        time.sleep(10)
        currentBrightness = None
    return(currentBrightness)


def set_brightness(percentage):

    percentage=str(percentage)
    subprocess.run(["powershell", "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,",percentage,")"])
    return

def get_ambience_lux(lightSensor):

    try:
        currentReading = lightSensor.get_current_reading()
        lux = round(currentReading.illuminance_in_lux)
        
    except Exception as e:
        # usually happens when coming back from a power event, such as sleep or hibernate
        print(time.strftime("%H:%M:%S", time.localtime()), ": Failed to get brighness, sleeping 10 seconds. Exception:\n", e)
        notification.notify(
        title = "Auto-Brightness",
        message = str(time.strftime("%H:%M:%S", time.localtime())) + ": Failed to get ambience Lux, sleeping 1 minute"
        )
        time.sleep(10)
        lux = None
    return(lux)


def map_lux_to_perc(lux_reading):

    if lux_reading is None:
        return(None)
   
    lux_reading = round(lux_reading)

    # here you customize your own curve. format is:
    # range ( min-lux, max-lux ) : target brighness percentage 
  
    switcher = {
        #range (lux range): target brightness percentage
        range(0, 10): 40,
        range(10, 45): 52,
        range(45, 80): 63,
        range(80, 140): 72,
        range(140, 240): 81,
        range(240, 500): 86,
        range(500, 800): 94
    }

    for key in switcher:
        if type(key) is range and lux_reading in key:
            return(switcher[key])
            
    return(100)   # if sensor reports > 800 lux, return 100% brighness


def is_change_needed(lux,current_p,target_p):

    if None in (lux,current_p):
        return(False,-1)

    if current_p > target_p:
        # may need to step down, get target range +20%
        print("step down? actual/target: ", lux, lux * 1.2)
        updated_target = map_lux_to_perc(lux * 1.2)
    elif current_p < target_p:
        # may need to step up, get target range -15%
        print("step up? actual/target: ", lux, lux * 0.85)
        updated_target = map_lux_to_perc(lux * 0.85)
    else:
        updated_target = target_p
    
    if updated_target == current_p:
        change = False
    else:
        change = True
    
    return(change,updated_target)


###  begin program ###

lightSensor = ws.LightSensor.get_default()

while True:

    measured_lux = get_ambience_lux(lightSensor)
    current_brightness_perc = get_brightness()
    pre_target_brightness_perc = map_lux_to_perc(measured_lux)

    change,target = is_change_needed(measured_lux,current_brightness_perc,pre_target_brightness_perc)

    if change == True:
        set_brightness(target)
        print("Setting new brightness (measured lux/target %): ", measured_lux, target)
    else:
        print("no change needed (measured lux/target %): ", measured_lux, target)

    time.sleep(5)
