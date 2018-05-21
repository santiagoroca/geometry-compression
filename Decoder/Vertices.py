

class VerticesDecoder():

    # data is expressed as an array of integers
    # in the next manner, eg:
    #
    # data = [1, 192, 32] = [00000001, 11000000, 00100000]
    # output = [0000000111, 0000000010]  = 7 (0000 discarded)
    # (10 bits number biased)
    #
    # t -
    #
    # uv - are the two color coordinates which are strided into the final
    # buffer. Memory allocated is formatted in the next way
    # vx, vy, vz, s0, t0, vx, vy, vz, s0, t0...
    #
    # Since this algorithm proccess a single geometry, UV coordinates are
    # constant for all vertices of the current execution
    #
    def __init__(self, data, t, uv):

        # The original implementation received an empty array intialized to
        # zero, which length, matched the final ammount of vertexts
        # in this algorithm, we're pushing the numbers at the end of the array
        # but we're keeping vertex_index to have a clearer and more relatable
        # explanation to the original implementation
        out = []

        # Fills up the mask array with the PO2 of 0-9
        # 1, 2, 4, 8, 16, 32, 64, n...
        masks = [ 1 << x for x in range(10) ]

        # Keeps traks of the current bit beeing readed
        # 10 bits length numbers
        current_bit_position = 9

        # Current position of vertex_index
        # Since the original function received an array of length v.length
        # initialized to zero, the index was used to place the corresponding
        # vertices in the corresponding position
        data_index = 0

        # Keeps track of the current component of the vertex beeing
        # uncompressed. 0 = x, 1 = y, 2 = z, 3 and 4 are the S and T
        # coordinates of the colors (UV)
        vertex_index = 0

        # Since al vertices are ints of 8 bits, this variable is used to
        # accumulate bits of each number until 10 bits processing is reached
        # After, vertex is reset to 0 and the process keeps gogin from the
        # current index position
        vertex = 0

        # Research - This is probably, because values are expressed as integers
        # but original data was floating point numbers. This numbers is
        # probably used to move the final result from int to its floating point
        # representation
        ncl = (1 << 10) - 1

        for index in range(len(data)):

            # Byte value currently beeing proccesed
            byte = data[index]

            # Range from 0 to 7, reversed, which means we're going
            # to check each bit from end to start, applying the maks to each
            for byte_index in reversed(range(8)):

                # CHeck if the current byte intercepts the mask in the
                # current byte_index. Since each mask is a single-bit-one number
                # we're actually checking if the current bit, is 1
                if byte & masks[byte_index]:

                    # If the current bit is one, it means that the current
                    # position is one, thus, we apply the value to the final
                    # number.
                    #
                    # This time we're using current_bit_position, since we
                    # want the value of the mask relative to the current
                    # vertex beeing proccesed
                    vertex |= masks[current_bit_position]

                # If we've just proccesed the last bit, we're moving to
                # store the built vertext, in the vertex's list
                if bit == 0:

                    # Research - We're appending the new vertex
                    # More explanation needed here
                    out.append(vertex / nlc) * t[3] + t[vertex_index++]

                    # Reset the vertext to zero to start accumulating
                    # bits again
                    vertex = 0

                    # Restart the bit position to start accumulating bits
                    # from 9 to zero again
                    bit = 9

                    # If we're procesing the last component of the vertex (vz),
                    # we proceed to also add the two map components S, T
                    if vertex_index == 3:

                        # Reset the vertex index to start saving from x through
                        # z
                        vertex_index = 0

                        # Appends the two UV coordinates so final memory layout
                        # looks like vx, vy, vz, s0, t0, for each proccessed
                        # vertex
                        out.append(uv[0])
                        out.append(uv[1])

                else:

                    # If the current bit position is still not 0, thus, not the
                    # last position, we keep moving down until we reach the
                    # last bit
                    current_bit_position -= 1
