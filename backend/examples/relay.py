#!/usr/bin/env python3

import time

import automationhat


ah = automationhat
ah.output.one.on()
time.sleep(1)
ah.output.one.off()

