EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:newConpass-cache
EELAYER 25 0
EELAYER END
$Descr User 14803 10354
encoding utf-8
Sheet 1 1
Title ""
Date "2016-07-18"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L CONN_02X20 P?
U 1 1 578CDFB4
P 7450 4000
F 0 "P?" H 7450 5050 50  0000 C CNN
F 1 "RASPBERRY PI GPIO CONN" V 7450 4000 50  0000 C CNN
F 2 "" H 7450 3050 50  0000 C CNN
F 3 "" H 7450 3050 50  0000 C CNN
	1    7450 4000
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X04 P?
U 1 1 578D3E96
P 7900 7800
F 0 "P?" H 7900 8050 50  0000 C CNN
F 1 "READER 1" V 8000 7800 50  0000 C CNN
F 2 "" H 7900 7800 50  0000 C CNN
F 3 "" H 7900 7800 50  0000 C CNN
	1    7900 7800
	0    1    1    0   
$EndComp
$Comp
L BC547 Q?
U 1 1 578D3E9C
P 8400 6850
F 0 "Q?" H 8600 6925 50  0000 L CNN
F 1 "BC547" H 8600 6850 50  0000 L CNN
F 2 "TO-92" H 8600 6775 50  0000 L CIN
F 3 "" H 8400 6850 50  0000 L CNN
	1    8400 6850
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578D3EA2
P 8050 7150
F 0 "R?" V 8130 7150 50  0000 C CNN
F 1 "R" V 8050 7150 50  0000 C CNN
F 2 "" V 7980 7150 50  0000 C CNN
F 3 "" H 8050 7150 50  0000 C CNN
	1    8050 7150
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578D3EBA
P 7950 6300
F 0 "R?" V 8030 6300 50  0000 C CNN
F 1 "R" V 7950 6300 50  0000 C CNN
F 2 "" V 7880 6300 50  0000 C CNN
F 3 "" H 7950 6300 50  0000 C CNN
	1    7950 6300
	1    0    0    -1  
$EndComp
$Comp
L Earth #PWR?
U 1 1 578D3ECA
P 8500 8250
F 0 "#PWR?" H 8500 8000 50  0001 C CNN
F 1 "Earth" H 8500 8100 50  0001 C CNN
F 2 "" H 8500 8250 50  0000 C CNN
F 3 "" H 8500 8250 50  0000 C CNN
	1    8500 8250
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X04 P?
U 1 1 578D9CF9
P 8800 7800
F 0 "P?" H 8800 8050 50  0000 C CNN
F 1 "READER 2" V 8900 7800 50  0000 C CNN
F 2 "" H 8800 7800 50  0000 C CNN
F 3 "" H 8800 7800 50  0000 C CNN
	1    8800 7800
	0    1    1    0   
$EndComp
$Comp
L BC547 Q?
U 1 1 578D9CFF
P 9200 6850
F 0 "Q?" H 9400 6925 50  0000 L CNN
F 1 "BC547" H 9400 6850 50  0000 L CNN
F 2 "TO-92" H 9400 6775 50  0000 L CIN
F 3 "" H 9200 6850 50  0000 L CNN
	1    9200 6850
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578D9D05
P 8950 7150
F 0 "R?" V 9030 7150 50  0000 C CNN
F 1 "R" V 8950 7150 50  0000 C CNN
F 2 "" V 8880 7150 50  0000 C CNN
F 3 "" H 8950 7150 50  0000 C CNN
	1    8950 7150
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578D9D15
P 8850 6300
F 0 "R?" V 8930 6300 50  0000 C CNN
F 1 "R" V 8850 6300 50  0000 C CNN
F 2 "" V 8780 6300 50  0000 C CNN
F 3 "" H 8850 6300 50  0000 C CNN
	1    8850 6300
	1    0    0    -1  
$EndComp
$Comp
L BC547 Q?
U 1 1 578D9D23
P 9050 5950
F 0 "Q?" H 9250 6025 50  0000 L CNN
F 1 "BC547" H 9250 5950 50  0000 L CNN
F 2 "TO-92" H 9250 5875 50  0000 L CIN
F 3 "" H 9050 5950 50  0000 L CNN
	1    9050 5950
	1    0    0    -1  
$EndComp
$Comp
L Earth #PWR?
U 1 1 578D9D31
P 9150 6350
F 0 "#PWR?" H 9150 6100 50  0001 C CNN
F 1 "Earth" H 9150 6200 50  0001 C CNN
F 2 "" H 9150 6350 50  0000 C CNN
F 3 "" H 9150 6350 50  0000 C CNN
	1    9150 6350
	1    0    0    -1  
$EndComp
$Comp
L +12V #PWR?
U 1 1 578DDC13
P 7500 7450
F 0 "#PWR?" H 7500 7300 50  0001 C CNN
F 1 "+12V" H 7500 7590 50  0000 C CNN
F 2 "" H 7500 7450 50  0000 C CNN
F 3 "" H 7500 7450 50  0000 C CNN
	1    7500 7450
	1    0    0    -1  
$EndComp
$Comp
L BC547 Q?
U 1 1 578E25AC
P 3350 5950
F 0 "Q?" H 3550 6025 50  0000 L CNN
F 1 "BC547" H 3550 5950 50  0000 L CNN
F 2 "TO-92" H 3550 5875 50  0000 L CIN
F 3 "" H 3350 5950 50  0000 L CNN
	1    3350 5950
	1    0    0    -1  
$EndComp
$Comp
L D D?
U 1 1 578E2977
P 3300 5600
F 0 "D?" H 3300 5700 50  0000 C CNN
F 1 "D" H 3300 5500 50  0000 C CNN
F 2 "" H 3300 5600 50  0000 C CNN
F 3 "" H 3300 5600 50  0000 C CNN
	1    3300 5600
	0    1    1    0   
$EndComp
$Comp
L RELAY_2RT K?
U 1 1 578E2106
P 3850 5200
F 0 "K?" H 3800 5600 50  0000 C CNN
F 1 "RELAY_2RT" H 4000 4700 50  0000 C CNN
F 2 "" H 3850 5200 50  0000 C CNN
F 3 "" H 3850 5200 50  0000 C CNN
	1    3850 5200
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578E4496
P 3000 6150
F 0 "R?" V 3080 6150 50  0000 C CNN
F 1 "R" V 3000 6150 50  0000 C CNN
F 2 "" V 2930 6150 50  0000 C CNN
F 3 "" H 3000 6150 50  0000 C CNN
	1    3000 6150
	1    0    0    -1  
