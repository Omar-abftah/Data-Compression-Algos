from decimal import Decimal, getcontext
import typing

getcontext().prec = 100


class FloatingPointCodec:
    def __init__(self, byte_size: int = 1):
        self.size = byte_size

    def decimal_to_bytes(self, value: Decimal) -> typing.Tuple[int, bytes]:
        sign, mantissa, exponent = value.as_tuple()
        binary_representation = sign.to_bytes(1, 'big')
        binary_representation += exponent.to_bytes(2 * self.size, 'big', signed=True)
        num_bytes = 1 + 2 * self.size

        for digit in mantissa:
            binary_representation += digit.to_bytes(1, 'big')
            num_bytes += 1

        return (num_bytes, binary_representation)

    def bytes_to_decimal(self, value: bytes) -> Decimal:
        sign = int.from_bytes(value[0:1], 'big')
        exponent = int.from_bytes(value[1:1 + 2 * self.size], 'big', signed=True)

        digits = [
            int.from_bytes(value[i:i + 1], 'big')
            for i in range(1 + 2 * self.size, len(value))
        ]

        return Decimal((sign, tuple(digits), exponent))

    def encode(self, input_string: str, binary_file: str) -> None:
        total_chars = len(input_string)
        frequency_map = {}
        for char in input_string:
            frequency_map[char] = frequency_map.get(char, 0) + 1

        start = Decimal(0)
        range_map = {}
        for char, count in frequency_map.items():
            prob = Decimal(count) / total_chars
            range_map[char] = (start, start + prob)
            start += prob

        lower, upper = Decimal(0), Decimal(1)
        for char in input_string:
            char_range = range_map[char]
            range_size = upper - lower
            upper = lower + range_size * char_range[1]
            lower = lower + range_size * char_range[0]

        encoded = (upper + lower) / 2

        with open(binary_file, 'wb') as f:
            f.write(total_chars.to_bytes(4, 'big'))
            f.write(len(range_map).to_bytes(1, 'big'))

            for char, (start, end) in range_map.items():
                f.write(char.encode('utf-8'))

                start_bytes = self.decimal_to_bytes(start)
                f.write(start_bytes[0].to_bytes(1, 'big'))
                f.write(start_bytes[1])

                end_bytes = self.decimal_to_bytes(end)
                f.write(end_bytes[0].to_bytes(1, 'big'))
                f.write(end_bytes[1])

            encoded_bytes = self.decimal_to_bytes(encoded)
            f.write(encoded_bytes[0].to_bytes(1, 'big'))
            f.write(encoded_bytes[1])

    def decode(self, binary_file: str) -> str:
        with open(binary_file, 'rb') as f:
            total_chars = int.from_bytes(f.read(4), 'big')
            map_range = int.from_bytes(f.read(1), 'big')
            char_ranges = {}

            for _ in range(map_range):
                char = f.read(1).decode('utf-8')

                start_bytes_length = int.from_bytes(f.read(1), 'big')
                start = self.bytes_to_decimal(f.read(start_bytes_length))

                end_bytes_length = int.from_bytes(f.read(1), 'big')
                end = self.bytes_to_decimal(f.read(end_bytes_length))

                char_ranges[char] = (start, end)

            encoded_bytes_length = int.from_bytes(f.read(1), 'big')
            encoded_number = self.bytes_to_decimal(f.read(encoded_bytes_length))

            decoded_string = ""
            for _ in range(total_chars):
                for char, (low, high) in char_ranges.items():
                    if low <= encoded_number < high:
                        decoded_string += char
                        range_size = high - low
                        encoded_number = (encoded_number - low) / range_size
                        break

            return decoded_string


def main():
    input_string = input("Enter the string to be compressed: ")

    codec = FloatingPointCodec()
    binary_file_name = input("Enter the binary file name: ")

    codec.encode(input_string, binary_file_name)
    decoded = codec.decode(binary_file_name)

    with open("output.txt", "w") as output_file:
        output_file.write(decoded)

    print(decoded == input_string)


if __name__ == "__main__":
    main()