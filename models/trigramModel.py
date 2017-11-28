import random
from nGramModel import *
from collections import defaultdict, Counter

class TrigramModel(NGramModel):

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the NGramModel object)
        Effects:  this is the TrigramModel constructor, which is done
                  for you. It allows TrigramModel to access the data
                  from the NGramModel class.
        """
        super(TrigramModel, self).__init__()

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts, a three-dimensional dictionary. For
                  examples and pictures of the TrigramModel's version of
                  self.nGramCounts, see the spec.
        Effects:  this function populates the self.nGramCounts dictionary,
                  which has strings as keys and dictionaries as values,
                  where those inner dictionaries have strings as keys
                  and dictionaries of {string: integer} pairs as values.

                  Note: make sure to use the return value of prepData to
                  populate the dictionary, which will allow the special
                  symbols to be included as their own tokens in
                  self.nGramCounts. For more details, see the spec.
        """
        
        def trigramiteration(words):
            count = len(words)
            for i in range(count - 2):
                yield words[i], words[i+1], words[i+2]
        
        self.nGramCounts = defaultdict(dict)
        listofwords = self.prepData(text)
        flattenList =[item for sublist in listofwords for item in sublist]
        counts = Counter(trigramiteration(words = flattenList))
        for unigram, bigram, trigram in counts:
            self.nGramCounts[unigram][bigram] = {}
            self.nGramCounts[unigram][bigram][trigram] = counts[(unigram, bigram, trigram)]
        self.nGramCounts = dict(self.nGramCounts)
    

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 2
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the TrigramModel, see the spec.
        """

        if sentence[-2] in self.nGramCounts.keys():
          if sentence[-1] in self.nGramCounts[sentence[-2]].keys():
            return True
          else:
            return False
        else:
          return False
    

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  TrigramModel sees as candidates, see the spec.
        """
        return self.nGramCounts[sentence[-2]][sentence[-1]]


###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    # Add your tests here
    text = [ ['the', 'quick', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    sentence = [ 'the', 'quick', 'brown' ]
    trigramModel = TrigramModel()
    trigramModel.trainModel(text)
    print trigramModel.trainingDataHasNGram(sentence)


