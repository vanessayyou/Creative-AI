import random
from nGramModel import *
from collections import defaultdict, Counter


class BigramModel(NGramModel):

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the BigramModel object)
        Effects:  this is the BigramModel constructor, which is done
                  for you. It allows BigramModel to access the data
                  from the NGramModel class by calling the NGramModel
                  constructor.
        """
        super(BigramModel, self).__init__()

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts, a two-dimensional dictionary. For examples
                  and pictures of the BigramModel's version of
                  self.nGramCounts, see the spec.
        Effects:  this function populates the self.nGramCounts dictionary,
                  which has strings as keys and dictionaries of
                  {string: integer} pairs as values.

                  Note: make sure to use the return value of prepData to
                  populate the dictionary, which will allow the special
                  symbols to be included as their own tokens in
                  self.nGramCounts. For more details, see the spec.
        """
        #generator that makes word combitions
        def bigramiteration(words):
            count = len(words)
            for i in range(count - 1):
                yield words[i], words[i + 1]
    
        #Preps text makes it so we can use the Counter() function on it
        self.nGramCounts = defaultdict(dict)
        listofwords = self.prepData(text)
        flattenList = [item for sublist in listofwords for item in sublist ]
        #Counts all the combitions generated
        counts = Counter(bigramiteration(words = flattenList))
        #indexes all new data into the self.nGramCounts dictionary
        for unigram1, unigram2 in counts:
            self.nGramCounts[unigram1][unigram2] = counts[(unigram1, unigram2)]
        self.nGramCounts = dict(self.nGramCounts)

    def trainingDataHasNGram(self, sentence):
        """s
        Requires: sentence is a list of strings, and len(sentence) >= 1
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the BigramModel, see the spec.
        """
        if sentence[-1] in self.nGramCounts.keys():
          return True
        else:
          return False

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  BigramModel sees as candidates, see the spec.
        """
        return self.nGramCounts[sentence[-1]]

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    # Add your test cases here
    text = [ ['the', 'quick', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    text.append([ 'quick', 'brown' ])
    sentence = [ 'lazy', 'the' ]
    bigramModel = BigramModel()
    print(bigramModel)
    bigramModel.trainModel(text)
    print(bigramModel.trainingDataHasNGram(sentence))
    print(bigramModel.getCandidateDictionary(sentence))


