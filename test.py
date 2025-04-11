import sys
if sys.argv[1] :
    # Има аргумент от командния ред
    url = sys.argv[1]
else:
    # Няма аргумент, питай потребителя
    url = input("Paste URL (q for exit): ")

if url.lower() == 'q':
            print("Bye")
            sys.exit()


# Сега input_text съдържа текста, или от аргумента, или от въвеждането
print("Въведеният текст е:", input_text)