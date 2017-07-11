Texting Centre
==============
Texting centre is a full featured enterprise level texting solution.

It can send, receive, process, categorise, autoreply and follow-up on texts to customers and prospects while keeping track of the communications and producing statistics.

Texting centre integrates with an external SMS gateway via REST API or with hardware GSM modems such as Huawei USB dongles. 


.. image:: https://github.com/fmalina/texting/blob/master/README-screenshot.png?raw=true

Installation
------------

::

    git clone https://github.com/fmalina/texting.git
    cd texting/
    pip3 install -r requirements.txt
    ./manage.py migrate
    ./manage.py runserver

Usage
-----

Plug in your GSM modem (USB Huawei dongle) or Get account with SMS Breadcast.
GSM modem integration uses ` PyHumod <https://github.com/oozie/pyhumod>`_.

To setup your SMS breadcast credentials use `./manage.py shell`
and follow `notes <NOTES.rst>`_