$EndComp
$Comp
L Earth #PWR?
U 1 1 578E4874
P 3450 6250
F 0 "#PWR?" H 3450 6000 50  0001 C CNN
F 1 "Earth" H 3450 6100 50  0001 C CNN
F 2 "" H 3450 6250 50  0000 C CNN
F 3 "" H 3450 6250 50  0000 C CNN
	1    3450 6250
	1    0    0    -1  
$EndComp
$Comp
L LED D?
U 1 1 578E4F17
P 4250 5650
F 0 "D?" H 4250 5750 50  0000 C CNN
F 1 "LED" H 4250 5550 50  0000 C CNN
F 2 "" H 4250 5650 50  0000 C CNN
F 3 "" H 4250 5650 50  0000 C CNN
	1    4250 5650
	0    -1   -1   0   
$EndComp
$Comp
L +12V #PWR?
U 1 1 578E5D82
P 3050 5250
F 0 "#PWR?" H 3050 5100 50  0001 C CNN
F 1 "+12V" H 3050 5390 50  0000 C CNN
F 2 "" H 3050 5250 50  0000 C CNN
F 3 "" H 3050 5250 50  0000 C CNN
	1    3050 5250
	1    0    0    -1  
$EndComp
$Comp
L BC547 Q?
U 1 1 578E6B20
P 3000 4200
F 0 "Q?" H 3200 4275 50  0000 L CNN
F 1 "BC547" H 3200 4200 50  0000 L CNN
F 2 "TO-92" H 3200 4125 50  0000 L CIN
F 3 "" H 3000 4200 50  0000 L CNN
	1    3000 4200
	1    0    0    -1  
$EndComp
$Comp
L D D?
U 1 1 578E6B26
P 2950 3850
F 0 "D?" H 2950 3950 50  0000 C CNN
F 1 "D" H 2950 3750 50  0000 C CNN
F 2 "" H 2950 3850 50  0000 C CNN
F 3 "" H 2950 3850 50  0000 C CNN
	1    2950 3850
	0    1    1    0   
$EndComp
$Comp
L RELAY_2RT K?
U 1 1 578E6B2C
P 3500 3450
F 0 "K?" H 3450 3850 50  0000 C CNN
F 1 "RELAY_2RT" H 3650 2950 50  0000 C CNN
F 2 "" H 3500 3450 50  0000 C CNN
F 3 "" H 3500 3450 50  0000 C CNN
	1    3500 3450
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578E6B32
P 2700 4400
F 0 "R?" V 2780 4400 50  0000 C CNN
F 1 "R" V 2700 4400 50  0000 C CNN
F 2 "" V 2630 4400 50  0000 C CNN
F 3 "" H 2700 4400 50  0000 C CNN
	1    2700 4400
	1    0    0    -1  
$EndComp
$Comp
L Earth #PWR?
U 1 1 578E6B38
P 3100 4500
F 0 "#PWR?" H 3100 4250 50  0001 C CNN
F 1 "Earth" H 3100 4350 50  0001 C CNN
F 2 "" H 3100 4500 50  0000 C CNN
F 3 "" H 3100 4500 50  0000 C CNN
	1    3100 4500
	1    0    0    -1  
$EndComp
$Comp
L LED D?
U 1 1 578E6B3E
P 3900 3900
F 0 "D?" H 3900 4000 50  0000 C CNN
F 1 "LED" H 3900 3800 50  0000 C CNN
F 2 "" H 3900 3900 50  0000 C CNN
F 3 "" H 3900 3900 50  0000 C CNN
	1    3900 3900
	0    -1   -1   0   
$EndComp
$Comp
L +12V #PWR?
U 1 1 578E6B51
P 2750 3500
F 0 "#PWR?" H 2750 3350 50  0001 C CNN
F 1 "+12V" H 2750 3640 50  0000 C CNN
F 2 "" H 2750 3500 50  0000 C CNN
F 3 "" H 2750 3500 50  0000 C CNN
	1    2750 3500
	1    0    0    -1  
$EndComp
$Comp
L BC547 Q?
U 1 1 578E9801
P 3400 2350
F 0 "Q?" H 3600 2425 50  0000 L CNN
F 1 "BC547" H 3600 2350 50  0000 L CNN
F 2 "TO-92" H 3600 2275 50  0000 L CIN
F 3 "" H 3400 2350 50  0000 L CNN
	1    3400 2350
	1    0    0    -1  
$EndComp
$Comp
L D D?
U 1 1 578E9807
P 3350 2000
F 0 "D?" H 3350 2100 50  0000 C CNN
F 1 "D" H 3350 1900 50  0000 C CNN
F 2 "" H 3350 2000 50  0000 C CNN
F 3 "" H 3350 2000 50  0000 C CNN
	1    3350 2000
	0    1    1    0   
$EndComp
$Comp
L RELAY_2RT K?
U 1 1 578E980D
P 3900 1600
F 0 "K?" H 3850 2000 50  0000 C CNN
F 1 "RELAY_2RT" H 4050 1100 50  0000 C CNN
F 2 "" H 3900 1600 50  0000 C CNN
F 3 "" H 3900 1600 50  0000 C CNN
	1    3900 1600
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578E9813
P 3050 2550
F 0 "R?" V 3130 2550 50  0000 C CNN
F 1 "R" V 3050 2550 50  0000 C CNN
F 2 "" V 2980 2550 50  0000 C CNN
F 3 "" H 3050 2550 50  0000 C CNN
	1    3050 2550
	1    0    0    -1  
$EndComp
$Comp
L Earth #PWR?
U 1 1 578E9819
P 3500 2650
F 0 "#PWR?" H 3500 2400 50  0001 C CNN
F 1 "Earth" H 3500 2500 50  0001 C CNN
F 2 "" H 3500 2650 50  0000 C CNN
F 3 "" H 3500 2650 50  0000 C CNN
	1    3500 2650
	1    0    0    -1  
$EndComp
$Comp
L LED D?
U 1 1 578E981F
P 4300 2050
F 0 "D?" H 4300 2150 50  0000 C CNN
F 1 "LED" H 4300 1950 50  0000 C CNN
F 2 "" H 4300 2050 50  0000 C CNN
F 3 "" H 4300 2050 50  0000 C CNN
	1    4300 2050
	0    -1   -1   0   
$EndComp
$Comp
L +12V #PWR?
U 1 1 578E9834
P 3100 1650
F 0 "#PWR?" H 3100 1500 50  0001 C CNN
F 1 "+12V" H 3100 1790 50  0000 C CNN
F 2 "" H 3100 1650 50  0000 C CNN
F 3 "" H 3100 1650 50  0000 C CNN
	1    3100 1650
	1    0    0    -1  
