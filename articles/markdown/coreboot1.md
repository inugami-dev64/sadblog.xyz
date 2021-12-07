---
title: Cleaning and hacking Thinkpad T420 bios (corebooting part1)
date: 2021\-12\-07
---

# Hacking into Thinkpad T420 bios (corebooting part1)

My friend recently gave me a T420 for cleaning and since I personally also own
a T420 as well I asked him, if he would like to get it corebooted as well. He agreed on that. 
Once I recieved the Thinkpad it was in a quite rough condition: scratches on screen, 
awful anime stickers on it, nasty keyboard, broken plastics etc. 

![Stickered laptop](/res/coreboot/T420Before.jpg)

Firstly I attempted to remove all stickers that I could get and after rubbing 
the back of the screen with some isopropyl alchohol for about 10 minutes, I 
managed to clean off most of the sticker glue and other nastiness from it. The 
result of this cleaning looks like this:

![Cleaned laptop](/res/coreboot/T420After.jpg)

After some outer cleaning I attempted to proceed with the usual corebooting process.
The first step of corebooting any machine is to update the vendor bios to the latest 
version, since the original bios image is required for firmware blobs. After trying to
access the bios, I was prompted with the following friendly screen:

![Locked T420](/res/coreboot/BiosPass.jpg)

It seems that the bios was locked after all so I asked my friend to provide the password,
but it seemed that he had forgotten it. After hearing that I decided to hack into 
bios instead. After some research I found that it is actually possible to bypass the password by 
shorting two pins on the bios security EEPROM chip. In my case it was the PCO8A chip on the 
motherboard. The bios security EEPROM should be located on the side of the motherboard 
where CPU socket is not located. Once the security chip is located you should identify SCL and SDA pins.
Usually they should be pins 5 and six 6 (circled on the picture below)

![Bios security EEPROM](/res/coreboot/SecurityChip.jpg)

Now you should reassemble the display, power connector, keyboard, memory and cpu back together, since now 
comes the fun part of actually accessing the bios. Finally connect the power connector to the charger
and you should have something like this:

![Ghetto setup](/res/coreboot/GhettoSetup.jpg)

Take some small conductive object, such as a flat-head screwdriver and follow the following
instructions (assuming that UEFI bios is used):

* Turn on the computer
* Once the screen turns on immideately short the SCL and SDA pins together
* Press F1 repeatedly 
* If the password prompt comes up, try these steps again
* If you get into bios successfully, you can navigate to Security -> Supervisor password and
disable or add new bios password

Now you should have successfully breached bios security measures and gained access to bios
settings once again.

![Bios access gained](/res/coreboot/BiosAccess.jpg)

**NOTE: I do not take any responsibility for any possible damages caused for the laptop.
Use this tutorial at your own risk.**
