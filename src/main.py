import motor_driver as MD
import encoder_reader as ER
import CL_Proportional_Control as CLPC
import utime
import cqueue
import pyb
import micropython

print("please work")
# init queue
Queue_Size = 250
time = cqueue.FloatQueue(Queue_Size)
pos = cqueue.FloatQueue(Queue_Size)

# Motor init
enable_pin = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
in1pin = pyb.Pin.cpu.B4
in2pin = pyb.Pin.cpu.B5
tim3 = pyb.Timer(3, freq=20000)
motor = MD.MotorDriver(enable_pin, in1pin, in2pin, tim3)
motor.enable()

# Encoder init
pin_A = pyb.Pin.cpu.C6
pin_B = pyb.Pin.cpu.C7
tim8 = pyb.Timer(8, prescaler = 0, period = 2**16-1)
encoder = ER.Encoder(pin_A, pin_B, tim8)

# Controller init
kp = float(input("Enter a Kp value:"))
CL = CLPC.ClosedLoop_P(kp,50000) # use small Kp
encoder.zero()
init = utime.ticks_ms()
#print(encoder.read())
for val in range(Queue_Size):
    pwm = CL.run(encoder.read())
    motor.set_duty_cycle(pwm)
    utime.sleep_ms(10)
    time.put(utime.ticks_ms()-init)
    pos.put(encoder.read())
#print(encoder.read())
for Queue_Size in range(250):
    print(f"{time.get()}, {pos.get()}")
    if time.any() == False:
        print("end")
        motor.set_duty_cycle(0)
