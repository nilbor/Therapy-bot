# import os
# print("Here: ", os.getcwd())
import pdb
import re
import os
import praw
from praw.models import MoreComments
import gpt_2_simple as gpt2
import time
import tarfile
import requests
import json

deltatime=0
previousTime=0
currentTime=0
#https://drive.google.com/file/d/1yQ6DpgYYaPWkruFvLrvg46TxnbXglPxh
filepath="checkpoint_runtherapist.tar"
googefileid= "1yQ6DpgYYaPWkruFvLrvg46TxnbXglPxh"

def extract():
    """Copies the checkpoint folder from a mounted Google Drive."""
    with tarfile.open(filepath, 'r') as tar:
        tar.extractall()
    os.remove(filepath)
    print("File",filepath, "Removed!")

def download_file_from_google_drive(id, destination): 
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def removeFirstLast(text, prefix): #removes first sentence containing prefix and last sentence missing a period 
    text=text.replace(prefix, "") #remove prefix
    text=re.split("",text)
    try: 
        while True: #first sentence
            if text[0]== "!" or text[0]=="." or text[0]=="?": #if one of these characters have been reached, they and the next blank space are removed and the loop is broken
                text.pop(0)
                text.pop(0)
                break
            else: #otherwise the character is just removed
                text.pop(0)
        while True: #last sentence
            if text[-1]== "!" or text[-1]=="." or text[-1]=="?":
                break
            else:
                text.pop()
    except:
        pass
    text="".join(text)
    return text


posts_replied_to=[]
url="https://b0t90n0z02.execute-api.us-east-1.amazonaws.com/redditIdAPIGateway1"
Items=json.loads(json.loads(requests.get(url).text)["body"])
for data in Items:
    posts_replied_to.append(data["id"])


print("Nu laddar vi ned")
download_file_from_google_drive(googefileid,filepath) #download pretrained model from google drive
print("Nu extraktar vi")
extract()
print("Nu kör vi")
print(os.getcwd())
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='runtherapist') #start session and load pretrained model

reddit=praw.Reddit("bot1")
subreddit=reddit.subreddit("therapybot") #specify subreddit

def createText(prefix): 
    textlength=50
    temp=0.8
    text= gpt2.generate(sess, #generate text based on user comment as prefix
        run_name='runtherapist',
        length= textlength,
        temperature=temp,
        # top_k=40,
        prefix=prefix,
        # nsamples=1,
        # batch_size=1,
        return_as_list=True #has to be returned as list to be readable
            )
    text=text[0] #extracts generated text from list
    text=removeFirstLast(text, prefix) #remove first and last sentence
    print(text)
    return text



def post():
    for submission in subreddit.hot(limit=None): #browses through every submission
        print("submission")
        submission.comments.replace_more(limit=None) #enables reading of child comments
        for comment in submission.comments.list():
            if comment.id not in posts_replied_to: #if the post hasnt been replied to already  
                newcomment=comment.reply(createText(comment.body)) #generate text and reply
                posts_replied_to.append(comment.id)
                print(newcomment.id)
                posts_replied_to.append(newcomment.id) #add both the comment replied to and the reply to comments to avoid
                posted=True
                break
        else:
            continue
        break    
    for post_id in posts_replied_to:
        requests.post(url+"?id="+post_id)

def submit(): #submits a daily post to leave comments on
    title="Daily post"
    selftext="Leave a comment on this post to receive an answer from Therapy-Bot!"
    subreddit.submit(title, selftext)

while True:
    print("Posted")
    currentTime=time.time()
    deltatime=currentTime-previousTime
    if deltatime<60*60*24: #if 24 hours has passed since last post
        post()
    else: #otherwise check for comments to reply to
        submit()
        previousTime=currentTime
    time.sleep(5*60) #wait 5 minutes to not make too many requests to reddit
    