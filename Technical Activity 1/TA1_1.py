def count():
    i = input("Please enter a string: ")
    
    v = 0  # vowel
    c = 0  # consonant
    s = 0  # whitespace
    o = 0  # other characters

    i = i.lower()

    for char in i:
        if char in 'aeiou':
            v += 1
        elif char in 'bcdfghjklmnpqrstvwxyz':
            c += 1
        elif char == ' ':
            s += 1
        else:
            o += 1
            
    print(f"Vowels: {v}")
    print(f"Consonants: {c}")
    print(f"Spaces: {s}")
    print(f"Other characters: {o}")

count()
