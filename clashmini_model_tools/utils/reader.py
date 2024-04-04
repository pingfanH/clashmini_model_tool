from .bytestream import ByteStream

from struct import unpack



class Reader:
	def __init__(self, buffer: bytes, endian: str = "<"):
		self.stream = ByteStream(buffer)
		self.endian = endian
	
	def readInteger(self, size: int):
		endian = "little" if self.endian == "<" else "big"
		return int.from_bytes(self.stream.read(size), endian, signed=True)
	
	def readUInteger(self, size: int):
		endian = "little" if self.endian == "<" else "big"
		return int.from_bytes(self.stream.read(size), endian, signed=False)
	
	def readInt8(self):
		return unpack("b", self.stream.read(1))[0]
	
	def readUInt8(self):
		return unpack("B", self.stream.read(1))[0]
	
	def readInt16(self):
		return unpack(self.endian + "h", self.stream.read(2))[0]
	
	def readUInt16(self):
		return unpack(self.endian + "H", self.stream.read(2))[0]
	
	def readInt32(self):
		return unpack(self.endian + "i", self.stream.read(4))[0]
	
	def readUInt32(self):
		return unpack(self.endian + "I", self.stream.read(4))[0]
	
	def readInt64(self):
		return unpack(self.endian + "q", self.stream.read(8))[0]
	
	def readUInt64(self):
		return unpack(self.endian + "Q", self.stream.read(8))[0]
	
	def readFloat16(self):
		return unpack(self.endian + "e", self.stream.read(2))[0]
	
	def readFloat32(self):
		return unpack(self.endian + "f", self.stream.read(4))[0]
	
	def readFloat64(self):
		return unpack(self.endian + "d", self.stream.read(8))[0]
	
	def readBool(self):
		if self.readUInt8() >= 1:
			return True
		return False
	
	def readChar(self, length: int):
		return self.stream.read(length).decode("UTF8")
	
	def readString(self):
		length = self.readUInt8()
		if length != 255:
			return self.readChar(length)
		return None
	
	def readUTF(self):
		return self.readChar(self.readUInt16())
	
	readByte = readInt8
	readUByte = readUInt8
	
	readShort = readInt16
	readUShort = readUInt16
	
	readInt = readInt32
	readUInt = readUInt32
	
	readLong = readInt64
	readULong = readUInt64
	
	readHalf = readFloat16
	readFloat = readFloat32
	readDouble = readFloat64
	
	def readNormalizedInt8(self):
		return round(self.readInt8() / 127, 3)
	
	def readNormalizedUInt8(self):
		return round(self.readUInt8() / 255, 3)
	
	def readNormalizedInt16(self):
		return round(self.readInt16() / 32512, 6)
	
	def readNormalizedUInt16(self):
		return round(self.readUInt16() / 65535, 6)
	
	readNByte = readNormalizedInt8
	readNUByte = readNormalizedUInt8
	
	readNShort = readNormalizedInt16
	readNUShort = readNormalizedUInt16
