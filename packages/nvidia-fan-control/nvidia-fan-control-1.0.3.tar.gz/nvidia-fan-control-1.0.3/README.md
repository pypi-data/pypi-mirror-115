# <img src="https://github.com/tudo75/nvidia-fan-control/blob/eb194449a0f87ad48520faa60e8548fbd44ab934/nvidia_fan_control/nvidiafancontrol.svg" alt="Icon" width="50px;" height="50px;"/> Nvidia Fan Control

GUI fan controller for Nvidia GPU

With this app you can set your preferred fan speed for Nvidia GPU (on Linux systems) without to use command line tools.

<b>Note:</b> Tested on GTX 460

![GUI Main Image](https://github.com/tudo75/nvidia-fan-control/blob/5308b771412321387d9f219d7e88ba8e4457abef/gui.png)

## Credits
Based on the work of Sabin Dcoster [nvidia-fan-control-gui-linux](https://github.com/dcostersabin/nvidia-fan-control-gui-linux)

## Disclaimer
NVIDIA is a registered trademark of NVIDIA Corporation.

Developers and app are not related to NVIDIA.

## Installation
To install the app:

<code>pip install nvidia_fan_control</code>

or

<code>sudo pip install nvidia_fan_control</code>

## Usage

1. Open application through the created menu launcher or from terminal 

    <code>nvidiafancontrol</code>

2. Click on: <i>"Initialize Nvidia Xconfig"</i>
4. If you receive a positive confirmation dialog then click on: <i>"Reboot"</i>.
If you receive an error message, you should install the <code>nvidia-smi</code> package and retry
5. After <i>Reboot</i> reopen app and set desired speed


