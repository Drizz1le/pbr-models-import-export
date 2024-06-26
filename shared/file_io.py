import struct

class BinaryReader:
    """
    Wrapper class to simplify reading data of various types
    from a binary file (assumes big-endian byte order)
    """
    
    def __init__(self, path):
        self.file = open(path, 'rb')

    def read(self, type, base, offset=0, whence='start'):
        """
        Reads data of type `type` from `base` + `offset`
        relative to `whence` ('start' or 'current')
        """
        self.seek(base + offset, whence)
        
        if type == 'uchar':
            return struct.unpack('>B', self.file.read(1))[0]
        if type == 'ushort':
            return struct.unpack('>H', self.file.read(2))[0]
        if type == 'uint':
            return struct.unpack('>I', self.file.read(4))[0]
        if type == 'char':
            return struct.unpack('>b', self.file.read(1))[0]
        if type == 'short':
            return struct.unpack('>h', self.file.read(2))[0]
        if type == 'int':
            return struct.unpack('>i', self.file.read(4))[0]
        if type == 'float':
            return struct.unpack('>f', self.file.read(4))[0]
        if type == 'double':
            return struct.unpack('>d', self.file.read(8))[0]
        if type == 'string':
            return self._read_string()
        raise ValueError(f'Invalid value for arg `type`: {type}')

    def _read_string(self):
        """
        Reads a char[] from the current position
        and converts it to an ascii string
        """
        s = ''
        nextChar = self.file.read(1)[0] # converts byte to int
        while nextChar != 0:
            s += chr(nextChar)
            nextChar = self.file.read(1)[0]
        return s

    def read_chunk(self, offset, size, whence='start'):
        """
        Reads `size` bytes from `offset`
        relative to `whence` ('start' or 'current')
        """
        self.seek(offset, whence)
        return self.file.read(size)

    def seek(self, offset, whence='start'):
        """
        Moves the BinaryReader's file to `offset`
        relative to `whence` ('start' or 'current')
        """
        if whence == 'start':
            self.file.seek(offset)
        elif whence == 'current':
            self.file.seek(offset, 1)
        else:
            raise ValueError(f'Invalid value for `whence`: {whence}')

    def tell(self):
        """Returns the BinaryReader's current position"""
        return self.file.tell()

    def close(self):
        """Closes the BinaryReader's file"""
        self.file.close()

    @staticmethod
    def is_primitive(type):
        """
        Returns bool indicating whether `type` is a primitive
        type and can thus be read by a BinaryReader
        """
        return type in ['uchar', 'ushort', 'uint',
                        'char', 'short', 'int',
                        'float', 'double', 'string']

    @staticmethod
    def primitive_size(type):
        primitive_sizes = {
            'uchar'  : 1,
            'char'   : 1,
            'ushort' : 2,
            'short'  : 2,
            'uint'   : 4,
            'int'    : 4,
            'float'  : 4,
            'double' : 8,
        }

        if type == 'string':
            return 0
        if not BinaryReader.is_primitive(type):
            return 0

        return primitive_sizes[type]

    @staticmethod
    def is_array(type):
        return type.endswith('[]')
    
    @staticmethod
    def is_pointer(type):
        return type.endswith('*')

class BinaryWriter(BinaryReader):
    """
    Wrapper class to simplify writing data of various types
    to a binary file (uses big-endian byte order)
    """
    
    def __init__(self, path):
        self.file = open(path, 'wb+')

    def write(self, type, data, base, offset=0, whence='start'):
        """
        Writes `data` as type `type` to `offset`
        relative to `whence` ('start' or 'current')
        """
        self.seek(base + offset, whence)
        
        if type == 'uchar':
            return self.file.write(struct.pack('>B', data))
        if type == 'ushort':
            return self.file.write(struct.pack('>H', data))
        if type == 'uint':
            return self.file.write(struct.pack('>I', data))
        if type == 'char':
            return self.file.write(struct.pack('>b', data))
        if type == 'short':
            return self.file.write(struct.pack('>h', data))
        if type == 'int':
            return self.file.write(struct.pack('>i', data))
        if type == 'float':
            return self.file.write(struct.pack('>f', data))
        if type == 'double':
            return self.file.write(struct.pack('>d', data))
        if type == 'string':
            # strings should be null terminated
            return self.file.write(bytes(data, 'ascii') + b'\x00')
        raise ValueError(f'Invalid value for arg `type`: {type}')

    def write_chunk(self, data, offset, whence='start'):
        """
        Writes `data` to `offset` relative
        to `whence` ('start' or 'current')
        """
        self.seek(offset, whence)
        return self.file.write(data)
