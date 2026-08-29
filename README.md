# DARKSKY PROJECT -- Tracking and Gimbal Control 

this repo is based on https://github.com/Gremsy/PayloadSdk.git. Note that libs/payload_sdk.py is modified. Using original payload_sdk.py will report error. 

## Envrionment setup

### Install required system dependencies
```bash
sudo apt-get install libxml2-dev libxslt-dev
sudo apt-get install python3-dev gobject-introspection libgirepository1.0-dev
sudo apt-get install libcairo2-dev libglib2.0-dev gir1.2-gtk-3.0 libgtkmm-3.0-dev
sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
sudo apt-get install pkg-config meson ninja-build
sudo apt-get install libcurl4-openssl-dev libjsoncpp-dev
```

### Clone the Repository
```bash
git clone https://github.com/mandeezh/darksky.git
```

### Install anaconda 
```
wget https://pro.anaconda.com/miniconda/Miniconda3-py312_26.5.3-2-Linux-aarch64.sh
bash Miniconda3-py312_26.5.3-2-Linux-aarch64.sh 
```

```
cd darksky
conda env create -f environment.yml 
conda activate darksky
```

## Check serial port 

Connect USB-2-TTL cable. It will show up as a ttyUSB* in device. Check it by:
```
ls -l /dev/ttyUSB*
```
The output will be similar to:
```
crw-rw---- 1 root dialout 188, 0 Aug 27 23:15 /dev/ttyUSB0
```

in libs/config.py, find:
```
# UART Configuration
    UART_PORT = "/dev/ttyUSB0"  
    UART_BAUDRATE = 115200
```
make corresponding change if your device is not shown as ttyUSB0.

Only group 'dialout' and root has permission to read and write the serial port. So add user to dialout group.

check if dialout group exists:
```
groups
```
if not,create it:
```
newgrp dialout
```
add user to group
```
sudo usermod -aG dialout $USER
```


## test gimbal connection 

- check port connection and payload connection
```
python examples/check_connect.py 
```
terminal output:
```
INFO] Loading payload definitions for VIO
[INFO] VIO definitions loaded successfully
Starting ConnectPayload example...
Starting Gremsy PayloadSdk 3.0.1_build.12122025
[INFO] Gremsy Payload SDK Configuration
[INFO] SDK Version: 3.0.1_build.12122025
[INFO] Payload Type: VIO
[INFO] Connection: /dev/ttyUSB0:115200
[INFO] System ID: 1
[INFO] Component ID: 193
[INFO] Connecting to /dev/ttyUSB0 at 115200 baud
[INFO] Sending initial HEARTBEATs...
[INFO] Waiting for HEARTBEAT...
[INFO] Sending initial ping
[INFO] Starting receive thread
Waiting for payload signal!
[INFO] Checking payload connection
[INFO] Payload connected!
system is:  1 gimbal is:  154
✅ Connection test completed successfully!
Payload is connected and responding.
[INFO] Connection closed.
Connection closed gracefully.
Check connection example finished.
```

- gimbal yaw right 90 degree then raw left 90 degree 

```
python examples/gimbal_move_angle.py 
```
Terminal output:
```
INFO] Loading payload definitions for VIO
[INFO] VIO definitions loaded successfully
Starting Set gimbal mode example...

Starting Gremsy PayloadSdk 3.0.1_build.12122025
[INFO] Gremsy Payload SDK Configuration
[INFO] SDK Version: 3.0.1_build.12122025
[INFO] Payload Type: VIO
[INFO] Connection: /dev/ttyUSB0:115200
[INFO] System ID: 1
[INFO] Component ID: 193
[INFO] Connecting to /dev/ttyUSB0 at 115200 baud
[INFO] Sending initial HEARTBEATs...
[INFO] Waiting for HEARTBEAT...
[INFO] Sending initial ping
[INFO] Starting receive thread
Waiting for payload signal!

[INFO] Checking payload connection
[INFO] Payload connected!
system is:  1 gimbal is:  154
Set gimbal RC mode
Move gimbal yaw to 90 deg, delay in 5secs
Move gimbal yaw to -90 deg, delay in 5secs
Move gimbal yaw to 0 deg, delay in 5secs
[INFO] Connection closed.
```

- Gimbal yaw to the right 20 deg/s, delay in 5secs. Then gimbal yaw to the left 20 deg/s, delay in 5secs.
```
python examples/gimbal_move_speed.py 
```
Terminal output: 

```
[INFO] Loading payload definitions for VIO
[INFO] VIO definitions loaded successfully
Starting Set gimbal mode example...

Starting Gremsy PayloadSdk 3.0.1_build.12122025
[INFO] Gremsy Payload SDK Configuration
[INFO] SDK Version: 3.0.1_build.12122025
[INFO] Payload Type: VIO
[INFO] Connection: /dev/ttyUSB0:115200
[INFO] System ID: 1
[INFO] Component ID: 193
[INFO] Connecting to /dev/ttyUSB0 at 115200 baud
[INFO] Sending initial HEARTBEATs...
[INFO] Waiting for HEARTBEAT...
[INFO] Sending initial ping
[INFO] Starting receive thread
Waiting for payload signal!

[INFO] Checking payload connection
[INFO] Payload connected!
system is:  1 gimbal is:  154
Pitch: -0.21 - Roll: -0.09 - Yaw: 4.84
Set gimbal RC mode
Pitch: -0.20 - Roll: -0.09 - Yaw: 4.86
Move gimbal yaw to the right 20 deg/s, delay in 5secs
Pitch: -0.20 - Roll: -0.09 - Yaw: 4.82
Pitch: -0.20 - Roll: -0.13 - Yaw: 4.86
...
```

- Customized motion example:

```
python darksky_examples/gimbal_move_speed.py
```
terminal output:
```
Move gimbal yaw-pitch to the right-down at speed 8 deg/s for 3 secs
Move gimbal yaw-pitch to the left-up at speed 8 deg/s for 3 secs
Move gimbal pitch down at speed 8 deg/s for 3 secs
Move gimbal pitch up at speed 8 deg/s for 3 secs
Move gimbal roll down at speed 8 deg/s for 3 secs
Move gimbal roll up at speed 8 deg/s for 3 secs
Keep gimbal stop, delay in 5secs
```
