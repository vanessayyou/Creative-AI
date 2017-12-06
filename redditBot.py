import time
import praw
import generate
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

SUBREDDIT = 'MusicAndLyricBotPosts'
TEAMNAME = '**Creative AI, but not creative title.**'
SPOTTED_COMMENTS = []
LYRICSDIRS = generate.LYRICSDIRS
MUSICDIRS = generate.MUSICDIRS
LINK = ''

def comments_spotted():
    with open("comments.txt", 'r') as saved:
        SPOTTED_COMMENTS = saved.read()
        SPOTTED_COMMENTS = SPOTTED_COMMENTS.split('\n')
        return SPOTTED_COMMENTS

def glogin():
    global gauth, drive
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

def upload_music(musicname, i):
    nfile = drive.CreateFile({'key' + str(i) :os.path.basename(musicname)})
    nfile.SetContentFile(musicname)
    nfile.Upload()
    permission = nfile.InsertPermission({
                            'type': 'anyone',
                            'value': 'anyone',
                            'role': 'reader'})
    LINK = str(nfile[u'alternateLink'])
    return LINK
    

def login():
    print("Trying to log in...")
    r = praw.Reddit(username="eecsLyricsGenerator",
                    password="eecs183",
                    client_id="5NnAPqcgsW8Y6w",
                    client_secret="qrkm58TM8HTwvrCfbAmmERM-29I",
                    user_agent="Respond to comments with A.I generated lyrics.")
    print("Logged In.")
    return r


'''
Input is the lyrics that were returned from generate.py
Return formatted lyrics that will be pasted in reddit.
'''
def lyrics(LYRICS):
    ultimatelyrics = ''
    for x in range(0, len(LYRICS)):
        for y in range(0, len(LYRICS[x])):
            for z in range(0, len(LYRICS[x][y])):
                if z == 0:
                    ultimatelyrics = ultimatelyrics + \
                        '    ' + LYRICS[x][y][z].title() + ' '
                else:
                    ultimatelyrics = ultimatelyrics + LYRICS[x][y][z] + ' '
            ultimatelyrics = ultimatelyrics + '\n' + ''
        ultimatelyrics = ultimatelyrics + '\n' + ''
    return ultimatelyrics


def run(r):
    SPOTTED_COMMENTS = comments_spotted()
    print "Going to the subreddit: " + SUBREDDIT
    print "Fetching 100 comments and searching for a lyrics request..."
    for comment in r.subreddit(SUBREDDIT).comments(limit=100):
        if "lyric" in comment.body.lower() and comment.id not in SPOTTED_COMMENTS and comment.author != r.user.me():
            print "User requesting lyrics has been found: " + str(comment.author)
            print "The link for the comment is: " + comment.permalink
            print "Generating lyrics..."
            lyrics_models = generate.trainLyricModels(LYRICSDIRS)
            LYRICS = generate.runLyricsGenerator(lyrics_models)
            ultimatelyrics = lyrics(LYRICS)
            print "Finished generating lyrics."
            comment.reply("Hello " + '*' + str(comment.author) + '*' + ".\n\n" + "I am a bot created by "
                          + TEAMNAME + "\n\n It seems to me that you want to read some awesome artificially \
            generated lyrics, so here you go: \n\n" + ultimatelyrics)
            print "Replied to the comment."
            with open("comments.txt", 'a') as saving:
                saving.write(comment.id + "\n")
        if "music" in (comment.body).lower() and comment.id not in SPOTTED_COMMENTS and comment.author != r.user.me():
            print "User requesting music has been found: " + str(comment.author)
            print "The link for the comment is: " + comment.permalink
            print "Generating music..."
            music_models = generate.trainMusicModels(MUSICDIRS)
            count = 0
            nums = []
            re = open("keys.txt", 'r+')
            for line in re:
                nums.append(line)
            re.write('\n' + str(1+int(nums[-1])))
            MUSICNAME = str("song"+nums[-2]).replace("\n","" + ".wav")
            generate.runMusicGenerator(music_models, MUSICNAME)
            glogin()
            LINK = upload_music(MUSICNAME, 1)
            print "Finished generating and uploading music."
            comment.reply("Hello " + '*' + str(comment.author) + '*' + ".\n\n" + "I am a bot created by "
                          + TEAMNAME + "\n\n It seems to me that you want to listen to some artificial \
                          music we've made just for you, so here you go: \n\n" + LINK)
            print "Replied to the comment."
            with open("comments.txt", 'a') as saving:
                saving.write(comment.id + "\n")
    print "Sleeping for 1 minute"
    time.sleep(60)


r = login()
while True:
    run(r)
