import tinytuya

class Device:
    def __init__(self, device_id, ip_address, local_key):
        self.led = tinytuya.BulbDevice(device_id, ip_address, local_key)
        self.led.set_version(3.5)

device = Device('################', '################', '################')
