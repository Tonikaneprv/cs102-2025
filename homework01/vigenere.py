def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    ext_key = ""

    if len(keyword) < len(plaintext):
        for i in range(len(plaintext)):
            ext_key += keyword[i % len(keyword)]
    else:
        ext_key = keyword

    for i, char in enumerate(plaintext):
        char_key = ext_key[i]
        if char.isupper():
            shift = ord(char_key.upper()) - ord("A")
            new_char = chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
            ciphertext += new_char
        elif char.islower():
            shift = ord(char_key.lower()) - ord("a")
            new_char = chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
            ciphertext += new_char
        else:
            ciphertext += char

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    ext_key = ""

    if len(keyword) < len(ciphertext):
        for i in range(len(ciphertext)):
            ext_key += keyword[i % len(keyword)]
    else:
        ext_key = keyword

    for i, char in enumerate(ciphertext):
        key_char = ext_key[i]
        if char.isupper():
            shift = ord(key_char.upper()) - ord("A")
            new_char = chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
            plaintext += new_char
        elif char.islower():
            shift = ord(key_char.lower()) - ord("a")
            new_char = chr((ord(char) - ord("a") - shift) % 26 + ord("a"))
            plaintext += new_char
        else:
            plaintext += char

    return plaintext
