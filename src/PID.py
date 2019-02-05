######################################
# PID implementation for micropython #
######################################

import utime

# Wrapper class that allows input, output, and setpoint
# to be passed around and modified
class PIDParams:

    # Constructor
    def __init__(self, input, output, setpoint):
        self.input = input
        self.output = output
        self.setpoint = setpoint
        
    
# Controller
class PID:

    # Constants
    SAMPLE_TIME_DEFAULT = 100
    FORWARD = 0
    REVERSE = 1
    OUTPUT_MIN_DEFAULT = 0 # Micropython PWM min
    OUTPUT_MAX_DEFAULT = 1023  # Micropython PWM max
    MANUAL = 0
    AUTOMATIC = 1
    
    # Constructor
    def __init__(self, params, kP, kI, kD, direction = FORWARD):
        # Set default values
        self.direction = self.FORWARD
        self.kP = 0.0
        self.kI = 0.0
        self.kD = 0.0
        self.inAuto = False
        self.isRaw = True
        self.outputMin = 0
        self.outputMax = 0
        self.iTerm = 0
        self.history = [0] * 30
        
        # Set input values
        self.params = params

        # Set output limits
        self.setOutputLimits(self.OUTPUT_MIN_DEFAULT, self.OUTPUT_MAX_DEFAULT)
        
        # Set sample time
        self.sampleTime = self.SAMPLE_TIME_DEFAULT

        # Set direction
        self.setDirection(direction)
        
        # Set tunings
        self.setTunings(kP, kI, kD)

        # Set last time run
        self.lastTime = utime.ticks_ms() - self.sampleTime
        
        print("Created")
        print("Sample time " + str(self.sampleTime))
        print("Input " + str(self.params.input))
        print("Output " + str(self.params.output))
        print("Setpoint " + str(self.params.setpoint))
        print("kP " + str(self.kP))
        print("kI " + str(self.kI))
        print("kD " + str(self.kD))
        print("Output min " + str(self.outputMin))
        print("Output max " + str(self.outputMax))
        print("iTerm " + str(self.iTerm))
        print("Last time " + str(self.lastTime))

    # Compute
    def compute(self):
        print("\n###############")
        print("Computing")

        # If not auto, return
        if not self.inAuto:
            print("Return not in auto")
            print("###############\n")
            return False

        now = utime.ticks_ms()
        timeChange = now - self.lastTime
        print("Now " + str(now))
        print("Time change " + str(timeChange))
        
        return True

    # Initialize
    def initialize(self):
        print("Initializing")
        self.initializeHistory()
        self.iTerm = self.params.output
        if self.iTerm > self.outputMax:
            self.iTerm = self.outputMax
        elif self.iTerm < self.outputMin:
            self.iTerm = self.outputMin
            
    # Initialize histor
    def initializeHistory(self):
        print("Initializing history")
        self.history[0] = self.params.input
        for i in range(1, 30):
            self.history[i] = self.history[0]
            
    # Set tunings
    def setTunings(self, kP, kI, kD):
        print("Setting tunings")

        if kP < 0 or kI < 0 or kD < 0:
            return

        sampleTimeInSecs = self.sampleTime / 1000

        self.kP = kP
        self.kI = kI * sampleTimeInSecs
        self.kD = kD * sampleTimeInSecs

        if self.direction == self.REVERSE:
            self.kP = 0 - self.kP
            self.kI = 0 - self.kI
            self.kD = 0 - self.kD

    # Set output limits
    def setOutputLimits(self, minLimit, maxLimit):
        self.outputMin = minLimit
        self.outputMax = maxLimit

        if self.inAuto:
            if self.params.output > self.outputMax:
                self.params.output = self.outputMax
            elif self.params.output < self.outputMin:
                self.params.output = self.outputMin
            if self.iTerm > self.outputMax:
                self.iTerm = self.outputMax
            elif self.iTerm < self.outputMin:
                self.iTerm = self.outputMin

    # Set mode
    def setMode(self, mode):
        newAuto = (mode == self.AUTOMATIC)
        if newAuto != self.inAuto:
            print("Changing mode")
            self.initialize()
        self.inAuto = newAuto
        
    # Set direction
    def setDirection(self, direction):
        print("Setting direction")
        if self.inAuto and direction != self.direction:
            self.kP = 0 - self.kP
            self.kI = 0 - self.kI
            self.kD = 0 - self.kD
        self.direction = direction
