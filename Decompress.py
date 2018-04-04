import struct

from array import array

'''

    Decompress

    Receives a file path, and decompress to vertices, colors and faces

'''


class Header:

    def __init__(self, header):

        # Constants Values
        UInt32 = 'I'
        Float32 = 'f'

        # Geometry Byte Length
        self.g_byte_l = struct.unpack_from(UInt32, header, 0)[0]
        __data = header[0:4]

        # Vertices Byte Length
        self.v_byte_l = struct.unpack_from(UInt32, header, 4)[0]

        # Faces Byte Length
        self.f_byte_l = struct.unpack_from(UInt32, header, 8)[0]

        # Total Vertices
        self.v_count = struct.unpack_from(UInt32, header, 12)[0]
        self.v_count = self.v_count + self.v_count / 3 * 2

        # Transformation vertex
        self.t_vertex = [
            struct.unpack_from(Float32, header, 16)[0],
            struct.unpack_from(Float32, header, 20)[0],
            struct.unpack_from(Float32, header, 24)[0],
            struct.unpack_from(Float32, header, 28)[0]
        ]

        # UV Vector Coordinates
        self.uv_vector = [
            struct.unpack_from(Float32, header, 32)[0],
            struct.unpack_from(Float32, header, 36)[0]
        ]

        # Total Symbols After Fan
        self.t_symbols_after_fan = struct.unpack_from(UInt32, header, 40)[0]

        # Fixed Header Length
        self.header_l = 44;


class Decompress:

    def __init__(self, file_path):

        # Reads Content from file
        data = open(file_path, 'rb')

        # Total File Size in Biytes
        self.bytes_left_to_read = self.get_size(data);

        # Store file data as binary array
        self.data = array('B')
        self.data.fromfile(data, self.bytes_left_to_read)

        # Vertex Buffer Data Arary
        self.vb_array = [];

        # Vertex Buffer Data Length
        self.vb_array_l = 0;

        # Faces Buffer Data Array
        self.fb_array = [];

        # Faces Buffer Data Array Length
        self.fb_array_l = 0;

        # Start To Read Model
        self.readModel(self.data)


    def readModel(self, model):

        # Current Header Size (Fixed)
        HEADER_SIZE = 44

        # Current position of the reading cursor
        cursor = 0

        # Read the file until there's no more bytes to read
        while self.bytes_left_to_read > 0:

            # Geometry Header
            header = Header(model[cursor:cursor + HEADER_SIZE])

            print(header.__dict__)

            # Empty array to fill up with vertices
            vertices = []

            # Empty array to fill up with faces
            faces = []

            # Read Vertices to vertices array
            # self.decode_vertices(model[padding + HEADER_SIZE: header.v_byte_l])

            # Reduce the bytes_left_to_read by the ammount of bytes readed
            self.bytes_left_to_read -= header.g_byte_l

            # Move the padding to the end of the geometry
            cursor += header.g_byte_l


    def decode_vertices(self, chain, vertices, t, uv):

        # for range(0, 9) => 1 << i
        masks = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]

        bit = 9

        v = 0

        c = 0

        vertex = 0

        # 2^10 - 1
        nlc = 1023

        for i in len(chain):
            byte = chain[i]

            for e in reversed(range(7)):

                if byte & masks[e] != 0:
                    vertex |= masks[bit]

                if bit == 0:
                    vertices[v] = vertex / nlc * t[3] + t[c]

                    v += 1
                    c += 1

                    vertex = 0
                    bit = 0

                    if c == 3:
                        c = 0
                        vertices[v] = uv[0]
                        v += 1

                        vertices[v] = uv[1]
                        v += 1

                else:
                    bit -= 1


    def get_size(self, fileobject):
        fileobject.seek(0, 2)
        size = fileobject.tell()
        fileobject.seek(0, 0)
        return int(size)
