from device import device
data = device.led.status()


print('Device status: %r' % data)
result = device.led.state()
print(result)