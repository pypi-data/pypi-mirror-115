from bs4 import BeautifulSoup
import requests
import moviepy.editor  as  mp
from requests_html import HTMLSession 
import os
import urllib.request
import re
from urllib.request import urlopen,Request
from lxml import etree
from requests.api import head

import pytube  
from pytube import YouTube  

class crawl:
    def __init__(self,video_name:str="",video_id:str="",output: str = "",video_link:str=''):
        self.name = video_name
        
        self.id = video_id
        self.out= output
        self.link = video_link
        if not self.name:
            if not self.id:
              if not self.link:
                raise ValueError("Provide Video Name Or Video Link or video id, Please.")
        if self.link:
            self.link=self.link
        elif self.id:
            self.link="https://www.youtube.com/watch?v=" + self.id
        elif self.name:        
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+ self.name)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            self.vidid=video_ids[0]
            self.link="https://www.youtube.com/watch?v=" + self.vidid
        self.link2=self.link
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent':user_agent} 
        self.link=self.link2
        session = HTMLSession()
        response = session.get(self.link2)
        response.html.render(sleep=1)
        self.soup = BeautifulSoup(response.html.html, "html.parser") 
    
    def keyword(self):
            
        self.title = self.soup.find("meta",attrs={"name":"keywords"})
        
        return self.title["content"]
        
    def videolink(self):
        return self.vidid
    
    def VideoDetails(self):

        likes=self.likes_dislikes()[1]
        dislikes=self.likes_dislikes()[2]
        if dislikes == "Dislike":
            dislikes= "N/A"
        title=self.upload_time_and_title()[0]
        upload=self.upload_time_and_title()[1]
        params = {
         "Video Title": title,
         "Video Id" : self.videolink().split("/")[-1], 
         "Description": self.description(),
         "Veiws": self.veiws(),
         "Likes": likes,
         "Dislikes": dislikes,
         "Upload Time": upload,
         "Video Link":self.videolink(),
         "Channel" : self.channel()
        }
        return params
        
    def likes_dislikes(self):
        session = HTMLSession()
        response = session.get(self.link2)
        response.html.render(sleep=1)
        soup = BeautifulSoup(response.html.html, "html.parser")
        likes_dislikes=[]
        for i in soup.find_all("yt-formatted-string",{"id":"text"}):
            likes_dislikes.append(i.get_text())
        return likes_dislikes
    
    def upload_time_and_title(self):
        det=[]
        title=self.soup.find_all("yt-formatted-string",{"class":"style-scope ytd-video-primary-info-renderer"})
        for i in title:
            det.append(i.get_text())
        return det

    def VidTitle(self):
        return self.upload_time_and_title()[0]

    def videoUploadTime(self):
        return self.upload_time_and_title()[1]
        

    def description(self):
        descrip=''
        for i in self.soup.find_all("span",{"class":"style-scope yt-formatted-string"}):
            descrip+=i.get_text()
        return descrip
    
    def channel(self):
        channelinfo={}
        name=self.soup.find("yt-formatted-string", {"class": "ytd-channel-name"})
        tg=name
        name=name.find("a").text
        channelink=self.soup.find("a",{"class":"yt-simple-endpoint style-scope ytd-video-owner-renderer"})
        channelink=channelink.get("href")
        subs=self.soup.find("yt-formatted-string",{"id":"owner-sub-count"})
        subs=subs.get_text()
        channelinfo.update({"name":name,"channel_link":"https://www.youtube.com"+ channelink,
        "subscriber": subs                
        })
        return channelinfo
    
    def download(self,to_mp3:bool=False,mp3name:str=''):
        
  
        youtube = pytube.YouTube(self.link)  
        video = youtube.streams.first()  
        video.download(self.out)   
                
    def veiws(self):
        veiws=self.soup.find("span",{"class":"view-count style-scope ytd-video-view-count-renderer"})
        return veiws.text
    
    def videolink(self):
      ida=self.soup.find("link",{"rel":"shortlinkUrl"})
      return ida.get("href")

