from .reader import Reader
from .writer import Writer

import os
import json



class GlbParser(Reader):
	def __init__(self, path: str):
		self.path = path
		
		file = open(self.path, 'rb')
		file_data = file.read()
		file.close()
		
		super().__init__(file_data, "<")
	
	def parse(self):
		magic = self.stream.read(4)
		assert magic == b"glTF"
		
		version = self.readUInt32()
		size = self.readUInt32()
		
		length = self.readUInt32()
		name = self.readChar(4) # JSON
		data = json.loads(self.readChar(length))
		
		length = self.readUInt32()
		name = self.stream.read(4) # BIN\x00
		binary = self.stream.read(length)
		
		self.compile_gltf(data, binary)
		
		print("Done")
	
	def compile_gltf(self, data: dict, binary: bytes):
		save_path = os.path.splitext(self.path)[0] + ".json"
		bin_path = os.path.splitext(self.path)[0] + ".bin"
		
		# writing path to .bin file in .gltf
		data["buffers"] = [
			{
				"byteLength": len(binary),
				"uri": bin_path
			}
		]
		
		# saving files
		json_file = open(save_path, 'w')
		json.dump(data, json_file, indent=4)
		json_file.close()
		
		bin_file = open(bin_path, 'wb')
		bin_file.write(binary)
		bin_file.close()


class GlbEncoder(Writer):
	def __init__(self, path: str):
		self.path = path
		
		file = open(self.path, 'r')
		file_data = file.read()
		file.close()
		
		self.data = json.loads(file_data)
	
	def encode(self):
		buffer = self.data["buffers"][0]
		
		bin_file = open(self.path.replace(".gltf",".bin"), 'rb')
		bin_data = bin_file.read(buffer["byteLength"])
		bin_file.close()
		
		# remove path to bin file in gltf
		del buffer["uri"]
		
		json_data = json.dumps(self.data, sort_keys=True, allow_nan=False, separators=(",", ":"))
		
		super().__init__("<")
		
		self.writeUInt32(len(json_data))
		self.writeChar("JSON")
		self.writeChar(json_data)
		
		self.writeUInt32(len(bin_data))
		self.stream.write(b"BIN\x00")
		self.stream.write(bin_data)
		
		self.compile_glb()
	
	def compile_glb(self):
		magic = b"glTF"
		version = b"\x02\x00\x00\x00"
		size = int(len(magic) + len(version) + len(self.stream.buffer) + 4).to_bytes(4, "little", signed=False)
		data = self.stream.buffer
		
		result = magic + version + size + data
		
		save_path = os.path.splitext(self.path)[0] + ".glb"
		
		file = open(save_path, 'wb')
		file.write(result)
		file.close()
