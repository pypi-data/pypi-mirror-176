from collections import Counter


class wordExclusionRate:
    # hypothesis --> path to the hypothesis file
    # reference --> path to the reference file
    def __init__(self, hypothesis, reference):
        self.hypothesis = hypothesis
        self.reference = reference

    def measures(self):
        # reading the txt files into a list of words
        with open(self.reference, "r", encoding="utf8") as ref_file:
            reference_words = ref_file.read().split()
        with open(self.hypothesis, "r", encoding="utf8") as hyp_file:
            hypothesis_words = hyp_file.read().split()
        # generating counter objects for the list of words in hypothesis and reference
        ref_count = Counter(reference_words)
        hyp_count = Counter(hypothesis_words)
        # generating the number of occurrences of words which are omitted from the reference file
        # Eg: D1 = Counter({'A': 2, 'B': 1, 'C': 4, 'D': 5})
        # D2 = Counter({'A': 3, 'B': 4, 'C': 4, 'D': 7})
        # D2 -D1 = Counter({'B': 3, 'D': 2, 'A': 1})
        values = (ref_count - hyp_count).values()
        # calculating the ration of numbers which are omitted from the reference file
        if sum(n < 0 for n in values) == 0:
            return (sum(values) / len(reference_words)) * 100


