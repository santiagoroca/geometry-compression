##
#
#   Receives a data string a compress it to LZW
#
##
from array import array


class StringBitReader:

    def readstring(self, data):

        # Total ammount of data to read
        data_length = len(data)

        # Current position pointer
        cursor = 0

        while cursor < data_length:

            # Get numeric (ASCII) representation of current character
            yield data[cursor]

            cursor += 1



class Compress:

    # 9 bits per char (0 to 8)
    BITS_PER_CHAR = 8

    # Last value is reserved for EOF Sign
    EOF = (2 << BITS_PER_CHAR) - 1

    # Last value (before EOF) is reserved for EOD (end of dictionary) Sign
    EOD = (2 << BITS_PER_CHAR) - 2

    def __init__(self, data):

        sbReader = StringBitReader()

        # Prefix Starts empty and stores the biggest match found in dictionary
        prefix = ""

        # Creates a dictionary pre-filled with the 256 ASCII codes
        dictionary  = { chr(x): int(x) for x in range(255) }

        # Binary Output
        out = array('i')

        # Current Code starts from 256 (all posible chars in ASCII)
        code = 256

        for char in sbReader.readstring(data):

            # If the current character and the preceiding prefix are not present
            # in the dictionary, add them to the output
            if prefix + char in dictionary:
                prefix += char

            # If the chain is not in the dictionary, we output the current
            # Prefix's code, and store the new chain in the dictionary
            else:

                # Send current prefix to output file
                out.append(dictionary[prefix])

                # Add new prefix to output
                dictionary[prefix + char] = code
                code += 1

                # Set current char as prefix
                prefix = char

        # Save output to file
        output_file = open('compressed', 'wb')
        out.tofile(output_file)
        output_file.close()
        print(out)

uncompressed = open("./uncompressed", "r")
compress = Compress(uncompressed.read())
