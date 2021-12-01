#%%

#note - challenge says combo of "a POW code from second indo china war" and "cipher from the first folio"
#1 - knock code, 2 - Baconian cipher
with open("./knock copy", 'r') as f:
    data = f.readlines()
data
# %%
all = []
for str in data:
    all.append(str.replace("knock", "").split())

all[0:5]
# %%
lens = []
for line in all:
    lens.append([len(s)//2 for s in line])
lens
# %%
flat = []
for sublist in lens:
    for item in sublist:
        if item !=5:
            flat.append(item)

letters = ["a" if item == 3 else "b" for item in flat ]
# %%
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

ch = list(chunks(letters, 5))

bacon = [''.join(l) for l in ch]
bacon
# %%
lookup = {'A':'aaaaa', 'B':'aaaab', 'C':'aaaba', 'D':'aaabb','E':'aabaa',
    'F':'aabab', 'G':'aabba', 'H':'aabbb', 'I':'abaaa', 'J':'abaab',
    'K':'abaab', 'L':'ababa', 'M':'ababb', 'N':'abbaa', 'O':'abbab',
    'P':'abbba', 'Q':'abbbb', 'R':'baaaa', 'S':'baaab', 'T':'baaba',
    'U':'babaa', 'V':'babab', 'W':'babaa', 'X':'babab', 'Y':'babba', 
    'Z':'babbb'}
reverse_cipher = {v: k for k, v in lookup.items()}

# %%
for i in range(len(bacon)):
    print(reverse_cipher[bacon[i]])
# %%
print (''.join([reverse_cipher[word] for word in bacon]))
# %%
