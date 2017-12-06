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





#REACH
from pydub import AudioSegment


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
    #selects word based off model and current sentence
    currentWord = selectNGramModel(models, sentence)
    #gets the next word to be appended to the list
    token = currentWord.getNextToken(sentence)
    while (not sentenceTooLong(desiredLength, len(sentence)-2)) and ( token != '$:::$'):
        sentence.insert(len(sentence), token)
        currentWord = selectNGramModel(models, sentence)
        token = currentWord.getNextToken(sentence)
    return sentence[2:len(sentence)]


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
    note = currentNote.getNextNote(sentence, possiblePitches)
    while (not sentenceTooLong(desiredLength, len(sentence)-2)) and ( note != '$:::$'):
        sentence.insert(len(sentence), note)
        currentNote = selectNGramModel(models, sentence)
        note = currentNote.getNextNote(sentence, possiblePitches)
    return sentence[2:len(sentence)]


def runLyricsGenerator(models):
    """
    Requires: models is a list of a trained nGramModel child class objects
    Modifies: nothing
    Effects:  generates a verse one, a verse two, and a chorus, then
              calls printSongLyrics to print the song out.
    """
    verseOne = [generateLyricalSentence(models, 10),
                generateLyricalSentence(models, 8),
                generateLyricalSentence(models, 10),
                generateLyricalSentence(models, 9)]
    verseTwo = [generateLyricalSentence(models, 7),
                generateLyricalSentence(models, 7),
                generateLyricalSentence(models, 7),
                generateLyricalSentence(models, 10)]
    chorus = [generateLyricalSentence(models, 9),
              generateLyricalSentence(models, 15),
              generateLyricalSentence(models, 13),
              generateLyricalSentence(models, 9)]
    verses = [verseOne, chorus, verseTwo, chorus]
    printSongLyrics(verseOne, verseTwo, chorus)
    return(verses)

def runMusicGenerator(models, songName):
    """
    Requires: models is a list of trained models
    Modifies: nothing
    Effects:  runs the music generator as following the details in the spec.
    """
    key = random.choice(KEY_SIGNATURES.keys())
    #tuplesList = generateMusicalSentence(models, 90, KEY_SIGNATURES[key])
    tuplesList = generateMusicalSentence(models, 60, KEY_SIGNATURES[key])

    pysynth.make_wav(tuplesList, fn=songName)

    #reach
    background_tuples_list = generateMusicalSentence(models, 4, KEY_SIGNATURES['c major'])
    length_background_tuples_list = len(background_tuples_list)
    #FIXME
    #print background_tuples_list

    background1 = []
    for x in range(0, 60):

        if length_background_tuples_list == 1:
            background1.append(background_tuples_list[0])
        elif length_background_tuples_list == 2:
            if (x + 1) % 4 == 1:
                background1.append(background_tuples_list[0])
            elif (x + 1) % 4 == 2:
                background1.append(background_tuples_list[1])
        elif length_background_tuples_list == 3:
            if (x + 1) % 4 == 1:
                background1.append(background_tuples_list[0])
            elif (x + 1) % 4 == 2:
                background1.append(background_tuples_list[1])
            elif (x + 1) % 4 == 3:
                background1.append(background_tuples_list[2])
        else:
            if (x + 1) % 4 == 1:
                background1.append(background_tuples_list[0])
            elif (x + 1) % 4 == 2:
                background1.append(background_tuples_list[1])
            elif (x + 1) % 4 == 3:
                background1.append(background_tuples_list[2])
            else:
                background1.append(background_tuples_list[3])

    pysynth.make_wav(background1, fn=WAVDIR + 'background1.wav')


    background_tuples_list = generateMusicalSentence(models, 4, KEY_SIGNATURES['e major'])
    length_background_tuples_list = len(background_tuples_list)
    #FIXME
    #print background_tuples_list

    background2 = []
    for x in range(0, 60):
        if length_background_tuples_list == 1:
            background2.append(background_tuples_list[0])
        elif length_background_tuples_list == 2:
            if (x + 1) % 4 == 1:
                background2.append(background_tuples_list[0])
            elif (x + 1) % 4 == 2:
                background2.append(background_tuples_list[1])
        elif length_background_tuples_list == 3:
            if (x + 1) % 4 == 1:
                background2.append(background_tuples_list[0])
            elif (x + 1) % 4 == 2:
                background2.append(background_tuples_list[1])
            elif (x + 1) % 4 == 3:
                background2.append(background_tuples_list[2])
        else:
            if (x + 1) % 4 == 1:
                background2.append(background_tuples_list[0])
            elif (x + 1) % 4 == 2:
                background2.append(background_tuples_list[1])
            elif (x + 1) % 4 == 3:
                background2.append(background_tuples_list[2])
            else:
                background2.append(background_tuples_list[3])




    pysynth.make_wav(background2, fn=WAVDIR + 'background2.wav')

    sound1 = AudioSegment.from_file(WAVDIR + "background1.wav")
    sound2 = AudioSegment.from_file(WAVDIR + "background2.wav")
    sound3 = AudioSegment.from_file(songName)

    combined1 = sound1.overlay(sound2)

    combined1.export(WAVDIR + "combined1.wav", format='wav')

    combined2 = combined1.overlay(sound3)
    os.remove("wav/combined1.wav")
    os.remove("wav/background2.wav")
    os.remove("wav/background1.wav")

    combined2.export(songName, format='wav')

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
    print('Starting program and loading data...')
    lyricsModels = trainLyricModels(LYRICSDIRS)
    musicModels = trainMusicModels(MUSICDIRS)
    print('Data successfully loaded')

    print('Welcome to the ' + TEAM + ' music generator!')
    while True:
        try:
            userInput = int(raw_input(PROMPT))
            if userInput == 1:
                runLyricsGenerator(lyricsModels)
            elif userInput == 2:
                songName = raw_input('What would you like to name your song? ')
                runMusicGenerator(musicModels, WAVDIR + songName + '.wav')
            elif userInput == 3:
                print('Thank you for using the ' + TEAM + ' music generator!')
                sys.exit()
            else:
                print("Invalid option!")
        except ValueError:
            print("Please enter a number")


if __name__ == '__main__':
    main()
    # note that if you want to individually test functions from this file,
    # you can comment out main() and call those functions here. Just make
    #lyricsModels = trainLyricModels(LYRICSDIRS)
   #musicModels = trainMusicModels(MUSICDIRS)

    #runMusicGenerator(musicModels, WAVDIR + '1' + '.wav')
# sure to call main() in your final submission of the project!

