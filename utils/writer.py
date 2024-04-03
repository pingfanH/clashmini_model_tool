from .bytestream import ByteStream

from struct import pack



class Writer:
	def __init__(self, endian: str = "<"):
		self.stream = ByteStream()
		self.endian = endian
	
	def writeInteger(self, value: int, size: int):
		endian = "little" if self.endian == "<" else "big"
		self.stream.write(int(value).to_bytes(size, endian, signed=True))
	
	def writeUInteger(self, value: int, size: int):
		endian = "little" if self.endian == "<" else "big"
		self.stream.write(int(value).to_bytes(size, endian, signed=False))
	
	def writeInt8(self, value: int):
		self.stream.write(pack("b", int(value)))
	
	def writeUInt8(self, value: int):
		self.stream.write(pack("B", int(value)))
	
	def writeInt16(self, value: int):
		self.stream.write(pack(self.endian + "h", int(value)))
	
	def writeUInt16(self, value: int):
		self.stream.write(pack(self.endian + "H", int(value)))
	
	def writeInt32(self, value: int):
		self.stream.write(pack(self.endian + "i", int(value)))
	
	def writeUInt32(self, value: int):
		self.stream.write(pack(self.endian + "I", int(value)))
	
	def writeInt64(self, value: int):
		self.stream.write(pack(self.endian + "q", int(value)))
	
	def writeUInt64(self, value: int):
		self.stream.write(pack(self.endian + "Q", int(value)))
	
	def writeFloat16(self, value: float):
		self.stream.write(pack(self.endian + "e", float(value)))
	
	def writeFloat32(self, value: float):
		self.stream.write(pack(self.endian + "f", float(value)))
	
	def writeFloat64(self, value: float):
		self.stream.write(pack(self.endian + "d", float(value)))
	
	def writeBool(self, value: bool):
		if value:
			self.writeUInt8(1)
		else:
			self.writeUInt8(0)
	
	def writeChar(self, string: str):
		for char in string:
			self.stream.write(char.encode("UTF8"))
	
	def writeString(self, string: str = None):
		if string:
			self.writeUByte(len(string))
			self.writeChar(string)
		else:
			self.writeUByte(255)
	
	def writeUTF(self, string: str):
		self.writeUInt16(len(string))
		self.writeChar(string)
	
	writeByte = writeInt8
	writeUByte = writeUInt8
	
	writeShort = writeInt16
	writeUShort = writeUInt16
	
	writeInt = writeInt32
	writeUInt = writeUInt32
	
	writeLong = writeInt64
	writeULong = writeUInt64
	
	writeHalf = writeFloat16
	writeFloat = writeFloat32
	writeDouble = writeFloat64
	
	def writeNormalizedInt8(self, value: float):
		self.writeInt8(round(value * 127))
	
	def writeNormalizedUInt8(self, value: float):
		self.writeUInt8(round(value * 255))
	
	def writeNormalizedInt16(self, value: float):
		self.writeInt16(round(value * 32512))
	
	def writeNormalizedUInt16(self, value: float):
		self.writeUInt16(round(value * 65535))
	
	writeNByte = writeNormalizedInt8
	writeNUByte = writeNormalizedUInt8
	
	writeNShort = writeNormalizedInt16
	writeNUShort = writeNormalizedUInt16
