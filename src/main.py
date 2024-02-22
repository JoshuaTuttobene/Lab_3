"""!
@file main.py
Initializes a queue, motor, encoder, and controller to perform a closed loop step response
and print data so it can be read via the serial port in a seperate file.

@author Aaron Escamilla, Karen Morales De Leon, Joshua Tuttobene
@date   02/22/2024 Original program, based on example from above listed source
@copyright (c) 2023 by Spluttflob and released under the GNU Public Licenes V3
"""
import motor_driver as MD
import encoder_reader as ER
import CL_Proportional_Control as CLPC
import utime
import cqueue
import pyb
import micropython


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
while True:
    kp = float(input("Enter a Kp value:"))  # input for Kp
    CL = CLPC.ClosedLoop_P(kp,50000) # use small Kp
    encoder.zero()  # zero encoder before using
    init = utime.ticks_ms() # initial time
    for val in range(Queue_Size):    # collect data for length of queue to fill
        pwm = CL.run(encoder.read())  # set return from controller as pwm for motor
        time.put(utime.ticks_ms()-init)   # put time into queue
        pos.put(encoder.read())          # put position into queue
        motor.set_duty_cycle(pwm)     # set new pwm
        utime.sleep_ms(10)    # sleep 10 ms to give delay before next reading

    for Queue_Size in range(250):  # for loop to print and empty queue
        print(f"{time.get()}, {pos.get()}")
        if time.any() == False:
            print("end")     # print end to indicate completion of data
            motor.set_duty_cycle(0) # turn off motor once data has been collected
