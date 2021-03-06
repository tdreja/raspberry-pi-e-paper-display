# Raspberry Pi (Zero W): 7.5 inch ePaper Display

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

### Other Libraries

```
sudo apt-get install libopenjp2-7
sudo apt-get install libtiff5
```

### Google API
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Activate SPI

Make sure that SPI is active in interfaces in `sudo raspi-config`.

## Links

https://www.waveshare.com/wiki/Pioneer600#Libraries_Installation_for_RPi

https://www.waveshare.com/wiki/E-Paper_Driver_HAT

https://www.waveshare.com/7.5inch-e-paper.htm

## Image Size

Height: 384px
Width: 640px

Block size: 16px

## Cronjob

Call Script every 5 Minutes
```
*/5 * * * * cd /home/pi/raspberry-pi-e-paper-display/ && python3 display_test.py >> /home/pi/python.log 2>&1
```