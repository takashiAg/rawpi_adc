# -*- coding: utf-8 -*-

from RPi import GPIO


class mcp3208():
    def __init__(self, type=1, SPICLK=11, SPIMOSI=10, SPIMISO=9, SPICS=8, Voltage_divider=3.3):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SPICLK, GPIO.OUT)
        GPIO.setup(SPIMOSI, GPIO.OUT)
        GPIO.setup(SPIMISO, GPIO.IN)
        GPIO.setup(SPICS, GPIO.OUT)
        self.Voltage_divider = Voltage_divider
        self.cs = SPICS
        self.ck = SPICLK
        self.mosi = SPIMOSI
        self.miso = SPIMISO
        if type == 0:
            self.type = 0
        if type == 1:
            self.type = 1

    def read(self, adcnum):
        if adcnum > 7 or adcnum < 0:
            return -1
        GPIO.output(self.cs, GPIO.HIGH)
        GPIO.output(self.ck, GPIO.LOW)
        GPIO.output(self.cs, GPIO.LOW)

        commandout = adcnum
        commandout |= 0x18
        commandout <<= 3
        for i in range(5):
            if commandout & 0x80:
                GPIO.output(self.mosi, GPIO.HIGH)
            else:
                GPIO.output(self.mosi, GPIO.LOW)
            commandout <<= 1
            GPIO.output(self.ck, GPIO.HIGH)
            GPIO.output(self.ck, GPIO.LOW)
        adcout = 0
        # 13ビット読む（ヌルビット＋12ビットデータ）
        for i in range(13):
            GPIO.output(self.ck, GPIO.HIGH)
            GPIO.output(self.ck, GPIO.LOW)
            adcout <<= 1
            if i > 0 and GPIO.input(self.miso) == GPIO.HIGH:
                adcout |= 0x1
        GPIO.output(self.cs, GPIO.HIGH)
        if self.type == 1:
            adcout = float(adcout) / 4096 * self.Voltage_divider
        return adcout

    def read_all(self):
        read_adc = []
        for i in range(8):
            read_adc.append(self.read(i))
        return read_adc[:]
