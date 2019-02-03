def split_lyrics(lyric, entries):
    """
    Use nltk to split the lyrics into arpabet phones
    """
    line_arpas = []
    arpa_words = []

    for n in lyric:
        l = []
        for subent in entries:
            if n.lower() in subent:
                l.append(subent)
                break
            elif n.lower() == 'rtrn':
                l.append(('rtrn', ['R1']))

        for arp in l[0][1]:
            line_arpas.append(arp)
            arpa_words.append(l[0][0])
    return line_arpas, arpa_words


def contain_nums(s):
    return any(i.isdigit() for i in s)


def generate_pairs(chunks):
    """
    Generate all possible permutations of length 2 (order doesn't matter)
    """
    outcomes = chunks
    length = 2
    ans = set([()])
    for dummy_idx in range(length):
        temp = set()
        for seq in ans:
            for item in outcomes:
                if item not in seq:
                    new_seq = list(seq)
                    new_seq.append(item)
                    temp.add(tuple(new_seq))
        ans = temp
    sorted_sequences = [tuple(sorted(sequence)) for sequence in ans]
    return set(sorted_sequences)
