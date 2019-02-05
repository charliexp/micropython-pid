#!/usr/bin/python3

import unittest
import sys
import os

# Set paths
srcImportPath = os.path.dirname(os.path.realpath(__file__)) + "/../src"
sys.path.append(srcImportPath)
mockImportPath = os.path.dirname(os.path.realpath(__file__)) + "/mock"
sys.path.append(mockImportPath)

from PID import PID, PIDParams

class PIDTestCase(unittest.TestCase):

    def setUp(self):
        self.pidParams = PIDParams(input = 70, output = 0, setpoint = 90)
        self.pid = PID(params = self.pidParams, kP = 5.0, kI = 0.25, kD = 1.15)

    def test_default_creation(self):
        self.assertIsNotNone(self.pid.params)
        self.assertFalse(self.pid.inAuto)
        self.assertTrue(self.pid.isRaw)
        self.assertEqual(self.pid.params.input, 70)
        self.assertEqual(self.pid.params.output, 0)
        self.assertEqual(self.pid.params.setpoint, 90)
        self.assertEqual(self.pid.sampleTime, 100)
        self.assertEqual(self.pid.direction, PID.FORWARD)
        self.assertEqual(self.pid.kP, 5.0)
        self.assertEqual(self.pid.kI, 0.025)
        self.assertEqual(self.pid.kD, 0.11499999999999999)
        self.assertIsNotNone(self.pid.lastTime)
        self.assertEqual(self.pid.outputMin, PID.OUTPUT_MIN_DEFAULT)
        self.assertEqual(self.pid.outputMax, PID.OUTPUT_MAX_DEFAULT)
        self.assertEqual(self.pid.iTerm, 0)

    def test_set_mode_from_manual_to_auto(self):
        self.pid.setMode(PID.AUTOMATIC)
        for i in range(0, 30):
            self.assertEqual(self.pid.history[i], 70)
        self.assertEqual(self.pid.iTerm, 0)

    def test_set_mode_from_manual_to_auto_with_output_above_max(self):
        self.pidParams.output = 1024
        self.pid.setMode(PID.AUTOMATIC)
        for i in range(0, 30):
            self.assertEqual(self.pid.history[i], 70)
        self.assertEqual(self.pid.iTerm, self.pid.outputMax)

    def test_set_mode_from_manual_to_auto_with_output_below_min(self):
        self.pidParams.output = -1
        self.pid.setMode(PID.AUTOMATIC)
        for i in range(0, 30):
            self.assertEqual(self.pid.history[i], 70)
        self.assertEqual(self.pid.iTerm, self.pid.outputMin)

    def test_should_switch_direction_from_forward_to_reverse_in_auto(self):
        self.pid.setMode(PID.AUTOMATIC)
        self.pid.setDirection(PID.REVERSE)
        self.assertEqual(self.pid.kP, -5.0)
        self.assertEqual(self.pid.kI, -0.025)
        self.assertEqual(self.pid.kD, -0.11499999999999999)

    def test_set_output_limits_output_greater_than_max_in_auto(self):
        self.pid.setMode(PID.AUTOMATIC)
        self.pidParams.output = 1024
        self.pid.setOutputLimits(0, 100)
        self.assertEqual(self.pid.outputMax, 100)
        self.assertEqual(self.pidParams.output, self.pid.outputMax)

    def test_set_output_limits_output_less_than_min_in_auto(self):
        self.pid.setMode(PID.AUTOMATIC)
        self.pidParams.output = -1
        self.pid.setOutputLimits(1, 1023)
        self.assertEqual(self.pid.outputMin, 1)
        self.assertEqual(self.pidParams.output, self.pid.outputMin)

    def test_set_output_limits_iterm_greater_than_max_in_auto(self):
        self.pid.setMode(PID.AUTOMATIC)
        self.pid.iTerm = 1023
        self.pid.setOutputLimits(0, 100)
        self.assertEqual(self.pid.outputMax, 100)
        self.assertEqual(self.pid.iTerm, self.pid.outputMax)

    def test_set_output_limits_iterm_less_than_min_in_auto(self):
        self.pid.setMode(PID.AUTOMATIC)
        self.pid.iTerm =-1
        self.pid.setOutputLimits(1, 1023)
        self.assertEqual(self.pid.outputMin, 1)
        self.assertEqual(self.pid.iTerm, self.pid.outputMin)

    def test_set_tunings_kp_negative_in_auto(self):
        self.pid.setMode(PID.AUTOMATIC)
        self.pid.setTunings(-1, 1, 2)
        self.assertEqual(self.pid.kP, 5.0)
        self.assertEqual(self.pid.kI, 0.025)
        self.assertEqual(self.pid.kD, 0.11499999999999999)

    def test_set_tunings_ki_negative_in_auto(self):
        self.pid.setMode(PID.AUTOMATIC)
        self.pid.setTunings(0, -1, 2)
        self.assertEqual(self.pid.kP, 5.0)
        self.assertEqual(self.pid.kI, 0.025)
        self.assertEqual(self.pid.kD, 0.11499999999999999)

    def test_set_tunings_ki_negative_in_auto(self):
        self.pid.setMode(PID.AUTOMATIC)
        self.pid.setTunings(0, 1, -2)
        self.assertEqual(self.pid.kP, 5.0)
        self.assertEqual(self.pid.kI, 0.025)
        self.assertEqual(self.pid.kD, 0.11499999999999999)

    def test_setunings_in_auto(self):
        self.pid.setMode(PID.AUTOMATIC)
        self.pid.setTunings(0, 1, 2)
        self.assertEqual(self.pid.kP, 0)
        self.assertEqual(self.pid.kI, 0.1)
        self.assertEqual(self.pid.kD, 0.2)

    def test_setunings_in_auto_reverse(self):
        self.pid.setMode(PID.AUTOMATIC)
        self.pid.setDirection(PID.REVERSE)
        self.pid.setTunings(1, 2, 3)
        self.assertEqual(self.pid.kP, -1)
        self.assertEqual(self.pid.kI, -0.2)
        self.assertEqual(self.pid.kD, -0.30000000000000004)
        
    def test_compute_no_auto(self):
        res = self.pid.compute()
        self.assertFalse(res)
        
if __name__ == '__main__':
    unittest.main()