$EndComp
$Comp
L BC547 Q?
U 1 1 578EBB5B
P 5050 2650
F 0 "Q?" H 5250 2725 50  0000 L CNN
F 1 "BC547" H 5250 2650 50  0000 L CNN
F 2 "TO-92" H 5250 2575 50  0000 L CIN
F 3 "" H 5050 2650 50  0000 L CNN
	1    5050 2650
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578EBB61
P 4700 2850
F 0 "R?" V 4780 2850 50  0000 C CNN
F 1 "R" V 4700 2850 50  0000 C CNN
F 2 "" V 4630 2850 50  0000 C CNN
F 3 "" H 4700 2850 50  0000 C CNN
	1    4700 2850
	1    0    0    -1  
$EndComp
$Comp
L Earth #PWR?
U 1 1 578EBB67
P 5150 2950
F 0 "#PWR?" H 5150 2700 50  0001 C CNN
F 1 "Earth" H 5150 2800 50  0001 C CNN
F 2 "" H 5150 2950 50  0000 C CNN
F 3 "" H 5150 2950 50  0000 C CNN
	1    5150 2950
	1    0    0    -1  
$EndComp
$Comp
L BC547 Q?
U 1 1 578EC9D6
P 5800 2650
F 0 "Q?" H 6000 2725 50  0000 L CNN
F 1 "BC547" H 6000 2650 50  0000 L CNN
F 2 "TO-92" H 6000 2575 50  0000 L CIN
F 3 "" H 5800 2650 50  0000 L CNN
	1    5800 2650
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578EC9DC
P 5450 2850
F 0 "R?" V 5530 2850 50  0000 C CNN
F 1 "R" V 5450 2850 50  0000 C CNN
F 2 "" V 5380 2850 50  0000 C CNN
F 3 "" H 5450 2850 50  0000 C CNN
	1    5450 2850
	1    0    0    -1  
$EndComp
$Comp
L Earth #PWR?
U 1 1 578EC9E2
P 5900 2950
F 0 "#PWR?" H 5900 2700 50  0001 C CNN
F 1 "Earth" H 5900 2800 50  0001 C CNN
F 2 "" H 5900 2950 50  0000 C CNN
F 3 "" H 5900 2950 50  0000 C CNN
	1    5900 2950
	1    0    0    -1  
$EndComp
$Comp
L BC547 Q?
U 1 1 578ECB29
P 6500 2650
F 0 "Q?" H 6700 2725 50  0000 L CNN
F 1 "BC547" H 6700 2650 50  0000 L CNN
F 2 "TO-92" H 6700 2575 50  0000 L CIN
F 3 "" H 6500 2650 50  0000 L CNN
	1    6500 2650
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578ECB2F
P 6150 2850
F 0 "R?" V 6230 2850 50  0000 C CNN
F 1 "R" V 6150 2850 50  0000 C CNN
F 2 "" V 6080 2850 50  0000 C CNN
F 3 "" H 6150 2850 50  0000 C CNN
	1    6150 2850
	1    0    0    -1  
$EndComp
$Comp
L Earth #PWR?
U 1 1 578ECB35
P 6600 2950
F 0 "#PWR?" H 6600 2700 50  0001 C CNN
F 1 "Earth" H 6600 2800 50  0001 C CNN
F 2 "" H 6600 2950 50  0000 C CNN
F 3 "" H 6600 2950 50  0000 C CNN
	1    6600 2950
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR?
U 1 1 578ED1D0
P 5150 1850
F 0 "#PWR?" H 5150 1700 50  0001 C CNN
F 1 "+5V" H 5150 1990 50  0000 C CNN
F 2 "" H 5150 1850 50  0000 C CNN
F 3 "" H 5150 1850 50  0000 C CNN
	1    5150 1850
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 57908716
P 3900 2600
F 0 "R?" V 3980 2600 50  0000 C CNN
F 1 "R" V 3900 2600 50  0000 C CNN
F 2 "" V 3830 2600 50  0000 C CNN
F 3 "" H 3900 2600 50  0000 C CNN
	1    3900 2600
	0    1    1    0   
$EndComp
$Comp
L R R?
U 1 1 579091A9
P 3500 4450
F 0 "R?" V 3580 4450 50  0000 C CNN
F 1 "R" V 3500 4450 50  0000 C CNN
F 2 "" V 3430 4450 50  0000 C CNN
F 3 "" H 3500 4450 50  0000 C CNN
	1    3500 4450
	0    1    1    0   
$EndComp
$Comp
L R R?
U 1 1 579096D9
P 3850 6200
F 0 "R?" V 3930 6200 50  0000 C CNN
F 1 "R" V 3850 6200 50  0000 C CNN
F 2 "" V 3780 6200 50  0000 C CNN
F 3 "" H 3850 6200 50  0000 C CNN
	1    3850 6200
	0    1    1    0   
$EndComp
$Comp
L CONN_01X02 P?
U 1 1 5790A5F1
P 5350 2250
F 0 "P?" H 5350 2400 50  0000 C CNN
F 1 "BUZZ 1" V 5450 2250 50  0000 C CNN
F 2 "" H 5350 2250 50  0000 C CNN
F 3 "" H 5350 2250 50  0000 C CNN
	1    5350 2250
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X02 P?
U 1 1 5790ADDB
P 6100 2250
F 0 "P?" H 6100 2400 50  0000 C CNN
F 1 "BUZZ 2" V 6200 2250 50  0000 C CNN
F 2 "" H 6100 2250 50  0000 C CNN
F 3 "" H 6100 2250 50  0000 C CNN
	1    6100 2250
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X02 P?
U 1 1 5790B410
P 6800 2250
F 0 "P?" H 6800 2400 50  0000 C CNN
F 1 "BUZZ 3" V 6900 2250 50  0000 C CNN
F 2 "" H 6800 2250 50  0000 C CNN
F 3 "" H 6800 2250 50  0000 C CNN
	1    6800 2250
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X03 P?
U 1 1 5790B886
P 4250 3200
F 0 "P?" H 4250 3400 50  0000 C CNN
F 1 "RELAY 2" V 4350 3200 50  0000 C CNN
F 2 "" H 4250 3200 50  0000 C CNN
F 3 "" H 4250 3200 50  0000 C CNN
	1    4250 3200
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X03 P?
U 1 1 5790CACC
P 4550 4950
F 0 "P?" H 4550 5150 50  0000 C CNN
F 1 "RELAY 1" V 4650 4950 50  0000 C CNN
F 2 "" H 4550 4950 50  0000 C CNN
F 3 "" H 4550 4950 50  0000 C CNN
	1    4550 4950
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X03 P?
U 1 1 5790D25E
P 4600 1350
F 0 "P?" H 4600 1550 50  0000 C CNN
F 1 "RELAY 3" V 4700 1350 50  0000 C CNN
F 2 "" H 4600 1350 50  0000 C CNN
F 3 "" H 4600 1350 50  0000 C CNN
	1    4600 1350
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X06 P?
U 1 1 5790E024
P 1800 7200
F 0 "P?" H 1800 7550 50  0000 C CNN
F 1 "STATE CONN" V 1900 7200 50  0000 C CNN
F 2 "" H 1800 7200 50  0000 C CNN
F 3 "" H 1800 7200 50  0000 C CNN
	1    1800 7200
	-1   0    0    1   
