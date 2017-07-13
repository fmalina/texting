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
Plug in your GSM modem (USB Huawei dongle) or get account with an SMS gateway such as `SMS Breadcast <https://www.smsbroadcast.co.uk>`_.

Campaigns
---------
Beauty of the Texting Centre comes from empowering you to send targetted, relevant and scriptable campaingns out to your focus groups, so that your prospects and customers actually love the texts you send out to them and find them helpful.

At present the campaign is setup using `settings_campaign.py <settings_campaign_example.py>` file and work by regular pulls of your `JSON data (categorised names and numbers) <sms/tests/campaign-data.json>` from your ``API_URL`` with ``API_KEY`` as per your `crontab schedule <crontab.txt>`.

Settings allow you to set your base text template ``TPL``, and your map of ``CATEGORIES`` matching your ``TEXTS``. ``TEXTS`` can be straight strings or templates with their relevant bits put in place based on category.

Followups are the "Hi, how did you get on?" type of texts sent out 2 days later to increase success of your campaign and get feedback.

Processing replies and incoming texts
-------------------------------------
There are 2 ways of receiving the incoming texts:

 - Via API inbound call, where the SMS gateway makes a callback to Texting Centre with the received text
 - from the GSM modem via ``manage.py read_in`` command, which reads texts from SIM card into the database and cleans up the SIM

Texting centre allows staff to sort incoming texts
 **replies** into **categories** and react based on this category. Basic categories should be "Thanks", "End", "Bot", "Misc".

 - "Thanks" is for marking texts where users thank you for your suggestion in multitude of ways. In a good campaing these should be prevalent.
 - "End" is for marking texts where users tell you to STOP texting them in expressive ways.
 - "Bot" marks spam texts you are bound to receive.
 - "Misc" is for texts too random to reply to in a useful way.

... and then there are your own categories for eventualities.

When texts are received they are automatically put into a category based on previous categorised texts.

Greeting
--------
Each text in a campaing is run by ``custom_replace`` function specified in your compaign settings. This allows you to finish your text with a timely and seasonal greeting, for example by replacing the words "Greetings" in your template with "Have a good night" or "Merry Christmas" based on time and date. This is handled by the ``greeting`` module. Feel free to add seasons and it's greeting to it for your country. ``custom_replace`` also allows for postprocessing such as adjusting URLs for a particular category of users.

SIM cards and Networks
----------------------
When sending texts using multiple GSM modems (dongles), Texting Centre allows you to add and manage the **Networks** and **SIM cards** tucked in your GSM dongles, tracking how many texts were sent using each SIM card per day and showing this in the **Stats**. This helps not to go over a certain limit as agreed with your operator for your plan.

When using an SMS gateway API, it will be your only network such as SMSBCAST and it's credentials are to be stored as a SIM using that Network.
To setup your SMS Broadcast credentials please follow `notes <NOTES.rst>`_.

For communications with Huawai GSM Dongles we maintain `PyHumod <https://github.com/oozie/pyhumod>`_ driver, using USB through PySerial.


