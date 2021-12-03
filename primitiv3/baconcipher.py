# %%

# note - challenge says combo of "a POW code from second indo china war" and "cipher from the first folio"
# 1 - knock code, 2 - Baconian cipher
# you can largely ignore the knock code, just need to recognize that for each pair of 5/3 dashes you get one symbol
with open("./knock copy", 'r') as f:
    data = f.readlines()

# remove the word knock and split on whitespace
# produces a list of lists, outer is each line, inner is the dashes in each line
all = []
for str in data:
    all.append(str.replace("knock", "").split())


# replace each string of dashes which it's length
lens = []
for line in all:
    lens.append([len(s)//2 for s in line])


# Remove all the 5s as they don't add values
flat = []
for sublist in lens:
    for item in sublist:
        if item != 5:
            flat.append(item)

# replace 3s with a and bs with 4. Arguably unnecessary but I coped the lookup table from a site which had it in As and Bs
letters = ["a" if item == 3 else "b" for item in flat]


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# break the list into chunks of 5 ABs for the cipher
ch = list(chunks(letters, 5))

bacon = [''.join(l) for l in ch]

lookup = {'A': 'aaaaa', 'B': 'aaaab', 'C': 'aaaba', 'D': 'aaabb', 'E': 'aabaa',
          'F': 'aabab', 'G': 'aabba', 'H': 'aabbb', 'I': 'abaaa', 'J': 'abaab',
          'K': 'abaab', 'L': 'ababa', 'M': 'ababb', 'N': 'abbaa', 'O': 'abbab',
          'P': 'abbba', 'Q': 'abbbb', 'R': 'baaaa', 'S': 'baaab', 'T': 'baaba',
          'U': 'babaa', 'V': 'babab', 'W': 'babaa', 'X': 'babab', 'Y': 'babba',
          'Z': 'babbb'}
# reverse the lookup table so it goes encoded to decoded
reverse_cipher = {v: k for k, v in lookup.items()}

# do the thing

print(''.join([reverse_cipher[word] for word in bacon]))