$EndComp
$Comp
L CONN_01X06 P?
U 1 1 5790E3ED
P 1800 8050
F 0 "P?" H 1800 8400 50  0000 C CNN
F 1 "BUTTON CONN" V 1900 8050 50  0000 C CNN
F 2 "" H 1800 8050 50  0000 C CNN
F 3 "" H 1800 8050 50  0000 C CNN
	1    1800 8050
	-1   0    0    1   
$EndComp
$Comp
L R R?
U 1 1 578E800C
P 8500 6300
F 0 "R?" V 8580 6300 50  0000 C CNN
F 1 "R" V 8500 6300 50  0000 C CNN
F 2 "" V 8430 6300 50  0000 C CNN
F 3 "" H 8500 6300 50  0000 C CNN
	1    8500 6300
	1    0    0    -1  
$EndComp
$Comp
L BC547 Q?
U 1 1 578D741F
P 8200 5950
F 0 "Q?" H 8400 6025 50  0000 L CNN
F 1 "BC547" H 8400 5950 50  0000 L CNN
F 2 "TO-92" H 8400 5875 50  0000 L CIN
F 3 "" H 8200 5950 50  0000 L CNN
	1    8200 5950
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578E998A
P 8300 5500
F 0 "R?" V 8380 5500 50  0000 C CNN
F 1 "R" V 8300 5500 50  0000 C CNN
F 2 "" V 8230 5500 50  0000 C CNN
F 3 "" H 8300 5500 50  0000 C CNN
	1    8300 5500
	1    0    0    -1  
$EndComp
$Comp
L Earth #PWR?
U 1 1 578EBCBD
P 8300 6500
F 0 "#PWR?" H 8300 6250 50  0001 C CNN
F 1 "Earth" H 8300 6350 50  0001 C CNN
F 2 "" H 8300 6500 50  0000 C CNN
F 3 "" H 8300 6500 50  0000 C CNN
	1    8300 6500
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578EEBAB
P 9150 5500
F 0 "R?" V 9230 5500 50  0000 C CNN
F 1 "R" V 9150 5500 50  0000 C CNN
F 2 "" V 9080 5500 50  0000 C CNN
F 3 "" H 9150 5500 50  0000 C CNN
	1    9150 5500
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578EF209
P 9300 6300
F 0 "R?" V 9380 6300 50  0000 C CNN
F 1 "R" V 9300 6300 50  0000 C CNN
F 2 "" V 9230 6300 50  0000 C CNN
F 3 "" H 9300 6300 50  0000 C CNN
	1    9300 6300
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X04 P?
U 1 1 578F2DF7
P 9800 7800
F 0 "P?" H 9800 8050 50  0000 C CNN
F 1 "READER 1" V 9900 7800 50  0000 C CNN
F 2 "" H 9800 7800 50  0000 C CNN
F 3 "" H 9800 7800 50  0000 C CNN
	1    9800 7800
	0    1    1    0   
$EndComp
$Comp
L BC547 Q?
U 1 1 578F2DFD
P 10300 6850
F 0 "Q?" H 10500 6925 50  0000 L CNN
F 1 "BC547" H 10500 6850 50  0000 L CNN
F 2 "TO-92" H 10500 6775 50  0000 L CIN
F 3 "" H 10300 6850 50  0000 L CNN
	1    10300 6850
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578F2E03
P 9950 7150
F 0 "R?" V 10030 7150 50  0000 C CNN
F 1 "R" V 9950 7150 50  0000 C CNN
F 2 "" V 9880 7150 50  0000 C CNN
F 3 "" H 9950 7150 50  0000 C CNN
	1    9950 7150
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578F2E09
P 9850 6300
F 0 "R?" V 9930 6300 50  0000 C CNN
F 1 "R" V 9850 6300 50  0000 C CNN
F 2 "" V 9780 6300 50  0000 C CNN
F 3 "" H 9850 6300 50  0000 C CNN
	1    9850 6300
	1    0    0    -1  
$EndComp
$Comp
L Earth #PWR?
U 1 1 578F2E0F
P 10400 8250
F 0 "#PWR?" H 10400 8000 50  0001 C CNN
F 1 "Earth" H 10400 8100 50  0001 C CNN
F 2 "" H 10400 8250 50  0000 C CNN
F 3 "" H 10400 8250 50  0000 C CNN
	1    10400 8250
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X04 P?
U 1 1 578F2E15
P 10700 7800
F 0 "P?" H 10700 8050 50  0000 C CNN
F 1 "READER 2" V 10800 7800 50  0000 C CNN
F 2 "" H 10700 7800 50  0000 C CNN
F 3 "" H 10700 7800 50  0000 C CNN
	1    10700 7800
	0    1    1    0   
$EndComp
$Comp
L BC547 Q?
U 1 1 578F2E1B
P 11100 6850
F 0 "Q?" H 11300 6925 50  0000 L CNN
F 1 "BC547" H 11300 6850 50  0000 L CNN
F 2 "TO-92" H 11300 6775 50  0000 L CIN
F 3 "" H 11100 6850 50  0000 L CNN
	1    11100 6850
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578F2E21
P 10850 7150
F 0 "R?" V 10930 7150 50  0000 C CNN
F 1 "R" V 10850 7150 50  0000 C CNN
F 2 "" V 10780 7150 50  0000 C CNN
F 3 "" H 10850 7150 50  0000 C CNN
	1    10850 7150
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578F2E27
P 10750 6300
F 0 "R?" V 10830 6300 50  0000 C CNN
F 1 "R" V 10750 6300 50  0000 C CNN
F 2 "" V 10680 6300 50  0000 C CNN
F 3 "" H 10750 6300 50  0000 C CNN
	1    10750 6300
	1    0    0    -1  
$EndComp
$Comp
L BC547 Q?
U 1 1 578F2E2D
P 10950 5950
F 0 "Q?" H 11150 6025 50  0000 L CNN
F 1 "BC547" H 11150 5950 50  0000 L CNN
F 2 "TO-92" H 11150 5875 50  0000 L CIN
F 3 "" H 10950 5950 50  0000 L CNN
	1    10950 5950
	1    0    0    -1  
