# lasertag

lasertag-Spiel auf ESP32-Basis. Jeder Spieler erhält einen Markierer mit Infrarotsender und Laserpointer und eine Weste mit IR-Sensoren. Ziel des Spieles ist es, die gegnerischen Westen zu taggen. Es kann jeder gegen jeden oder in Teams gespeilt werden. Es wird aus Videospielen bekannte Spielmodi und Features geben wie Capture-the-flag, powerups, heilen, Markiereraufladung, ...

## Features
- [x] Spiel ohne Weste nur mit Markierern spielbar
- [x] Markieren und markiert werden per gebündeltem IR, mehrere Bytes per Markierung übertragbar für z. B. Player-ID und Trefferpunkte
- [ ] Kommunikation per Wifi, ein Spieler eröffnet am Markierer über das Farb-Grafikdisplay ein Spiel, andere können joinen
- [ ] Effekte über ansteuerbare LED-Streifen und Sound
- [ ] Weste per Bluetooth oder WLAN angebunden

## Hardware
Momentan wird ein TTGO BTC T4 Modul genutzt welches schon recht viel bietet. Das Modul wird auf eine noch zu designende Platine gesteckt. Später soll es emehrere zusammenlöt- oder steckbare Platinen geben die zusammen die Form des Markierers bilden. Griff und ähnliches werden 3D gedruckt. Display, Akkuladeschaltung, An-Aus, 3 Buttons, ESP32 mit extra 4MB RAM, MicroSD-Slot, gerausgeführte IOs.

## Software
Die Firmware von badge.team dient als Basis. Sie stellt eine Micropython Umgebung mit App-Store und viel unterstützter Hardware bereit.

## Projektstand
Proof of concept. Es gibt Testhardware auch Lochrasterplatine. Die Peripherie kann bereits angesprochen werden:
- [x] IR-LED, IR-Empfänger: Senden und empfangen von UART-Bytes mit CRC16 Checksumme 38 kHz moduliert
- [x] Display: Anzeigen von Text, Linien, Rechtecken, ...
- [x] Buttons
- [x] SK6812 einzeln ansteuerbare LEDs
- [x] Laserpointer

ToDo:
- [ ] Testcode für Peripherie
- [ ] Zuverlässige Fehlerkorrektur finden (CRC16 auf 2 Datenbytes reicht nicht)
- [ ] Testcode für Markieren und getroffen werden
- [ ] Reichweitentests, Schaltung mit FETs für IR-Sender entwickeln
- [ ] Platine designen und Prototypen fertigen lassen
- [ ] Gutes Konzept für Audio finden und umsetzen
- [ ] Dieses Git schöner strukturieren

## Initial Setup
Wir starten mit einem frischen Debian Testing, es muss kein Desktop installiert werden.

Dependencies:
```
apt-get install make unzip git libncurses5-dev flex bison gperf python-serial libffi-dev libsdl2-dev libmbedtls-dev perl python-pip
pip2 install --upgrade pip
```

badge.team git:
```
git clone https://github.com/badgeteam/ESP32-platform-firmware.git --depth 1
cd ~/ESP32-platform-firmware/
git submodule update --init --recursive
unzip -p toolchain/xtensa-esp32-elf-linux64.zip xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar | tar xvf -

export PATH="$PATH:/root/ESP32-platform-firmware/xtensa-esp32-elf/bin"
python -m pip install --user -r /root/ESP32-platform-firmware/esp-idf/requirements.txt
```

Copy default config for TTGO BTC T4
```
cp firmware/configs/ttgo_t4_defconfig firmware/sdkconfig
```

Configure IOs and periphery (delete chars with Shift+Backspace):
```
./config.sh
```
- Serial flasher config --> (/dev/ttyUSB0) Default serial port
- Serial flasher config --> Flash size: 4MB (TTGO BTC)
- Component config --> MicroPython --> modules --> opus: disable
- Component config --> Driver: ILI9341 LCD display (Reset: 5, D: 26, CS: 27, BL: -1, Ori: 1)
- Component config --> neoplixel: enable, Pin 19 (TTGO BTC)
- Firmware & device configuration --> Code-name of the firmware, MicroPython modules directory, Name of the badge on the app hatchery: lasertag
- save as default filename

Create folder for python code and copy default files:
```
mkdir ./firmware/python_modules/lasertag
cp ./firmware/python_modules/ttgo-t4/* ./firmware/python_modules/lasertag -r
```

clone lasertag git:
```
git clone https://github.com/larsmm/lasertag.git ./firmware/python_modules/lasertag/lasertag
mv ./firmware/python_modules/lasertag/lasertag/root_dir/* ./firmware/python_modules/lasertag
```

add this to beginning of build.sh (make clean is buggy):
```
rm -r firmware/build
```

## Write code, build and flash

Put code in ./firmware/python_modules/lasertag or ./firmware/python_modules/lasertag/lasertag 

Build:
```
export PATH="$PATH:/root/ESP32-platform-firmware/xtensa-esp32-elf/bin"
./build.sh
```

Connect USB and Flash:
```
export PATH="$PATH:/root/ESP32-platform-firmware/xtensa-esp32-elf/bin"
./flash.sh
```

Console to test code:
```
export PATH="$PATH:/root/ESP32-platform-firmware/xtensa-esp32-elf/bin"
./monitor.sh
```
- Ctrl+]  Exit program
-- Ctrl+T  Menu escape key, followed by:
--- Ctrl+R  Reset target board via RTS line
--- Ctrl+F  Build & flash project
--- Ctrl+A  Build & flash app only

Run .py files:
```
import l
import lasertag.l
```

Get details about binary size:
```
cd firmware
make size-components
cd ..
```
From left to right:
- DRAM .data: Size of segment containing initialisation data for static variables
- DRAM .bss: Size of segment that will be reserved in DRAM for uninitialised static variables (not relevant for you)
- IRAM: Size of segment containing static variables and functions placed in IRAM
- Flash code: total size of all code in the archive file
- rodata: total size of all data contained in the archive file
- Total: total size of the archive filemake size-files
(framebuffer ist so groß wegen der integrierten fonts. Die kann man auskommentieren: driver_framebuffer_text.cpp a list of fonts is defined (remove both the corresponding pointer and the string from the two lists to remove the font))

## Notizen
Python code da rein: /firmware/python_modules, alternativ als app bauen (dann würden sie in der fat partition landen)

faq:
eine lib fehlt: menüconfig ganz unten

Speicher: python_modules liegt nicht in der fat partition. in der fat partition liegen die apps. "To make the firmware smaller you can remove built-in python modules from the python_modules folder, but it's also possible to look elsewhere. For example in driver_framebuffer_text.cpp a list of fonts is defined (remove both the corresponding pointer and the string from the two lists to remove the font)" "also: now that it compiles you can do "make size-components" and "make size-files" to see what parts of the firmware are taking up space"
Sonst muss die partition table csv angepasst werden. Zum Test kann man die debug_4MB.csv nehmen. Die lässt aber seehhr wenig platz für fat.
Opus abschalten: ./config.sh --> Component config --> MicroPython --> modules --> opus

also keep in mind that doing partial builds without removing the "build" folder is a bit broken in some situations due to micropython being stupid so if you encounter "weird" python errors do a full rebuild. build.sh macht keinen full rebuild weil make clean broken ist. full rebuild: "rm -r build"

known problems:
"E (512) esp_image: Image length 1614480 doesn't fit in partition length 1572864" mit rebootschleife im monitor.sh: config.sh --> Serial flasher config --> Flash size: 4MB (TTGO BTC)