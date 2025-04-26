# py-MCC-USB-TC
Simple python code that uses the `mccdaq` lib to gather all temperature data from a [MCC USB-TC thermocouple device](https://digilent.com/shop/mcc-usb-temp-and-tc-series-temperature-and-voltage-measurement-usb-daq-devices/?srsltid=AfmBOoolRMjAcx3jR9GDfbEzpXCI7UAlbfnUXj0Jnu_xijO5TsiLRdl2) and save to file. Packagable to standalone executable on Windows.

I made an article where this project was used, check it out: [Drying Filament](https://raniseth.com/blog/2025-04-26-Drying-Filament.html).

## Linux 

For running on Linux, the `mcculw` library is exchanged for the `uldaq` library. Follow installation instructions on the [uldaq github](https://github.com/mccdaq/uldaq) before building or running.

Your user needs access to the USB device. The easiest way is to add your user to the dialout group.

```
sudo usermod -a -G dialout $USER
```

## Package to standalone .exe for Windows

Easily done with [PyInstaller](https://pyinstaller.org).

```
pip install -U pyinstaller
pyinstaller log_temp.py
```

## Plotting on acqisition device

If you want to get a quick peek at the temperature data while logging on device, you can use the plot_tc.py script. It requires python with pandas and matplotlib installed. You also need to edit the script to look for the data in the correct directory by modifying `DATADIR`.

The `.bat` file is just for ease of running the script and also needs an updated path to the script.



Made for use in the electrochemistry lab at [NTNU](https://www.ntnu.edu/ima/research/electrochemistry) in 2024 for monitoring of 18650 battery cells.