$EndComp
$Comp
L Earth #PWR?
U 1 1 578F2E33
P 11050 6350
F 0 "#PWR?" H 11050 6100 50  0001 C CNN
F 1 "Earth" H 11050 6200 50  0001 C CNN
F 2 "" H 11050 6350 50  0000 C CNN
F 3 "" H 11050 6350 50  0000 C CNN
	1    11050 6350
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578F2E49
P 10400 6300
F 0 "R?" V 10480 6300 50  0000 C CNN
F 1 "R" V 10400 6300 50  0000 C CNN
F 2 "" V 10330 6300 50  0000 C CNN
F 3 "" H 10400 6300 50  0000 C CNN
	1    10400 6300
	1    0    0    -1  
$EndComp
$Comp
L BC547 Q?
U 1 1 578F2E54
P 10100 5950
F 0 "Q?" H 10300 6025 50  0000 L CNN
F 1 "BC547" H 10300 5950 50  0000 L CNN
F 2 "TO-92" H 10300 5875 50  0000 L CIN
F 3 "" H 10100 5950 50  0000 L CNN
	1    10100 5950
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578F2E5B
P 10200 5500
F 0 "R?" V 10280 5500 50  0000 C CNN
F 1 "R" V 10200 5500 50  0000 C CNN
F 2 "" V 10130 5500 50  0000 C CNN
F 3 "" H 10200 5500 50  0000 C CNN
	1    10200 5500
	1    0    0    -1  
$EndComp
$Comp
L Earth #PWR?
U 1 1 578F2E67
P 10200 6500
F 0 "#PWR?" H 10200 6250 50  0001 C CNN
F 1 "Earth" H 10200 6350 50  0001 C CNN
F 2 "" H 10200 6500 50  0000 C CNN
F 3 "" H 10200 6500 50  0000 C CNN
	1    10200 6500
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578F2E6E
P 11050 5500
F 0 "R?" V 11130 5500 50  0000 C CNN
F 1 "R" V 11050 5500 50  0000 C CNN
F 2 "" V 10980 5500 50  0000 C CNN
F 3 "" H 11050 5500 50  0000 C CNN
	1    11050 5500
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578F2E7A
P 11200 6300
F 0 "R?" V 11280 6300 50  0000 C CNN
F 1 "R" V 11200 6300 50  0000 C CNN
F 2 "" V 11130 6300 50  0000 C CNN
F 3 "" H 11200 6300 50  0000 C CNN
	1    11200 6300
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X04 P?
U 1 1 578F33F0
P 11700 7800
F 0 "P?" H 11700 8050 50  0000 C CNN
F 1 "READER 1" V 11800 7800 50  0000 C CNN
F 2 "" H 11700 7800 50  0000 C CNN
F 3 "" H 11700 7800 50  0000 C CNN
	1    11700 7800
	0    1    1    0   
$EndComp
$Comp
L BC547 Q?
U 1 1 578F33F6
P 12200 6850
F 0 "Q?" H 12400 6925 50  0000 L CNN
F 1 "BC547" H 12400 6850 50  0000 L CNN
F 2 "TO-92" H 12400 6775 50  0000 L CIN
F 3 "" H 12200 6850 50  0000 L CNN
	1    12200 6850
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578F33FC
P 11850 7150
F 0 "R?" V 11930 7150 50  0000 C CNN
F 1 "R" V 11850 7150 50  0000 C CNN
F 2 "" V 11780 7150 50  0000 C CNN
F 3 "" H 11850 7150 50  0000 C CNN
	1    11850 7150
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578F3402
P 11750 6300
F 0 "R?" V 11830 6300 50  0000 C CNN
F 1 "R" V 11750 6300 50  0000 C CNN
F 2 "" V 11680 6300 50  0000 C CNN
F 3 "" H 11750 6300 50  0000 C CNN
	1    11750 6300
	1    0    0    -1  
$EndComp
$Comp
L Earth #PWR?
U 1 1 578F3408
P 12300 8250
F 0 "#PWR?" H 12300 8000 50  0001 C CNN
F 1 "Earth" H 12300 8100 50  0001 C CNN
F 2 "" H 12300 8250 50  0000 C CNN
F 3 "" H 12300 8250 50  0000 C CNN
	1    12300 8250
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X04 P?
U 1 1 578F340E
P 12600 7800
F 0 "P?" H 12600 8050 50  0000 C CNN
F 1 "READER 2" V 12700 7800 50  0000 C CNN
F 2 "" H 12600 7800 50  0000 C CNN
F 3 "" H 12600 7800 50  0000 C CNN
	1    12600 7800
	0    1    1    0   
$EndComp
$Comp
L BC547 Q?
U 1 1 578F3414
P 13000 6850
F 0 "Q?" H 13200 6925 50  0000 L CNN
F 1 "BC547" H 13200 6850 50  0000 L CNN
F 2 "TO-92" H 13200 6775 50  0000 L CIN
F 3 "" H 13000 6850 50  0000 L CNN
	1    13000 6850
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578F341A
P 12750 7150
F 0 "R?" V 12830 7150 50  0000 C CNN
F 1 "R" V 12750 7150 50  0000 C CNN
F 2 "" V 12680 7150 50  0000 C CNN
F 3 "" H 12750 7150 50  0000 C CNN
	1    12750 7150
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578F3420
P 12650 6300
F 0 "R?" V 12730 6300 50  0000 C CNN
F 1 "R" V 12650 6300 50  0000 C CNN
F 2 "" V 12580 6300 50  0000 C CNN
F 3 "" H 12650 6300 50  0000 C CNN
	1    12650 6300
	1    0    0    -1  
$EndComp
$Comp
L BC547 Q?
U 1 1 578F3426
P 12850 5950
F 0 "Q?" H 13050 6025 50  0000 L CNN
F 1 "BC547" H 13050 5950 50  0000 L CNN
F 2 "TO-92" H 13050 5875 50  0000 L CIN
F 3 "" H 12850 5950 50  0000 L CNN
	1    12850 5950
	1    0    0    -1  
$EndComp
$Comp
L Earth #PWR?
U 1 1 578F342C
P 12950 6350
F 0 "#PWR?" H 12950 6100 50  0001 C CNN
F 1 "Earth" H 12950 6200 50  0001 C CNN
F 2 "" H 12950 6350 50  0000 C CNN
F 3 "" H 12950 6350 50  0000 C CNN
	1    12950 6350
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578F3442
P 12300 6300
F 0 "R?" V 12380 6300 50  0000 C CNN
F 1 "R" V 12300 6300 50  0000 C CNN
F 2 "" V 12230 6300 50  0000 C CNN
F 3 "" H 12300 6300 50  0000 C CNN
	1    12300 6300
	1    0    0    -1  
