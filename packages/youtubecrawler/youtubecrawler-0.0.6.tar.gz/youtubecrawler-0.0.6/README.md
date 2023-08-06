


## YouTubeCrawle Wrapper for python



# readable and good Docs at https://github.com/KeinShin/youtubecrawler


- Install Using pip
``` 
pip3 install youtubecrawler

```


# Documentation

> Initialize Wrapper

```
from youtubecrawler import crawl



yt=crawl(video_name="xyz)

```

**You can also use**

```

yt=crawl(video_link=link)

yt=crawl(video_id=video_id)

```

Wrapper Is Capable of 

**For Video**

> Getting Video Views
> Getting video tags
> Getting Video Description
> Getting Video Title
> Getting Likes and Dislikes
> Getting Upload Time
> Getting Uploader Information

**For channels**
Can Scrape Any info about the channel
__Like__
> Last Date Joined
> Latest Video Details
> Latest Community Post
> Channel Description
> Info about other channels of the video
> Subs of the channel ( by name)

## Videos

**Gather everything in a single call**

```
video=yt.VideoDetails()
```

__Gather Info Separately__

**Get Views of the video**

```

veiws=yt.veiws()

```

**Get tags of the video**

```
tags=yt.keyword()
```

**Get video link**

```
link=yt.videolink()
```

**Likes and dislikes of the video**

```
likes=yt.likes_dislikes()[1]
dislikes=yt.likes_dislikes()[2]
```

**Get Upload time**

```
uploadtime=yt.videoUploadTime()
```

**Get Video Title**

```
title=yt.VidTitle()
```

**Get video description**


```
description=yt.description()
```


**Get Uploader Information**

```

uploader=yt.channel()
```


**Get Video Views**

```
views=yt.views()
```


**Get Video Link**

```
videolink=yt.videolink()

```

## Channels

```
from youtubecrawler.channel import channel

ch=channel(channelname="CarryMinati")

```

Other parameters
```
> ch = channel(channellink=channellink)
> ch = channel(channelid='/channel/UC0IWRLai-BAwci_e9MylNGw')
```

**Get Subs of the channel**
__Use full with name__

```
subs=ch.subs()
```

**Get Latest Video**

```
subs=ch.latest_video()
```

**Get Latest Community Post**

```
post=ch.latest_community()
```

**Get That user other channels**
```
otherchannels=ch.spareChannels()
```

**Get links of about**

```
aboutlinks=ch.links()
```



