import struct


if __name__ == '__main__':
    def float_to_binary64(value):
        # Utilise struct.pack pour convertir le flottant en une représentation binaire
        packed_value = struct.pack('>d', value)
        print(f'packed_value: {packed_value}')
        # Utilise struct.unpack pour obtenir un entier non signé (64 bits)
        unpacked_value = struct.unpack('>Q', packed_value)[0]
        # Convertit l'entier en une chaîne binaire de 64 bits
        binary_string = f'{unpacked_value:064b}'
        
        return binary_string

    def display_float_components(value):
        binary_string = float_to_binary64(value)
        
        # Sépare les parties du format IEEE 754
        sign = binary_string[0]
        exponent = binary_string[1:12]
        fraction = binary_string[12:]
        
        return f'Sign: {sign}\nExponent: {exponent}\nFraction: {fraction}'

    # Exemple d'utilisation
    float_value = 30
    binary_representation = float_to_binary64(float_value)
    components = display_float_components(float_value)

    print(f'Float value: {float_value}')
    print(f'Binary representation: {binary_representation}')
    print(f'{components}')
