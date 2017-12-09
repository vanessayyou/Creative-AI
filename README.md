# Creative AI Project

**Creative AI** is about using artificial intelligence to automatically generate lyrics and music using datasets of your choice.

Welcome to the repository! If you have questions, please check here:

- <a href="https://youtu.be/Z46LvHwgygs?list=PL2BYDiR6uDOJzYCJ7QuuQz-hWvQeYN5Nx" target="_blank">Link to generated lyrics demo</a>

- <a href="https://youtu.be/RrHrRqZ3pUM?list=PL2BYDiR6uDOJzYCJ7QuuQz-hWvQeYN5Nx" target="_blank">Link to generated music demo</a>

- <a href="https://github.com/eecs183/creative-ai/wiki" target="_blank">Link to specification</a>

Here are a few notes to get you started:

* Don't touch the __init__.py files. These are necessary to your project.

* Things will be easier if you read the spec first and follow the given function order.

* Make sure you have ```pip``` installed so you download pysynth.

* Remember to update this file to describe your finished Final Project.

Have fun on the project!
  
## Reach: 
### 1. Reddit Bot  
**Welcome to RedditBot:**  
This is a bot that will reply to any comment exactly once on a certain Reddit Thread if it contains the words
"music" or "lyric", regardless of letter case. The following is the thread in question:  
- <a href="https://www.reddit.com/r/MusicAndLyricBotPosts/comments/7i1yuw/demonstrational_post/" target="_blank">Link to the demonstrational post in our subreddit.</a>    
* If the comment contains "lyrics", the bot will reply with some artifically generated lyrics.  
* If the comment contains "music", the bot will, right then and there, generate some music, access its own
google drive, upload its music and reply with a link to the song on google drive!  
  
In order for this program to work however, there are a few things that must be kept in the same folder.
The following files must be kept in the same folder:
- The python files RedditBot.py and generate.py
- The text files "keys.txt" (which stores the unique names for each song uploaded) and "comments.txt" 
(which is a log of the comments RedditBot has already replied to so it doesn't reply more than once to
the same comment), 
- "credentials.json" and "settings.yaml" which MUST NOT
BE TOUCHED as they contain the access keys to RedditBot's own google account.
- Also, in order for the program to work, pydrive must be pip-installed for python 2.7.
