class ByteStream:
	def __init__(self, buffer: bytes = None):
		if buffer is None:
			buffer = b""
		
		self.buffer = buffer
		self.pos = 0
	
	def tell(self):
		return self.pos
	
	def seek(self, pos: int):
		self.pos = pos
	
	def skip(self, amount: int):
		self.pos += amount
	
	def eof(self):
		if self.tell() == len(self.buffer):
			return True
		return False
	
	def read(self, length: int):
		data = self.buffer[self.pos:self.pos + length]
		self.pos += length
		
		return data
	
	def check(self, length: int):
		data = self.read(length)
		self.seek(self.tell() - length)
		
		return data
	
	def write(self, data: bytes):
		self.buffer += data
	
	def fill(self, amount: int, size: int = 1):
		for x in range(amount):
			self.write(b"\x00" * size)
