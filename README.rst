Texting Centre
==============
Texting Centre is a full featured enterprise level texting solution to send, receive, process and categorise replies, autoreply and follow-up on texts to customers and prospects while keeping track of the communications and producing statistics.

Texting Centre integrates with an external SMS gateway via REST API or with Huawei USB GSM modems. 


.. image:: https://github.com/fmalina/texting/blob/master/docs/screenshot.png?raw=true

Installation
------------

::

    git clone https://github.com/fmalina/texting.git
    cd texting/
    pip3 install -r requirements.txt
    ./manage.py migrate
    ./manage.py runserver

Features and usage
------------------
Plug in your GSM modems (Huawei USB dongles) or get account with an SMS gateway such as `SMS Breadcast <https://www.smsbroadcast.co.uk>`_.

Campaigns
~~~~~~~~~
Beauty of the Texting Centre comes from empowering you to send targetted, relevant and scriptable campaigns out to your focus groups, so that your prospects and customers actually love the texts you send out to them and find them helpful.

The campaign is setup using **templates** and work by regular pulls of your `JSON data source (categorised names and numbers) <sms/tests/campaign-data.json>`_ from your ``TEXTING_API_URL`` with ``TEXTING_API_KEY`` as per your `crontab schedule <crontab.txt>`_ and `settings_local.py <settings_local_example.py>`_, same ``TEXTING_API_URL`` gets notified via POST when sending completes.

Templates (campaign texts)
~~~~~~~~~~~~~~~~~~~~~~~~~~
Templates are texts you are sending to your focus groups. For sending scheduled campaigns the template name needs to match your focus group name from your `data source <sms/tests/campaign-data.json>`_ .

Followups are the "Hi, how did you get on?" type of texts sent out 2 days later to increase success of your campaign and get feedback.

Processing replies and incoming texts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
There are 2 ways of receiving the incoming texts:

 - Via API inbound call, where the SMS gateway makes a callback to Texting Centre with the received text
 - From the GSM modem via ``manage.py read_in`` command, which reads texts from SIM card into the database and cleans up the SIM

Texting centre allows staff to sort replies and **incoming texts** using **reply types**, categories based on which Texting Centre may react. Basic categories should be "Thanks", "End", "Bot", "Misc".

 - "Thanks" is for marking texts where users thank you for your suggestion in multitude of ways. In a good campaing these should be prevalent.
 - "End" is for marking texts where users tell you to STOP texting them in expressive ways.
 - "Bot" marks spam texts you are bound to receive.
 - "Misc" is for texts too random to reply to in a useful way.

... and then there are your own categories for eventualities.

When texts are received they are automatically put into a category based on previous categorised texts.

SIM cards and Networks
~~~~~~~~~~~~~~~~~~~~~~
When sending texts using multiple GSM modems (dongles), Texting Centre allows you to add and manage the **Networks** and **SIM cards** tucked in your GSM dongles, tracking how many texts were sent using each SIM card per day and showing this in the **Stats**. This helps not to go over a certain limit as agreed with your operator for your plan.

When using an SMS gateway API, it will be your only network such as SMSBCAST and it's credentials are to be stored as a SIM using that Network.
To setup your SMS Broadcast credentials please follow `notes <docs/NOTES.rst>`_.

For communications with Huawai GSM Dongles we maintain `PyHumod <https://github.com/oozie/pyhumod>`_ driver, using USB through PySerial.

Greeting
~~~~~~~~
Greeting allows you to end your text with a timely and seasonal greeting by replacing the keyword "{greeting}" in your template with "Have a good night" or "Merry Christmas" based on time and date.
This is handled by the ``greeting`` module. Feel free to add season greetings for your country.


Dual Licensing
--------------

Commercial license
~~~~~~~~~~~~~~~~~~
If you want to use Texting Centre to develop and run commercial campaigns, projects and applications, the Commercial license is the appropriate license. With this option, your source code is kept proprietary.

Once purchased, you are granted a commercial BSD style license and all set to use Texting Centre in your business.

`Small Team License (£900) <https://fmalina.github.io/pay.html?amount=900&msg=Texting_Centre_Team_License>`_
Small Team License for up to 8 developers

`Organization License (£3200) <https://fmalina.github.io/pay.html?amount=3200&msg=Texting_Centre_Organisation_License>`_
Commercial Organization License for Unlimited developers

Open source license
~~~~~~~~~~~~~~~~~~~
If you are creating an open source application under a license compatible with the GNU GPL license v3, you may use Texting Centre under the terms of the GPLv3.

