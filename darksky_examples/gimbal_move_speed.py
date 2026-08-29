#!/usr/bin/env python3
import sys
import os

# Add the libs directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'libs'))

# Import config first to setup environment automatically
from config import config

import time
import signal
from pymavlink import mavutil
from payload_sdk import PayloadSdkInterface, payload_status_event_t, input_mode_t
from payload_define import *

my_payload = None

# Signal handler for quitting
def quit_handler(sig, frame):
    global my_payload
    print("\nTERMINATING AT USER REQUEST")

    # Close payload interface
    if my_payload:
        try:
            my_payload.sdkQuit()
        except Exception as e:
            print(f"Error while quitting payload: {e}")
    # End program    
    sys.exit(0)

# Callback function for payload status changes
def onPayloadStatusChanged(event, param):
    if payload_status_event_t(event) == payload_status_event_t.PAYLOAD_GB_ATTITUDE:
        # param[0]: pitch
        # param[1]: roll
        # param[2]: yaw
        print(f"Pitch: {param[0]:.2f} - Roll: {param[1]:.2f} - Yaw: {param[2]:.2f}")

def main():
    global my_payload

    print("Starting Set gimbal mode example...\n")
    signal.signal(signal.SIGINT, quit_handler)

    # Create payloadsdk object
    my_payload = PayloadSdkInterface()

    # ==== comment by Darksky =====
    # # Init payload
    # my_payload.sdkInitConnection()
    # print("Waiting for payload signal!\n")

    # # Register callback function
    # my_payload.regPayloadStatusChanged(onPayloadStatusChanged)

    # # Check connection
    # my_payload.checkPayloadConnection()
    # time.sleep(0.1)  
    # ==== end Darksy comment 

    # == add by Darksky, check after ini =============
    if not my_payload.sdkInitConnection():
        print("ERROR: sdkInitConnection() failed")
        return
    print("Waiting for payload signal!\n")

    # my_payload.regPayloadStatusChanged(onPayloadStatusChanged)
    # if not my_payload.checkPayloadConnection():
    #    print("ERROR: checkPayloadConnection() failed")
    #    my_payload.sdkQuit()
    #    return
    # print("Payload connection OK")

    time.sleep(0.5)
    # == end Darksky =================


    # === commented by Darksky 
    # # Set gimbal RC mode to STANDARD 
    # print("Set gimbal RC mode")
    # my_payload.setPayloadCameraParam(PAYLOAD_CAMERA_RC_MODE, payload_camera_rc_mode.PAYLOAD_CAMERA_RC_MODE_STANDARD, mavutil.mavlink.MAV_PARAM_TYPE_UINT32)
    # time.sleep(0.1)  
    # === end of Darksky ==========

    
    print("Move gimbal yaw-pitch to the right-down at speed 8 deg/s for 3 secs")
    start = time.time()
    while time.time()-start <3:
        my_payload.setGimbalSpeed(0, -8, -8, input_mode_t.INPUT_SPEED)
        time.sleep(0.05) 

    
    print("Move gimbal yaw-pitch to the left-up at speed 8 deg/s for 3 secs")
    start = time.time()
    while time.time()-start <3:
        my_payload.setGimbalSpeed(0, 8, 8, input_mode_t.INPUT_SPEED)
        time.sleep(0.05) 

    
    print("Move gimbal pitch down at speed 8 deg/s for 3 secs")
    start = time.time()
    while time.time()-start <3:
        my_payload.setGimbalSpeed(-8, 0, 0, input_mode_t.INPUT_SPEED)
        time.sleep(0.05) 

    
    print("Move gimbal pitch up at speed 8 deg/s for 3 secs")
    start = time.time()
    while time.time()-start <3:
        my_payload.setGimbalSpeed(8, 0, 0, input_mode_t.INPUT_SPEED)
        time.sleep(0.05) 
    
    
    print("Move gimbal roll right at speed 8 deg/s for 3 secs")
    start = time.time()
    while time.time()-start <3:
        my_payload.setGimbalSpeed(0, -8, 0, input_mode_t.INPUT_SPEED)
        time.sleep(0.05) 

    
    print("Move gimbal roll left at speed 8 deg/s for 3 secs")
    start = time.time()
    while time.time()-start <3:
        my_payload.setGimbalSpeed(0, 8, 0, input_mode_t.INPUT_SPEED)
        time.sleep(0.05) 

    # Stop gimbal movement
    print("Keep gimbal stop, delay in 5secs")
    for _ in range(10):
       my_payload.setGimbalSpeed(0, 0, 0, input_mode_t.INPUT_SPEED)
       time.sleep(0.05) 

    # Close payload interface
    try:
        my_payload.sdkQuit()
    except Exception as e:
        print(f"Error while quitting payload: {e}")

if __name__ == "__main__":
    main()