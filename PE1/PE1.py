def counterW(statement):
    exWords = {
        'and', 'but', 'or', 'nor', 'for', 'so', 'yet','a', 'an', 'the','of'
    }
    words = statement.split()

    wCount = {}
    for word in words:
        if word.lower() not in exWords:
            wCount[word] = wCount.get(word, 0) + 1

    lowWords = {word: count for word, count in wCount.items() if word.islower()}
    upWords = {word: count for word, count in wCount.items() if word[0].isupper()}

    lowSorted = sorted(lowWords.items())
    upSorted = sorted(upWords.items())

    for word, count in lowSorted:
        print(f"{word.ljust(10)} - {count}")

    for word, count in upSorted:
        print(f"{word.ljust(10)} - {count}")

    totalFiltered = sum(wCount.values())
    print(f"Total words filtered: {totalFiltered}")


statement = input("Enter a string statement:\n")
counterW(statement)