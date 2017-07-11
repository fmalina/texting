Integrating with SMS broadcast
==============================

Create a new network named SMSBCAST.

Create a new SIM using network SMSBCAST.
Enter your username and password with API URL:
https://api.smsbroadcast.co.uk/api-adv.php

::

    from sms.models import Sim, Net
    
    net, _c = Net.objects.get_or_create(name='SMSBCAST')
    key, _c = Sim.objects.get_or_create(net=net,
        url='https://api.smsbroadcast.co.uk/api-adv.php')


GSM modems
==========
Interesting AT commands

+CLAC - list all commands supported
+CNUM - gives a number on the sim card (not supported on older O2 SIMS)
+COPS - show SIM operator

List of AT commands
http://www.forensicswiki.org/wiki/AT_Commands

List of GSM error codes
http://www.smssolutions.net/tutorials/gsm/gsmerrorcodes/

Need your phone number?
On Vodafone, Asda, press the following to request:
*#100#  - your number
*#147#  - last caller
*#1345# - your onscreen credit
*#06#   - show serial no