$EndComp
$Comp
L BC547 Q?
U 1 1 578F344D
P 12000 5950
F 0 "Q?" H 12200 6025 50  0000 L CNN
F 1 "BC547" H 12200 5950 50  0000 L CNN
F 2 "TO-92" H 12200 5875 50  0000 L CIN
F 3 "" H 12000 5950 50  0000 L CNN
	1    12000 5950
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578F3454
P 12100 5500
F 0 "R?" V 12180 5500 50  0000 C CNN
F 1 "R" V 12100 5500 50  0000 C CNN
F 2 "" V 12030 5500 50  0000 C CNN
F 3 "" H 12100 5500 50  0000 C CNN
	1    12100 5500
	1    0    0    -1  
$EndComp
$Comp
L Earth #PWR?
U 1 1 578F3460
P 12100 6500
F 0 "#PWR?" H 12100 6250 50  0001 C CNN
F 1 "Earth" H 12100 6350 50  0001 C CNN
F 2 "" H 12100 6500 50  0000 C CNN
F 3 "" H 12100 6500 50  0000 C CNN
	1    12100 6500
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578F3467
P 12950 5500
F 0 "R?" V 13030 5500 50  0000 C CNN
F 1 "R" V 12950 5500 50  0000 C CNN
F 2 "" V 12880 5500 50  0000 C CNN
F 3 "" H 12950 5500 50  0000 C CNN
	1    12950 5500
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 578F3473
P 13100 6300
F 0 "R?" V 13180 6300 50  0000 C CNN
F 1 "R" V 13100 6300 50  0000 C CNN
F 2 "" V 13030 6300 50  0000 C CNN
F 3 "" H 13100 6300 50  0000 C CNN
	1    13100 6300
	1    0    0    -1  
$EndComp
Connection ~ 7200 2800
Wire Wire Line
	7200 2800 13100 2800
Wire Wire Line
	5150 1850 5150 2200
Connection ~ 5900 2000
Wire Wire Line
	6600 2000 6600 2200
Connection ~ 5150 2000
Wire Wire Line
	5900 2000 5900 2200
Wire Wire Line
	5150 2000 6600 2000
Wire Wire Line
	6150 3250 7200 3250
Wire Wire Line
	5450 3550 7200 3550
Connection ~ 6600 2900
Wire Wire Line
	6600 2850 6600 2950
Wire Wire Line
	6150 3000 6150 3250
Wire Wire Line
	6150 2650 6150 2700
Wire Wire Line
	6300 2650 6150 2650
Connection ~ 5900 2900
Wire Wire Line
	5900 2850 5900 2950
Wire Wire Line
	5450 3000 5450 3550
Wire Wire Line
	5450 2650 5450 2700
Wire Wire Line
	5600 2650 5450 2650
Wire Wire Line
	5150 2300 5150 2450
Wire Wire Line
	4700 3650 7200 3650
Connection ~ 5150 2900
Wire Wire Line
	5150 2850 5150 2950
Wire Wire Line
	4700 3000 4700 3650
Wire Wire Line
	4700 2650 4700 2700
Wire Wire Line
	4850 2650 4700 2650
Wire Wire Line
	4550 3750 7200 3750
Wire Wire Line
	4550 2850 4550 3750
Wire Wire Line
	3050 2850 4550 2850
Connection ~ 3350 1650
Connection ~ 3500 2600
Wire Wire Line
	4300 2600 4300 2250
Wire Wire Line
	3100 1650 3500 1650
Wire Wire Line
	3350 1850 3350 1650
Wire Wire Line
	4300 1750 4300 1850
Wire Wire Line
	3500 2550 3500 2650
Wire Wire Line
	3050 2700 3050 2850
Wire Wire Line
	3050 2350 3050 2400
Wire Wire Line
	3200 2350 3050 2350
Wire Wire Line
	3500 1850 3350 1850
Wire Wire Line
	3350 2150 3500 2150
Wire Wire Line
	3500 2150 3500 1950
Wire Wire Line
	6050 3950 7200 3950
Wire Wire Line
	6050 4700 6050 3950
Wire Wire Line
	2700 4700 6050 4700
Connection ~ 2950 3500
Connection ~ 3100 4450
Wire Wire Line
	3900 4450 3900 4100
Wire Wire Line
	2750 3500 3100 3500
Wire Wire Line
	2950 3700 2950 3500
Wire Wire Line
	3900 3600 3900 3700
Wire Wire Line
	3100 4400 3100 4500
Wire Wire Line
	2700 4550 2700 4700
Wire Wire Line
	2700 4200 2700 4250
Wire Wire Line
	2800 4200 2700 4200
Wire Wire Line
	3100 3700 2950 3700
Wire Wire Line
	2950 4000 3100 4000
Wire Wire Line
	3100 4000 3100 3800
Connection ~ 3300 5250
Connection ~ 3450 6200
Wire Wire Line
	4250 6200 4250 5850
Wire Wire Line
	3050 5250 3450 5250
Wire Wire Line
	3300 5450 3300 5250
Wire Wire Line
	4250 5350 4250 5450
Wire Wire Line
	3450 6150 3450 6250
Wire Wire Line
	6150 4050 7200 4050
Wire Wire Line
	6150 6450 6150 4050
Wire Wire Line
	3000 6450 6150 6450
Wire Wire Line
	3000 6300 3000 6450
Wire Wire Line
	3000 5950 3000 6000
Wire Wire Line
	3150 5950 3000 5950
Wire Wire Line
	3450 5450 3300 5450
Wire Wire Line
	3300 5750 3450 5750
Wire Wire Line
	3450 5750 3450 5550
Wire Wire Line
	6250 4150 7200 4150
Wire Wire Line
	6250 7050 6250 4150
Wire Wire Line
	6400 4450 7200 4450
Wire Wire Line
	6400 7900 6400 4450
Wire Wire Line
	6550 4550 7200 4550
Wire Wire Line
	6550 4550 6550 7250
Wire Wire Line
	6700 4650 7200 4650
Wire Wire Line
	6700 8100 6700 4650
Wire Wire Line
	6850 4750 7200 4750
Wire Wire Line
	2000 7450 6850 7450
Wire Wire Line
	7000 4850 7200 4850
Wire Wire Line
	7000 8300 7000 4850
Connection ~ 7200 1050
Wire Wire Line
	7200 1050 7200 3050
Wire Wire Line
	2100 1050 7200 1050
Connection ~ 8500 5150
Connection ~ 7850 7500
Wire Wire Line
	7500 7500 7500 7450
