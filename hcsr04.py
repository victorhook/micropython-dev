from machine import Pin
import utime

# D1 (5) echo
# D2 (4) trig

class HCSR04:

    def __init__(self, trig_pin, echo_pin):
        self.trig = Pin(trig_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)

    def distance(self):
        # Send 10 us pulse to start measurement
        self.trig.on()
        utime.sleep_us(10)
        self.trig.off()

        # Wait until pulses are sent
        t_start = utime.ticks_ms()
        while utime.ticks_ms() - t_start < 100 and not self.echo.value():
            # waiting MAX 100 ms, if this occurs, there's an error
            pass

        # Start timer do measure distance!
        timer = utime.ticks_us()
        while utime.ticks_us() - timer < 100000 and self.echo.value():
            # waiting MAX 100 ms, if this occurs, there's an error
            pass
        
        # Transform the time into distance
        duration = utime.ticks_us() - timer
        distance = (duration / 2) / 29.4

        return int(distance)

