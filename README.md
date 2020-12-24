# raspberry-pi-e-paper-display
Raspberry Pi Zero W with a 5 inch ePaper Display

## Python Addons
```
pip3 install RPi.GPIO
pip3 install spidev
pip3 install Pillow
```

## Other Libaries

### Install WiringPi Library
```
cd
sudo apt-get install wiringpi
wget https://project-downloads.drogon.net/wiringpi-latest.deb
sudo dpkg -i wiringpi-latest.deb
gpio -v
```


### Install C Library bcm2835

```
cd
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz
tar zxvf bcm2835-1.60.tar.gz 
cd bcm2835-1.60/
sudo ./configure
sudo make && sudo make check && sudo make install
```

### Activate SPI

Make sure that SPI is active in interfaces in `sudo raspi-config`.

## Links

https://www.waveshare.com/wiki/Pioneer600#Libraries_Installation_for_RPi

https://www.waveshare.com/wiki/E-Paper_Driver_HAT

https://www.waveshare.com/7.5inch-e-paper.htm