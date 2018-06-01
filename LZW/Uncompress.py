##
#
#   Receives a data string a compress it to LZW
#
##
from array import array

def get_size(fileobject):
    fileobject.seek(0, 2)
    size = fileobject.tell()
    fileobject.seek(0, 0)
    return size


class Uncompress:

    def __init__(self, data):

        # Create the dictionary containing the first two bit values
        dictionary  = { int(x): chr(x) for x in range(255) }

        # Current Code starts from 256 (all posible chars in ASCII)
        code = 256

        # Prev code, holds the last processed code
        prev_code = data[0]

        # First next is the first character of the current_substr after each
        # iteration
        first_next = ""

        # The current working sub string, prospect to be part of the output
        current_substr = ""

        #  Output file
        out = chr(prev_code)

        #
        for index in range(1, len(data)):

            # Get next possible character of sequence
            current_code = data[index]

            # If the current character is not in the
            # dictionary, yet, we append it to the current_substr
            if not current_code in dictionary:

                # Previous code + current code makes the new substr
                current_substr = dictionary[prev_code] + first_next

            else:

                # Since the character is present, we set it as the active one
                # and prepare it to be appended to the output
                current_substr = dictionary[current_code]

            # Output current substr
            out += current_substr

            # We take the first character from the current String
            # To create the new entry in the dictionary
            first_next = current_substr[0]

            # Create the new entry in the dictionary
            dictionary[code] = dictionary[prev_code] + first_next
            code += 1

            # Previous code is now the current code just created
            prev_code = current_code

        print(len(out), len(data))

        # Diplay
        print(out)



compressed_data = open("./compressed", "r")
compressed = array('I')
compressed.fromfile(compressed_data, get_size(compressed_data) / 4)
uncompress = Uncompress(compressed)