Connection ~ 8650 7600
Connection ~ 8750 7500
Wire Wire Line
	8750 7500 8750 7600
Wire Wire Line
	7850 7600 7850 7500
Wire Wire Line
	7200 4950 7200 8100
Wire Wire Line
	7700 3350 12750 3350
Wire Wire Line
	7700 3450 13300 3450
Wire Wire Line
	7700 3550 11850 3550
Wire Wire Line
	7700 3750 12500 3750
Wire Wire Line
	7700 3850 10850 3850
Wire Wire Line
	7700 4050 11400 4050
Wire Wire Line
	7700 4150 9950 4150
Wire Wire Line
	7700 4250 10600 4250
Wire Wire Line
	8950 4550 7700 4550
Wire Wire Line
	8050 4850 7700 4850
Wire Wire Line
	8700 4950 7700 4950
Connection ~ 8500 8100
Wire Wire Line
	9150 6150 9150 6350
Wire Wire Line
	8850 6450 8850 7600
Wire Wire Line
	8950 7300 8950 7600
Wire Wire Line
	7950 5950 8000 5950
Wire Wire Line
	7950 6150 7950 5950
Wire Wire Line
	8050 6850 8050 7000
Wire Wire Line
	7950 6450 7950 7600
Wire Wire Line
	8050 7300 8050 7600
Wire Wire Line
	4300 2600 4050 2600
Wire Wire Line
	3750 2600 3500 2600
Wire Wire Line
	3900 4450 3650 4450
Wire Wire Line
	3350 4450 3100 4450
Wire Wire Line
	4000 6200 4250 6200
Wire Wire Line
	3700 6200 3450 6200
Wire Wire Line
	5900 2300 5900 2450
Wire Wire Line
	6600 2300 6600 2450
Wire Wire Line
	3100 3200 4050 3200
Wire Wire Line
	3900 3300 4050 3300
Wire Wire Line
	3900 3100 4050 3100
Wire Wire Line
	3450 4950 4350 4950
Wire Wire Line
	4250 5050 4350 5050
Wire Wire Line
	4250 4850 4350 4850
Wire Wire Line
	3500 1350 4400 1350
Wire Wire Line
	4300 1450 4400 1450
Wire Wire Line
	4300 1250 4400 1250
Wire Wire Line
	2000 8300 7000 8300
Wire Wire Line
	2000 8100 6700 8100
Wire Wire Line
	2000 7900 6400 7900
Wire Wire Line
	2000 7050 6250 7050
Wire Wire Line
	2100 8200 2000 8200
Wire Wire Line
	2100 1050 2100 8200
Wire Wire Line
	2000 8000 2100 8000
Connection ~ 2100 8000
Wire Wire Line
	2000 7800 2100 7800
Connection ~ 2100 7800
Wire Wire Line
	2000 7350 2100 7350
Connection ~ 2100 7350
Wire Wire Line
	2000 7150 2100 7150
Connection ~ 2100 7150
Wire Wire Line
	2000 6950 2100 6950
Connection ~ 2100 6950
Wire Wire Line
	6550 7250 2000 7250
Wire Wire Line
	6850 7450 6850 4750
Wire Wire Line
	8500 7050 8500 8250
Wire Wire Line
	8500 6450 8500 6650
Wire Wire Line
	8500 6150 8500 5150
Wire Wire Line
	8500 6500 8700 6500
Wire Wire Line
	8700 6500 8700 4950
Connection ~ 8500 6500
Wire Wire Line
	8300 6150 8300 6500
Wire Wire Line
	8300 5650 8300 5750
Wire Wire Line
	8300 5350 8300 5150
Wire Wire Line
	8300 5700 8050 5700
Wire Wire Line
	8050 5700 8050 4850
Connection ~ 8300 5700
Wire Wire Line
	8200 6850 8050 6850
Wire Wire Line
	8850 6150 8850 5950
Wire Wire Line
	9150 5650 9150 5750
Wire Wire Line
	9150 5700 8950 5700
Wire Wire Line
	8950 5700 8950 4550
Connection ~ 9150 5700
Wire Wire Line
	9150 5150 9150 5350
Connection ~ 9150 5150
Wire Wire Line
	9300 8100 9300 7050
Connection ~ 9300 8100
Wire Wire Line
	8950 7000 8950 6850
Wire Wire Line
	8950 6850 9000 6850
Wire Wire Line
	9300 6450 9300 6650
Wire Wire Line
	9300 5150 9300 6150
Connection ~ 9300 5150
Wire Wire Line
	9300 6500 9500 6500
Wire Wire Line
	9500 6500 9500 4750
Wire Wire Line
	9500 4750 7700 4750
Connection ~ 9300 6500
Connection ~ 10400 5150
Connection ~ 9750 7500
Connection ~ 10550 7600
Connection ~ 10650 7500
Wire Wire Line
	10650 7500 10650 7600
Wire Wire Line
	9750 7500 9750 7600
Connection ~ 10400 8100
Wire Wire Line
	11050 6150 11050 6350
Wire Wire Line
	10750 6450 10750 7600
Wire Wire Line
	10850 7300 10850 7600
Wire Wire Line
	9850 5950 9900 5950
Wire Wire Line
	9850 6150 9850 5950
Wire Wire Line
	9950 6850 9950 7000
Wire Wire Line
	9850 6450 9850 7600
Wire Wire Line
	9950 7300 9950 7600
Wire Wire Line
	10400 7050 10400 8250
Wire Wire Line
	10400 6450 10400 6650
Wire Wire Line
	10400 5150 10400 6150
Wire Wire Line
	10600 6500 10400 6500
Wire Wire Line
	10600 4250 10600 6500
Connection ~ 10400 6500
Wire Wire Line
	10200 6150 10200 6500
Wire Wire Line
	10200 5650 10200 5750
Wire Wire Line
	10200 5350 10200 5150
Wire Wire Line
	9950 5700 10200 5700
Wire Wire Line
	9950 4150 9950 5700
Connection ~ 10200 5700
Wire Wire Line
	10100 6850 9950 6850
Wire Wire Line
	10750 6150 10750 5950
Wire Wire Line
	11050 5650 11050 5750
Wire Wire Line
	10850 5700 11050 5700
Wire Wire Line
	10850 3850 10850 5700
Connection ~ 11050 5700
Wire Wire Line
	11050 5150 11050 5350
Connection ~ 11050 5150
Wire Wire Line
	11200 8100 11200 7050
Connection ~ 11200 8100
Wire Wire Line
	10850 7000 10850 6850
Wire Wire Line
	10850 6850 10900 6850
Wire Wire Line
	11200 6450 11200 6650
