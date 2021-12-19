---
title: Equipment and software I use
date: 2021-07-11
---

# Equipment and software I use

## Hardware
I built a desktop computer back in 2017. So far I have managed to upgrade it quite a bit and since I got sick from all the consoomerism, I do not plan to upgrade my computer anytime soon.  
The specs are following:  

**Processor**  
I use AMD Ryzen 1600. I would say it is quite good CPU for my purposes. I might even consider this CPU as AMD's version of i5 2500k, in terms of its longetivity and useability. That being said this CPU is still using x86 architecture,
which is heavily compromised by glowies, by having essentially a built in [backdoor](https://www.tomshardware.com/news/design-flaws-backdoors-amd-ryzen,36657.html), which not only could be used by glowies, 
but also by random black-hat hackers, whenever a new exploit is found.

**Graphics card**  
My desktop has not one, but two graphics cards. One is Nvidia GTX 1070ti and the other one is AMD RX 480. The reason for two completely different graphics cards is actually quite simple. Since I sometimes setup virtual machines
for different purposes, I'd like to have near native graphics performance in my guest operating systems. For this purpose I do PCI passthrough and in order to do PCI passthrough I must isolate secondary graphics card from the host 
machine completely. The secondary graphics card in my case is AMD RX 480.  
For more information about isolating graphics card and setting up PCI passthrough for the vm, check out this Arch wiki [article](https://wiki.archlinux.org/title/PCI_passthrough_via_OVMF)  

**Memory**  
I have a good amount of 32GB of memory (mainly because of my virtual machine autism).

**Storage devices**  
For root file system I use a 500GB ssd, which I also use to store EFI and swap partitions. I also have one 1TB hard drive, which has 90% of its storage capacity used. To combat this issue I also have
two 2TB hard drives in raid. This provides me some additional storage space that is much needed in my case.


## Software
When it comes to software I try to mostly avoid proprietary software (or isolate it in virtual machine and use it that way if really needed). The only bad exception, when I really need to use proprietary software is when I need to install
Nvidia drivers, because Nvidia as a company is a capitalist pig that hates free software. 

![Linus from Linus Tech Tips showing his dissatisfaction with Nvidia](/res/linus_nvidia.png)

### Basic software

**Operating system**  
I use Debian Linux on my desktop and Arch btw linux on my laptops. The reason being that Debian and Arch are the most popular distros that just work and don't have too much bloat preinstalled. 
I have also used other distributions in the past such as Void linux, Gentoo and even Ubuntu at some point. As much as I can tell, there is not much difference 
between distros, other than the package management system, init system and the amount of bloat that comes preinstalled with clean installation.

**Window manager**  
I use my own configuration of suckless's dwm alongside with my own configuration of dmenu. In addition I always set the GTK theme as Chicago95 for better visual compatibility with the status bar and GTK ui. I haven't really found any 
good QT themes that would look uniform with Chicago95, but I don't really care either since I don't really use programs that use QT anyway.  
My dwm configuration can be found [here](https://git.sadblog.xyz/dwm) and dmenu configuration can be found [here](https://git.sadblog.xyz/dmenu)  

**Terminal emulator**  
As for the terminal emulator I use suckless's st. It does all that it needs to do, it is lightweight and it is quite customisable. My custom st build can be found at following [link](https://git.sadblog.xyz/st).

**Web browser**  
I use Firefox ESR with hardened configuration, since I despise Chromium based browsers. That being said Firefox is still quite bad browser out of the box for the following reasons: the amount of telemetry it sends back home, useless features such as pocket, 
Goolag as its default search engine, gimped down user interface, no adblocking by default, and the leftist agenda that Mozilla is propagating. However once the tweaking part is done it is quite a good browser. If the tweaking is too much I can recommend more
sane fork of Firefox called [Librewolf](https://librewolf-community.gitlab.io/). It has all the same functionality as regular Firefox, but without telemetry, with more private search engine providers by default and with uBlock origin preinstalled.


### Utilities
**Text editor**  
I use Neovim for text editing, which is essentially just a community driven fork of Vim, which onto itself is a fork of old unix based text editor called Vi. Vim is a completely different world onto itself and its keybindings are really nice to use, once 
you master the Vim wizardry. My init.vim (vimrc for Neovim) can be found [here](https://git.sadblog.xyz/dotfiles/tree/.config/nvim/init.vim)

**File manager**
For the file manager I use vifm and / or just terminal. Vifm is a great terminal file manager, which can be extended to even show image previews using Überzug! That being said the only reason for me to ever use file manager is when I need to find a 
specific image from my badly organised image directory with timestamps as image file names.

**3D Modelling**
I use Blender for 3D modelling. However I am still quite novice at using it.


### Multimedia
**Media player**  
I use mpv for listening to music and consooming videos locally or from the internet using youtube-dl. MPV is literally the best media player out there. It is quite lightweight (compared to vlc for example), it is extensible with userscripts,
it has decent selection of commandline options and most importantly it is very keyboard friendly media player.

**Image viewer**  
I use feh for image viewing. It supports most of the image formats (except animated gifs), is quite small and can be used to set wallpapers for X11.

**Image manipulation (read: meme manipulation program)**  
GIMP, it is decent enough.


### Productivity and communication
**Mail client**  
I use Thunderbird, since I am lazy and it just werks®. It's not great email client, since it is quite bloated by using Mozilla's gecko engine, but it is good enough for my purposes. If you'd like a CLI mail client use something like mutt instead.

**PDF viewer**  
For PDF viewer I use mupdf. It does what it is supposed to do, show the PDF file. That being said mupdf does not have many fancy features including printing capability, but that can be done using lpr anyways.

**Torrent client**  
For torrenting stuff, I use transmission-cli. It is probably the most basic bitch choice (along with qbittorrent), but it works and is not too bloated.

**Typesetting**  
For typesetting I use LaTex because all cool kids use it, so I must as well. I like Latex, since it allows to create fancy mathematical equations, automatic paragraph numbering, automatic ToC generation and decent bibliography management. 
Also Latex allows to create a correctly formated documents with ease. Which means that I can just focus on writing the document and not having to worry about formating (assuming that I have necessary template created).

**Presentations**  
Whenever I need to create a presentation I just write a Markdown file, then use pandoc to convert the markdown file into Latex using Beamer class and finally compile the Latex file into PDF. It is really easy to do and much better than having
to use something like Libreoffice or even worse Google slides.

**Spreadsheets**  
For spreadsheets, I use Libreoffice calc, because I have Libreoffice installed anyways for opening word documents, when needed.
