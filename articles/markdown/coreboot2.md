---
title: Compiling and flashing coreboot for T420 (corebooting part 2)
date: 2021-12-15
---

# Compiling and flashing coreboot for T420

Recently I cleaned and hacked into the locked bios of a T420 that my friend had given to me for Corebooting. Article can
be found [here](https://sadblog.xyz/blog/coreboot1.html). After having successfully unlocked the bios, it was time to
proceed with Corebooting. The main steps can be broken down into following categories: updating the vendor bios,
getting the original bios image from the flash chip, compiling the rom and flashing the rom. You will either need a Raspberry
PI setup for writing the flashchip or one of the SPI programmers that are sold on eBay for like 10$. I used a CH341A 
programmer, which came with a nice SOIC-8 clip as well.


## Updating the vendor bios

First step of performing any Corebooting is to update the vendor BIOS to the latest version possible. This ensures that the 
most up to date firmware is used, since after corebooting it becomes nearly impossible to update the firmware. For Thinkpad 
T420 you can find the latest BIOS update image from following [site](https://pcsupport.lenovo.com/us/en/products/laptops-and-netbooks/thinkpad-t-series-laptops/thinkpad-t420/downloads/DS018784).
After downloading and verifying the integrity you can proceed to flashing the BIOS update image to the USB drive. First of
all you will need to extract an El Torito image from the received ISO file. For that install `genisoimage`.
After installation extract the image with following command:

```
$ geteltorito 83uj33us.iso -o t420.img
```

Now you can flash the image to USB drive using following command:

```
$ sudo dd if=t420.img of=/dev/sdX bs=64K status=progress
```

Reboot the computer and you should be able to boot into the BIOS update utility. Just follow on-screen instructions and you
should be good to go. Additionally check the BIOS version to verify that the update really was successful.


## Extracting BLOBs from vendor BIOS

After successfully updating the bios, you should extract all necessary BLOBs, which are needed for the compilation. If you
are lucky, you should be able to dump the bios image internally. To test if internal flashing is supported run the following
command and cross your fingers:

```
$ sudo /sbin/flashrom -p internal -r bios.bin
```

If no errors are displayed, you can proceed to the next stage. If there were errors then that means that internal flashing is
unsupported and thus external measures need to be taken -\_\_-. Unfortunately in my case I could not read rom internally.


### Reading the BIOS image externally

**NOTE: I recommend to remove the CPU and memory from the motherboard to avoid accidental powering, when the programmer is connected.**

Disassemble your laptop and locate the flash chip. The flash chip should be located directly under the magnesium cover 
around the trackpad area. Once you have located the flash chip, you can connect it to the SPI programmer. Firstly 
I attempted to connect the flash chip with SOIC-8 clip but soon I realised that doing so was merely impossible to create a 
stable connection. After some frustration I decided to solder jumper wires to the motherboard instead (savage, I know).
After doing so I was prompted with something like this:

![Looks legit](/res/coreboot/SPI.png)

I tested the conductivity between chip pins and potential spots on motherboard to find out that there were special reserved
holes on the PCB connected to the flash chip (potentially for flashing purposes?) where I could conveniently solder jumper wires 
to. After doing so I connected the jumpers with my programmer.

**PLEASE ALWAYS DOUBLE, TRIPLE, QUADRUPLE CHECK THAT ALL WIRES ARE CONNECTED TO THE PROGRAMMER CORRECTLY!!! THIS CAN POTENTIALLY 
SAVE YOUR MOTHERBOARD!!!** 

After verifying that everything was correct, I connected the programmer with my laptop. I checked if the usb device is 
recognized properly and then proceeded to reading the BIOS image with following command:

```
$ sudo /sbin/flashrom -p ch341a_spi -r bios.bin.1
```

If no errors are thrown, you should repeat the reading process at least 2 times to check for potential checksum errors.
Then check the SHA256 checksums with following command:

```
$ sha256sum bios.bin.1 bios.bin.2 bios.bin.3
```

If the hashes match you are good to go, if not then check your connections and try again. Delete the other two images
and proceed with the next stage.


## Extracting firmware BLOBs from the BIOS image

For now you should have managed to successfully extract the vendor bios image from the flash chip. Clone the coreboot 
repository using following commands:

```
$ git clone https://review.coreboot.org/coreboot
$ cd coreboot
$ git submodule update --init --checkout
```

Navigate to `./util/ifdtool` and run `make` to compile it. Copy or create a symlink of the executable to `/usr/local/bin` 
for convenience and navigate to directory where BIOS image is stored. Extract the bios image into firmware blobs by using 
following command:

```
$ ifdtool -x bios.bin
```

From now on, you should be having 4 regions of the bios extracted. The files should be following: 
`flashregion_0_flashdescriptor.bin`, `flashregion_1_bios.bin`, `flashregion_2_intel_me.bin` and `flashregion_3_gbe.bin`.
Delete `flashregion_1_bios.bin` since it is not needed and rename the rest of the files to something more memorable, for example:

```
$ mv flashregion_0_flashdescriptor.bin descriptor.bin
$ mv flashregion_2_intel_me.bin me.bin
$ mv flashregion_3_gbe.bin gbe.bin
```


### Extracting the vbios

If you would like to use a custom bootsplash or use Tianocore as a payload, you will need to extract the vbios from original vendor 
bios image. For that step I recommend using [UEFITool](https://github.com/LongSoft/UEFITool), which is essentially a GUI tool for 
viewing and extracting multiple regions of your UEFI firmware images. Install and open your bios image with it. Search for the string
"VGA Compatible BIOS" and uncheck `Unicode`. If the search was successful, you should find an appropriate RAW area. Click 
"Action -> Section -> Extract Body..." to extract it from the BIOS image and give it a familiar name to later find it.


### Crippling Intel ME spyware

![Average CIA agent, looking into your loli collection on your Stinkpad running btw I use Arch Linux via Intel ME backdoor](/res/coreboot/Glow.png)

Unfortunately it is impossible to disable Intel ME completely, however it is possible to greatly restrict its capabilities using 
[me_cleaner scripts](https://github.com/corna/me_cleaner). Coreboot also gives you an option to reduce ME firmware size on compilation,
however for flexibility I usually like to clean Intel ME manually using the me_cleaner. Once you have these scripts, you can sanitize 
most of the ME functionality using following command:

```
python3 me_cleaner.py -S me.bin -O me_clean.bin
```

Once you have successfully done that you can proceed to compilation stage.


## Compiling and flashing Coreboot rom

Install following packages needed for compilation (Debian): 
```
apt install build-essential gnat flex bison libncurse5-dev wget zlib1g-dev iasl
```


Once you have installed those prerequisites navigate to Coreboot root directory and run `make nconfig`. From here on you can customise the Coreboot
to fill your needs. Make sure that the board is `Lenovo T420` and `Use CMOS for configuration values` is used and CBFS filesystem size should be set to 3MB 
(0x300000). Navigate to `Chipset` and verify that `Add Intel descriptor.bin file`, `Add Intel ME/TXE firmware` and `Add gigabit ethernet configuration` paths
are set correctly to your extracted firmware blobs. For payload I used default `SeaBIOS`. Additionally if you want to use a custom bootsplash, add the correct 
vbios rom path to `Devices -> Add a VGA BIOS image`. Bootsplash image path can be specified in `General setup -> Add a bootsplash image`. Supported formats
are bmp and jpg. If you want to use my bootsplash then link can be found [here](/res/coreboot/Bootsplash.jpg). Once you are done configuring your Coreboot build
you can start by compiling the required toolchain with following command:

```
$ make crossgcc CPUS=<n>
```

This compilation takes a looong time (on my T420 it took about 2 - 3 hours), so grab yourself a cup of coffee and something to eat while it is compiling. After 
the toolchain is build you can compile the Coreboot rom using following command:

```
$ make -j<n>
```

This shouldn't take long and once it is complete, you should find `coreboot.rom` file in `build/` directory. Now you can start flashing your freshly built 
Coreboot rom using following command:

```
$ sudo /sbin/flashrom -p ch431a_spi -w coreboot.rom
```

If no errors were present, you can reassemble the laptop and power it on. The result will be magnificent!

![](/res/coreboot/WorkingBootsplash.png)


# More information about Corebooting
* [](https://www.coreboot.org/Board:lenovo/t420)
* [](https://www.coreboot.org/Build_HOWTO)
