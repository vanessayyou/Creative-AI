#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True # Suppress .pyc files

import random
from pysynth import pysynth
from data.dataLoader import *
from models.musicInfo import *
from models.unigramModel import *
from models.bigramModel import *
from models.trigramModel import *

# FIXME Add your team name
TEAM = 'Creative A.I. but not creative title'
LYRICSDIRS = ['the_beatles']
MUSICDIRS = ['gamecube']
WAVDIR = 'wav/'

###############################################################################
# Helper Functions
###############################################################################

def sentenceTooLong(desiredLength, currentLength):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  returns a bool indicating whether or not this sentence should
              be ended based on its length. This function has been done for
              you.
    """
    STDEV = 1
    val = random.gauss(currentLength, STDEV)
    return val > desiredLength

def printSongLyrics(verseOne, verseTwo, chorus):
    """
    Requires: verseOne, verseTwo, and chorus are lists of lists of strings
    Modifies: nothing
    Effects:  prints the song. This function is done for you.
    """
    verses = [verseOne, chorus, verseTwo, chorus]
    print
    for verse in verses:
        for line in verse:
            print(' '.join(line)).capitalize()
        print

def trainLyricModels(lyricDirs):
    """
    Requires: lyricDirs is a list of directories in data/lyrics/
    Modifies: nothing
    Effects:  loads data from the folders in the lyricDirs list,
              using the pre-written DataLoader class, then creates an
              instance of each of the NGramModel child classes and trains
              them using the text loaded from the data loader. The list
              should be in tri-, then bi-, then unigramModel order.
              Returns the list of trained models.
    """
    models = [TrigramModel(), BigramModel(), UnigramModel()]
    for ldir in lyricDirs:
        lyrics = loadLyrics(ldir)
        for model in models:
            model.trainModel(lyrics)
    return models

###############################################################################
# Core
###############################################################################

def trainMusicModels(musicDirs):
    """
    Requires: lyricDirs is a list of directories in data/midi/
    Modifies: nothing

    Effects:  works exactly as trainLyricsModels, except that
              now the dataLoader calls the DataLoader's loadMusic() function
              and takes a music directory name instead of an artist name.
              Returns a list of trained models in order of tri-, then bi-, then
              unigramModel objects.
    """
    models = [TrigramModel(), BigramModel(), UnigramModel()]
    # call dataLoader.loadMusic for each directory in musicDirs
    
    for mdir in musicDirs:
        music = loadMusic(mdir)
        for model in models:
            model.trainModel(music)
    return models

def selectNGramModel(models, sentence):
    """
    Requires: models is a list of NGramModel objects sorted by descending
              priority: tri-, then bi-, then unigrams.
    Modifies: nothing
    Effects:  returns the best possible model that can be used for the
              current sentence based on the n-grams that the models know.
              (Remember that you wrote a function that checks if a model can
              be us3ed to pick a word for a sentence!)
    """
    for model in models:
        if model.trainingDataHasNGram(sentence):
            #FIXME
            #print model
            return model
    return models[len(models)-1]

def generateLyricalSentence(models, desiredLength):
    """
    Requires: models is a list of trained NGramModel objects sorted by
              descending priority: tri-, then bi-, then unigrams.
              desiredLength is the desired length of the sentence.
    Modifies: nothing
    Effects:  returns a list of strings where each string is a word in the
              generated sentence. The returned list should NOT include
              any of the special starting or ending symbols.

              For more details about generating a sentence using the
              NGramModels, see the spec.
    """
    sentence = ['^::^', '^:::^']
    currentWord = selectNGramModel(models, sentence)
    while (not sentenceTooLong(desiredLength, len(sentence)-2)) and (currentWord.getNextToken(sentence) != '$:::$'):
        sentence.insert(len(sentence), currentWord.getNextToken(sentence))
        currentWord = selectNGramModel(models, sentence)
    #FIXME
    return sentence
    #return sentence[2:len(sentence)-1]

def generateMusicalSentence(models, desiredLength, possiblePitches):
    """
    Requires: possiblePitches is a list of pitches for a musical key
    Modifies: nothing
    Effects:  works exactly like generateLyricalSentence from the core, except
              now we call the NGramModel child class' getNextNote()
              function instead of getNextToken(). Everything else
              should be exactly the same as the core.
    """
    sentence = ['^::^', '^:::^']
    currentNote = selectNGramModel(models, sentence)
    while (not sentenceTooLong(desiredLength, len(sentence) - 2)) and (currentNote.getNextNote(sentence, possiblePitches) is not '$:::$'):
        sentence.insert(len(sentence) - 1, currentNote.getNextNote(sentence, possiblePitches))
        currentNote = selectNGramModel(models, sentence)
    return sentence[2:len(sentence) - 1]

def runLyricsGenerator(models):
    """
    Requires: models is a list of a trained nGramModel child class objects
    Modifies: nothing
    Effects:  generates a verse one, a verse two, and a chorus, then
              calls printSongLyrics to print the song out.
    """
    verseOne = [generateLyricalSentence(models, 5), generateLyricalSentence(models, 8), generateLyricalSentence(models, 10), generateLyricalSentence(models, 5)]
    verseTwo = [generateLyricalSentence(models, 7), generateLyricalSentence(models, 3), generateLyricalSentence(models, 7), generateLyricalSentence(models, 6)]
    chorus = [generateLyricalSentence(models, 6), generateLyricalSentence(models, 3), generateLyricalSentence(models, 2), generateLyricalSentence(models, 5)]
    printSongLyrics(verseOne, verseTwo, chorus)

def runMusicGenerator(models, songName):
    """
    Requires: models is a list of trained models
    Modifies: nothing
    Effects:  runs the music generator as following the details in the spec.
    """
    key = random.choice(KEY_SIGNATURES.keys())
    part1 = generateMusicalSentence(models, 10, KEY_SIGNATURES[key])
    part2 = generateMusicalSentence(models, 15, KEY_SIGNATURES[key])
    part3 = generateMusicalSentence(models, 25, KEY_SIGNATURES[key])
    part4 = generateMusicalSentence(models, 25, KEY_SIGNATURES[key])
    part5 = generateMusicalSentence(models, 15, KEY_SIGNATURES[key])
    part6 = generateMusicalSentence(models, 10, KEY_SIGNATURES[key])
    tuplesList = [tuple(part1), tuple(part2), tuple(part3), tuple(part4), tuple(part5), tuple(part6)]
    pysynth.make_wav(tuplesList, fn=songName)
    
###############################################################################
# Reach
###############################################################################

PROMPT = """
(1) Generate song lyrics by The Beatles
(2) Generate a song using data from Nintendo Gamecube
(3) Quit the music generator
> """


def main():
    """
    Requires: Nothing
    Modifies: Nothing
    Effects:  This is your main function, which is done for you. It runs the
              entire generator program for both the reach and the core.
              It prompts the user to choose to generate either lyrics or music.
    """
    # FIXME uncomment these lines when ready
    print('Starting program and loading data...')
    lyricsModels = trainLyricModels(LYRICSDIRS)
    musicModels = trainMusicModels(MUSICDIRS)
    print('Data successfully loaded')

    print('Welcome to the ' + TEAM + ' music generator!')
    while True:
        try:
            userInput = int(raw_input(PROMPT))
            if userInput == 1:
                #FIXME uncomment this line when ready
                runLyricsGenerator(lyricsModels)
                #print("Under construction")
            elif userInput == 2:
                # FIXME uncomment these lines when ready
                songName = raw_input('What would you like to name your song? ')
                runMusicGenerator(musicModels, WAVDIR + songName + '.wav')
               # print("Under construction")
            elif userInput == 3:
                print('Thank you for using the ' + TEAM + ' music generator!')
                sys.exit()
            else:
                print("Invalid option!")
        except ValueError:
            print("Please enter a number")

if __name__ == '__main__':
    #FIXME!!!!!
    main()
    # note that if you want to individually test functions from this file,
    # you can comment out main() and call those functions here. Just make
    lyricsModels = trainLyricModels(LYRICSDIRS)
    musicModels = trainMusicModels(MUSICDIRS)

    print lyricsModels
# sure to call main() in your final submission of the project!

