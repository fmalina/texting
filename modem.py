from serial import SerialException
from serial.tools import list_ports
from humod.siminfo import seq, show_imsi
from sms.models import Sim, gateway_sim
import humod

pre  = '/dev/cu.HUAWEIMobile-'
# m = humod.Modem(pre+'Modem', pre+'Pcui')
# print(m.show_model())

def get_modems():
    """Return a list of modems plugged into the computer.
    Switched to text mode."""
    ports = list_ports.comports()
    ports = [s.device for s in ports if s.device.startswith(pre)]
    no1 = True if 'Modem' in ''.join(ports) else False
    ports = [int(p.replace(pre, '')) for p in ports if p[-1].isdigit()]
    ports = [(y, z) for x,y,z in seq(ports, 3)]
    if no1: ports.append(('Modem', 'Pcui'))
    modems, info = {}, []
    for i, pair in enumerate(ports):
        try:
            modems[i] = humod.Modem(
                pre+str(pair[0]),
                pre+str(pair[1])
            )
            modems[i].enable_textmode(True)
        except OSError as e:
            info.append(('Power off.', str(e), i+1))
        except SerialException as e:
            info.append(('Not connected.', str(e), i+1))
        except humod.errors.AtCommandError as e:
            info.append(('', str(e), i+1))
            del modems[i]
    return modems, info

def list_devices(dev=None):
    """Return a list with gateway SIM and GSM modems with their SIM cards,
    current device (SIM+modem or Gateway) and info messages if any."""
    modems, info = get_modems()
    gateway = gateway_sim()
    
    senders = list(modems.items())
    if gateway:
        fake_modem = (len(modems)+1, False)
        senders.append(fake_modem)
    
    devices, current = [], {}
    for i, modem in senders:
        if not modem:
            sim = gateway
        else:
            imsi = None
            try:
                imsi = show_imsi(modem)
            except (IOError, OSError) as e:
                info.append(('Turned off', e, i+1))
            except humod.errors.AtCommandError as e:
                info.append(('SIM error', e, i+1))
            if imsi and imsi.isdigit():
                sim, created = Sim.objects.get_or_create(imsi=imsi)
            
        ok = dev == str(i) or False
        device = {'i': i, 'modem': modem, 'sim': sim, 'current': bool(ok)}
        devices.append(device)
        if ok: current = device
    
    devices = sorted(devices, key=lambda k: str(k['sim']))
    return devices, current, info