Wire Wire Line
	11200 5150 11200 6150
Connection ~ 11200 5150
Wire Wire Line
	11400 6500 11200 6500
Wire Wire Line
	11400 4050 11400 6500
Connection ~ 11200 6500
Connection ~ 12300 5150
Connection ~ 11650 7500
Connection ~ 12450 7600
Connection ~ 12550 7500
Wire Wire Line
	12550 7500 12550 7600
Wire Wire Line
	11650 7500 11650 7600
Connection ~ 12300 8100
Wire Wire Line
	12950 6150 12950 6350
Wire Wire Line
	12650 6450 12650 7600
Wire Wire Line
	12750 7300 12750 7600
Wire Wire Line
	11750 5950 11800 5950
Wire Wire Line
	11750 6150 11750 5950
Wire Wire Line
	11850 6850 11850 7000
Wire Wire Line
	11750 6450 11750 7600
Wire Wire Line
	11850 7300 11850 7600
Wire Wire Line
	12300 7050 12300 8250
Wire Wire Line
	12300 6450 12300 6650
Wire Wire Line
	12300 5150 12300 6150
Wire Wire Line
	12500 6500 12300 6500
Wire Wire Line
	12500 3750 12500 6500
Connection ~ 12300 6500
Wire Wire Line
	12100 6150 12100 6500
Wire Wire Line
	12100 5650 12100 5750
Wire Wire Line
	12100 5350 12100 5150
Wire Wire Line
	11850 5700 12100 5700
Wire Wire Line
	11850 3550 11850 5700
Connection ~ 12100 5700
Wire Wire Line
	12000 6850 11850 6850
Wire Wire Line
	12650 6150 12650 5950
Wire Wire Line
	12950 5650 12950 5750
Wire Wire Line
	12750 5700 12950 5700
Wire Wire Line
	12750 3350 12750 5700
Connection ~ 12950 5700
Wire Wire Line
	12950 5150 12950 5350
Connection ~ 12950 5150
Wire Wire Line
	13100 8100 13100 7050
Connection ~ 13100 8100
Wire Wire Line
	12750 7000 12750 6850
Wire Wire Line
	12750 6850 12800 6850
Wire Wire Line
	13100 6450 13100 6650
Wire Wire Line
	13100 2800 13100 6150
Connection ~ 13100 5150
Wire Wire Line
	13300 6500 13100 6500
Wire Wire Line
	13300 3450 13300 6500
Connection ~ 13100 6500
Wire Wire Line
	7200 8100 13100 8100
Wire Wire Line
	7500 7500 12550 7500
Wire Wire Line
	7750 7600 7500 7600
Wire Wire Line
	7500 7600 7500 8100
Connection ~ 7500 8100
Wire Wire Line
	8650 7600 8500 7600
Connection ~ 8500 7600
Wire Wire Line
	9650 7600 9300 7600
Connection ~ 9300 7600
Wire Wire Line
	10550 7600 10400 7600
Connection ~ 10400 7600
Wire Wire Line
	11550 7600 11200 7600
Connection ~ 11200 7600
Wire Wire Line
	12450 7600 12300 7600
Connection ~ 12300 7600
Wire Wire Line
	8300 5150 13100 5150
$Comp
L R R?
U 1 1 578F825A
P 2450 8700
F 0 "R?" V 2530 8700 50  0000 C CNN
F 1 "R" V 2450 8700 50  0000 C CNN
F 2 "" V 2380 8700 50  0000 C CNN
F 3 "" H 2450 8700 50  0000 C CNN
	1    2450 8700
	1    0    0    -1  
$EndComp
Wire Wire Line
	2450 8550 2450 8300
Connection ~ 2450 8300
$Comp
L R R?
U 1 1 578F8572
P 2800 8700
F 0 "R?" V 2880 8700 50  0000 C CNN
F 1 "R" V 2800 8700 50  0000 C CNN
F 2 "" V 2730 8700 50  0000 C CNN
F 3 "" H 2800 8700 50  0000 C CNN
	1    2800 8700
	1    0    0    -1  
$EndComp
Wire Wire Line
	2800 7900 2800 8550
Connection ~ 2800 7900
$Comp
L R R?
U 1 1 578F8D98
P 3150 8700
F 0 "R?" V 3230 8700 50  0000 C CNN
F 1 "R" V 3150 8700 50  0000 C CNN
F 2 "" V 3080 8700 50  0000 C CNN
F 3 "" H 3150 8700 50  0000 C CNN
	1    3150 8700
	1    0    0    -1  
$EndComp
Wire Wire Line
	3150 8100 3150 8550
Wire Wire Line
	2450 8850 3750 8850
Connection ~ 2800 8850
$Comp
L Earth #PWR?
U 1 1 578F9215
P 2800 9050
F 0 "#PWR?" H 2800 8800 50  0001 C CNN
F 1 "Earth" H 2800 8900 50  0001 C CNN
F 2 "" H 2800 9050 50  0000 C CNN
F 3 "" H 2800 9050 50  0000 C CNN
	1    2800 9050
	1    0    0    -1  
$EndComp
Wire Wire Line
	2800 8850 2800 9050
$Comp
L R R?
U 1 1 578F99DF
P 3400 7650
F 0 "R?" V 3480 7650 50  0000 C CNN
F 1 "R" V 3400 7650 50  0000 C CNN
F 2 "" V 3330 7650 50  0000 C CNN
F 3 "" H 3400 7650 50  0000 C CNN
	1    3400 7650
	1    0    0    -1  
$EndComp
Wire Wire Line
	3400 7500 3400 7450
$Comp
L R R?
U 1 1 578F99E6
P 3750 7650
F 0 "R?" V 3830 7650 50  0000 C CNN
F 1 "R" V 3750 7650 50  0000 C CNN
F 2 "" V 3680 7650 50  0000 C CNN
F 3 "" H 3750 7650 50  0000 C CNN
	1    3750 7650
	1    0    0    -1  
$EndComp
Wire Wire Line
	3750 7050 3750 7500
$Comp
L R R?
U 1 1 578F99ED
P 4100 7650
F 0 "R?" V 4180 7650 50  0000 C CNN
F 1 "R" V 4100 7650 50  0000 C CNN
F 2 "" V 4030 7650 50  0000 C CNN
F 3 "" H 4100 7650 50  0000 C CNN
	1    4100 7650
	1    0    0    -1  
$EndComp
Wire Wire Line
	4100 7250 4100 7500
Wire Wire Line
	3400 7800 4100 7800
Connection ~ 3750 7800
Wire Wire Line
	3750 8850 3750 7800
Connection ~ 3150 8850
$EndSCHEMATC
