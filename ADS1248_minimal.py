#!/usr/bin/python
#import the library
from Adafruit_BBIO.SPI import  SPI
import Adafruit_BBIO.GPIO as GPIO

import time

class ADS1248:


	MUX0	= 0x00   
	MUX1	= 0x02

	VBIAS	= 0x01
	SYS0	= 0x03

	OFC0	= 0x04
	OFC1	= 0x05
	OFC2	= 0x06

	FSC0	= 0x07
	FSC1	= 0x08
	FSC2	= 0x09

	IDAC0	= 0x0a
	IDAC1	= 0x0b

	GPIOCFG	= 0x0c
	GPIODIR	= 0x0d
	GPIODAT	= 0x0e

	NOP = 0xff
	WREG = 0x40
	RREG = 0x20
	RDATA = 0x12

	# custom settings
	STARTPIN = "P9_15"

def RegWrite(reg,val):
	spi.xfer2([ADS1248.WREG+(reg & 0xF),0x00,val]);
	return False

def RegRead(reg):
	spi.xfer2([ADS1248.RREG+(reg & 0xF),00]);
	r = spi.xfer2([0x00]); # dummy
	return r
	
def ReadADC():
	spi.writebytes([ADS1248.RDATA]) # RDATA (read data once, page 49)
	a=spi.readbytes(3)
	spi.writebytes([ADS1248.NOP]) # sending NOP

	print (a[0]<<16)+(a[1]<<8)+a[2]
	print a[0]
	print a[1]
	print a[2]
	print "\n"
	return False

spi = SPI(0,0)	#/dev/spidev1.0
spi.msh=10000 # SPI clock set to 100 kHz
spi.bpw = 8  # bits/word
spi.threewire = False
spi.lsbfirst = False
spi.mode = 1 
spi.cshigh = False  # ADS1248 chip select (active low)
spi.open(0,0)

GPIO.setup("P9_14", GPIO.OUT)


# drive START high to start conversion

GPIO.setup(ADS1248.STARTPIN, GPIO.OUT)
GPIO.output(ADS1248.STARTPIN,GPIO.HIGH)

def ADCinit():	
	RegWrite(ADS1248.MUX0, 0b00001100);	# MUX0:  Pos. input: AIN1, Neg. input: AIN4 (Burnout current source off) 
	RegWrite(ADS1248.MUX1, 0b00100000);	# MUX1:  REF0, normal operation
	RegWrite(ADS1248.SYS0, 0b00000010);	# SYS0:  PGA Gain = 1, 20 SPS
	RegWrite(ADS1248.IDAC0,0b00000000);	# IDAC0: off
	RegWrite(ADS1248.IDAC1,0b11001100);	# IDAC1: n.c.
	RegWrite(ADS1248.VBIAS,0b00000000);	# VBIAS: BIAS voltage disabled
 	RegWrite(ADS1248.OFC0, 0b00000000);	# OFC0:  0 => reset offset calibration
	RegWrite(ADS1248.OFC1, 0b00000000);	# OFC1:  0 => reset offset calibration
	RegWrite(ADS1248.OFC2, 0b00000000);	# OFC2:  0 => reset offset calibration
	RegWrite(ADS1248.GPIOCFG, 0b00000000);	# GPIOCFG: we don't use them
	RegWrite(ADS1248.GPIOCFG, 0b00000000);	# GPIODIR: we don't use them
	RegWrite(ADS1248.GPIODAT, 0b00000000);	# GPIODAT: we don't use them

ADCinit()

while True:

	GPIO.output("P9_14",GPIO.HIGH)

	ReadADC()

	GPIO.output("P9_14",GPIO.LOW)
	time.sleep(1)

