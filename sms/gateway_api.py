import urllib.parse
import urllib.request


def api_call(key, data):
    data.update({'username': key.user, 'password': key.pwd})
    data = urllib.parse.urlencode(data)
    req = urllib.request.Request(key.url, data.encode())
    return urllib.request.urlopen(req).read().decode()


def send(key, to, from_, message, ref):
    """ Send text. Accepts key(SIM object with user+pwd) following string args.
    to: '07000000000', # Multiple numbers can be separated by a comma.
    from_: 'MyCompany', message: 'This is our test message', ref: 'abc123'
    """
    data = {'to': to, 'from': from_, 'message': message, 'ref': ref}
    response = api_call(key, data)
    for data_line in response.split("\n"):
        l = data_line.split(':')
        if   l[0] == "OK":
            print(f"The message to {l[1]} was successful, with reference {l[2]}")
        elif l[0] == "BAD":
            print(f"The message to {l[1]} was NOT successful. Reason: {l[2]}")
        elif l[0] == "ERROR":
            print(f"There was an error with this request. Reason: {l[1]}")


def receive(get):
    """ Receive inbound text. Accepts GET request dictionary with following keys.
    to: The receiving mobile number 
    from: The sending mobile number 
    message: SMS content 
    """
    msg = urllib.parse.unquote_plus(get["message"])
    return get["to"], get["from"], msg


def balance(key):
    data = {'action': 'balance'}
    res = api_call(key, data).split(":")
    if res[0] == "OK":
        print("SMS Broadcast balance is "+res[1])
    elif res[0] == "ERROR":
        print("There was an error with this request. Reason: "+res[1])


def status(get):
    """ Return message status.
    to: The receiving mobile number
    ref: Your reference number, if provided when sending
    smsref: SMS Broadcast reference number
    status: Message status
    """
    return get["to"], get["ref"], get["smsref"], get["status"]
