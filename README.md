# Windows-11-custom-auto-brighness

A custom script to manually set an auto-brighness curve on Windows 11, based on the input from a 
lux sensor (typically, screen-mounted on laptops).

This is for devices that count with an ambience light sensor and allow to set screen brightness on a percentage based scale.

I run this script as a scheduled task upon boot, always running in background and monitoring for ambience brighness changes every few seconds (similar to how the native Windows 11 mechanism does)

## customize brighness curve
See around line 60. 

##setup (python 3.7 to 3.9 only):
pip install winrt  (to access the brightness sensor)
In Windows, disable "automatic brighness when lighting changes"

for new device, change "map_lux_to_perc". Should be an exponential curve, where example:
10 lux measured ambience should produce ~32 nits screen brighness. 
800 lux measured ambience should produce ~260 nits screen brighness.
now to map brighness to actual percentage values, use spyder colorimeter and get 6-8 readings
of pure white at difference brightness levels. Map those percentages to luminance (Y == cd/m2 == lux)

##References:
https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/sensors-adaptive-brightness

https://download.microsoft.com/download/8/0/6/8061224B-6EDA-4162-A5D4-FA9A779E732F/integrating-ambient-light-sensors-with-windows-10.docx

To monitor lux in various conditions for testing, SensorExplorer from MS comes in handy:
https://apps.microsoft.com/detail/9pgl3xpq1tpx
