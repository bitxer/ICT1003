# ICT1003

## Goal
Create an innovation new application or use case for the tiny circuit

## Details
- This is a team exploration project and not a instructor-led project
- Work within your teams and leverage on the vast amount of materials available on the internet
- You can use modify, hack, remix any open source code you can find out there
- You have to use the tiny-circuit but you can also connect the tiny-circuit to other devices

## Setup
The setup for the different components is as follows

> Note: Setup the sensor and server before the controller

### Server
All server code is contained within the [server](server) folder
1. Install docker and docker-compose
2. Execute the script `deploy.sh` within the [server](server) folder
3. Navigate to `/ui/rooms` of the server to add a room. Do remember to take note of the apikey shown as it will be needed when setting up the controller

### Sensor
All sensor codes are contained within the [sensor](sensor) folder
1. Load the code using Arduino IDE into the tinycircuit

### Controller
All controller codes are contained within the [controller](controller) folder.
> Note: The controller code is developed for Raspberry Pi

1. Run the following lines in the terminal and replace the apikey with the key generated when adding a room in the server
```
$ cd controller
$ sudo ./deploy.sh -f camera -k <apikey> -i
```

## Communication
The data of the sensor and the controller is transmitted using the following format
```
 0                   1           
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       |       |               |
|  VER  |  REV  |   ACTION REF  |
|       |       |               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          MESSAGE ID           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          MESSAGE ID           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

	VER: 4 bits
		Version of the transmission format used
	
	REV: 4 bits
		Revision of the transmission format used
	
	ACTION REF: 8 bits
		0000 0001: Sync
			Used to trigger the syncing of clock with the raspberry
			pi and should only run at start up
		
		0000 0010: Triggered Open
			Used when the sensor detects the door is open
			
		0000 0100: Triggered Close
			Used when the sensor detects the door is close

	MESSAGE ID: 32 bit
		32 bit Message Id
```

## License and Copyright
This project is an assignment submission in partial fulfillment of the module ICT1003 Computer Organisation and Architecture.

As such, copyright and any rights to this project shall belong to the project contributors as well as to Singapore Institute of Technology (SIT)

Plagiarism is a serious offence, and SIT's policy explicitly forbids such acts. Any submission caught with plagiarised work shall receive zero marks for their submission.

Any third-party resources used for this project may be reused in accordance to their license and/or terms and conditions.