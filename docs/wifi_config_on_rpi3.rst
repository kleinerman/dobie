Wifi Configuration on Raspberry Pi 3 under Arm Arch Linux
=========================================================

.. contents::


Configuring wpa_supplicant
--------------------------

Check the name of the wifi adapter you are going to use with the following command:

.. code-block::

  # ip link ls

Create the following file ``/etc/wpa_supplicant/wpa_supplicant-wlan0.conf`` assuming the previous command outputs ``wlan0`` as interface name with the following content:

.. code-block::

  ctrl_interface=/run/wpa_supplicant
  update_config=1

Now start wpa_supplicant with:

.. code-block::

  # wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
  
At this point run:

.. code-block::

  # wpa_cli -i wlan0

This will present an interactive prompt (>), which has tab completion and descriptions of completed commands.


Use the ``scan`` and ``scan_results`` commands to see the available networks:

.. code-block::

  > scan
  OK
  <3>CTRL-EVENT-SCAN-RESULTS

  > scan_results
  bssid / frequency / signal level / flags / ssid
  00:00:00:00:00:00 2462 -49 [WPA2-PSK-CCMP][ESS] MYSSID
  11:11:11:11:11:11 2437 -64 [WPA2-PSK-CCMP][ESS] ANOTHERSSID
 
To associate with MYSSID, add the network, set the credentials and enable it:

.. code-block::

  > add_network
  0

  > set_network 0 ssid "MYSSID"
  OK

  > set_network 0 psk "passphrase"
  OK
  
  > enable_network 0
  OK
  <3>CTRL-EVENT-SCAN-STARTED 
  <3>CTRL-EVENT-SCAN-RESULTS 
  <3>WPS-AP-AVAILABLE 
  <3>Trying to associate with 18:a6:f7:60:e6:02 (SSID='MYSSID' freq=2412 MHz)
  <3>Associated with 18:a6:f7:60:e6:02
  <3>WPA: Key negotiation completed with 18:a6:f7:60:e6:02 [PTK=CCMP GTK=TKIP]
  <3>CTRL-EVENT-CONNECTED - Connection to 18:a6:f7:60:e6:02 completed [id=0 id_str=]

Finally save this network in the configuration file:

.. code-block::

  > save_config
  OK
  

To check link status, use following command.

.. code-block::

  # iw dev interface link



To enable wireless at boot, enable the below service on your particular wireless interface.

.. code-block::

  # systemctl enable wpa_supplicant@wlan0
  
wpa_supplicant@.service - accepts the interface name as an argument and starts the wpa_supplicant daemon for this interface. It reads a ``/etc/wpa_supplicant/wpa_supplicant-interface.conf`` configuration file. For this reason the file in ``/etc/wpa_supplicant`` was named ``wpa_supplicant-wlan0.conf``



Setting the IP address trough systemd-networkd
----------------------------------------------

Create the following file ``/etc/systemd/network/wlan0.network`` assuming your interface is ``wlan0``:

.. code-block::

  [Match]
  Name=wlan0
  
  [Network]
  Address=10.10.7.71/24
  Gateway=10.10.7.1
  DNS=10.10.5.5
  
  
``systemd-resolved`` is required only if you are specifying DNS entries in .network files or if you want to obtain DNS addresses from networkd's DHCP client. Alternatively you may manually manage /etc/resolv.conf.

If you are going to use it delete or rename the existing file ``/etc/resolv.conf`` and create the following symbolic link:

.. code-block::

  # ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf
  
Enable both services at boot:

.. code-block::

  # systemctl enable systemd-networkd
  # systemctl enable systemd-resolved
  

Restart the board

 
Interesting links
-----------------

Follow the installation guide to install the Arch Linux Arm according the board being used:

**Arch Linux WPA_Supplicant configuration:** `https://wiki.archlinux.org/index.php/WPA_supplicant`

**Arch Linux Wireless network configuration:** `https://wiki.archlinux.org/index.php/Wireless_network_configuration`

**Arch Linux Systemd-Networkd:** `https://wiki.archlinux.org/index.php/systemd-networkd`
  
