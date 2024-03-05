class ByteArrayIO:
    def __init__(self, initial_bytes=None):
        self.buffer = bytearray(initial_bytes or b"")
        self.position = 0

    def write(self, b):
        if self.position > len(self.buffer):
            # Extend the buffer with null bytes if the position is beyond the current buffer size
            self.buffer.extend(b'\x00' * (self.position - len(self.buffer)))
        
        end_position = self.position + len(b)
        # If writing beyond the current buffer, extend it
        if end_position > len(self.buffer):
            self.buffer.extend(b[len(self.buffer) - self.position:])
        else:  # Otherwise, overwrite the existing content
            self.buffer[self.position:end_position] = b

        self.position = end_position

    def read(self, size=-1):
        if size < 0:
            size = len(self.buffer) - self.position
        
        start_position = self.position
        end_position = min(self.position + size, len(self.buffer))
        self.position = end_position
        return bytes(self.buffer[start_position:end_position])

    def seek(self, offset, whence=0):
        if whence == 0:  # SEEK_SET
            self.position = offset
        elif whence == 1:  # SEEK_CUR
            self.position += offset
        elif whence == 2:  # SEEK_END
            self.position = len(self.buffer) + offset
        else:
            raise ValueError("Invalid value for 'whence'")
        self.position = max(0, self.position)  # Ensure position isn't negative

    def tell(self):
        return self.position

    def getvalue(self):
        return bytes(self.buffer)
