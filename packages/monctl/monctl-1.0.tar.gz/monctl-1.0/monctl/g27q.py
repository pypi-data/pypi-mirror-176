import usb.core
import usb.util
from time import sleep

class G27Q:
	_dev=None	# Device Handler
	_usb_delay = 50/1000 # 50 ms sleep after every usb op

	_VID=0x2109	# (VIA Labs, Inc.)
	_PID=0x8883	# USB Billboard Device
	properties={
		"Brightness": {
			"min"	: 0,
			"max"	: 100,
			"code"	: [0x10, 0x00]
		},
		"Contrast": {
			"min"	: 0,
			"max"	: 100,
			"code"	: [0x12, 0x00]
		},
		"Sharpness": {
			"min"	: 0,
			"max"	: 10,
			"code"	: [0x87, 0x00]
		},
		"BlueLight": {
			"min"	: 0,
			"max"	: 10,
			"code"	: [0xe0, 0x0b]
		},
		"ColorMode": {
			"min"	: 0,
			"max"	: 3,
			"code"	: [0xe0, 0x03]
		},
		"Red": {
			"min"	: 0,
			"max"	: 100,
			"code"	: [0xe0, 0x04]
		},
		"Green": {
			"min"	: 0,
			"max"	: 100,
			"code"	: [0xe0, 0x05]
		},
		"Blue": {
			"min"	: 0,
			"max"	: 100,
			"code"	: [0xe0, 0x06]
		},
	}

	def __enter__(self):
		# Find device
		self._dev=usb.core.find(idVendor=self._VID, idProduct=self._PID)
		if self._dev is None:
			raise IOError(f"Device VID_{self._VID}&PID_{self._PID} not found")
		
		# Detach kernel driver
		self._had_driver = False
		try:
			if self._dev.is_kernel_driver_active(0):
				self._dev.detach_kernel_driver(0)
				self._had_driver = True
		except Exception as e:
			pass
		
		# Set config (1 as discovered with Wireshark)
		self._dev.set_configuration(1)
		return self

	# Optionally reattach kernel driver
	def __exit__(self, exc_type, exc_val, exc_tb):
		# Reattach kernel driver
		if self._had_driver:
			self._dev.attach_kernel_driver(0)
		# Release device
		usb.util.dispose_resources(self._dev)

	def usb_write(self, b_request: int, w_value: int, w_index: int, message: bytes):
		bm_request_type = 0x40
		if not self._dev.ctrl_transfer(bm_request_type, b_request, w_value, w_index, message) == len(message):
			raise IOError("Transferred message length mismatch")
		sleep(self._usb_delay)

	def usb_read(self, b_request: int, w_value: int, w_index: int, msg_length: int):
		bm_request_type = 0xC0
		data = self._dev.ctrl_transfer(bm_request_type, b_request, w_value, w_index, msg_length)
		sleep(self._usb_delay)
		return data

	def get_property(self, property: str):
		if not self.properties[property]:
			raise IOError("No property with that name")

		self.usb_write(
			b_request=178,
			w_value=0,
			w_index=0,
			message=bytearray([0x6E, 0x51, 0x83, 0x01])
				+ bytearray(self.properties[property]['code']),
		)
		data = self.usb_read(b_request=162, w_value=0, w_index=111, msg_length=12)
		return data[10]
	
	def set_property(self, property: str, value: int):
		if not self.properties[property]:
			raise IOError("No property with that name")

		self.usb_write(
			b_request=178,
			w_value=0,
			w_index=0,
			message=bytearray([0x6E, 0x51, 0x84, 0x03]
				+ self.properties[property]['code']
				+ [max(self.properties[property]['min'], min(self.properties[property]['max'], value))]),
		)