import tweepy
import json
from pprint import pprint
import sys
import io

if __name__=='__main__':
    encoding='UTF-8'
    archivo_datos=io.open("menciones_alejo_url.txt","w",encoding=encoding)
    archivo_celebridades=io.open("celebridades_alejo.txt",'w',encoding=encoding)

    consumer_key = ""
    consumer_secret = ""
    access_key =""
    access_secret =""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    #Esto hara que no me aparezca el error 429 y que el codigo respete la velocidad con que trae los datos de twitter(segun)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    api = tweepy.API(auth)
    #El user_timeline es el del usuario
    #creation=""
    query="@alejoeder"
    lista_url=[]
    indice=0
    can=0
    suma_seg=0
    pprint(len(lista_url))
    for status in tweepy.Cursor(api.search,q=query,geo="geocode",tweet_mode='extended').items():
        #pprint(status._json)
        hashtags=""
        mentions=""
        likes=0
        retweet=0
        creado=status._json["created_at"]
        if "retweeted_status" in status._json:
            yn="retweet"
            #Se sacan los hashtags
            if len(status._json["retweeted_status"]["entities"]["hashtags"])>0:
                for i in status._json["retweeted_status"]["entities"]["hashtags"]:
                    hashtags+="{}/".format(i["text"])

            #Se sacan las menciones
            if len(status._json["retweeted_status"]["entities"]["user_mentions"])>0:
                for i in status._json["retweeted_status"]["entities"]["user_mentions"]:
                    mentions+="{}/".format(i["screen_name"])
            twit=status._json["retweeted_status"]["full_text"]
            a=twit
            user=status._json["retweeted_status"]["user"]["name"]
            twit2=a.find('\n')
            twit2=a.find('\n')
            if twit2==-1:
                pass
            else:
                while True:
                    b=a.find('\n')
                    if b==-1:
                        break
                    else:
                        a=a[:b]
                        a+=a[b+1:]
                pass
            #a=a.encode(sys.stdout.encoding, errors='replace')
            a=a.encode('UTF-8',errors = 'ignore')
            likes=status._json["retweeted_status"]["favorite_count"]
            retweet=status._json["retweeted_status"]["retweet_count"]
            usuario=status._json["retweeted_status"]["user"]["name"]
            #if "urls" in status._json["retweeted_status"]["entities"]:
                #for url in status._json["retweeted_status"]["entities"]["urls"]:
                    #if "url" in url:
                        #url2=url["url"]

        else:
            yn="propio"
            if len(status._json["entities"]["hashtags"])>0:
                for i in status._json["entities"]["hashtags"]:
                    hashtags+="{}/".format(i["text"])
                #hashtags = hashtags.rstrip('\n')
            if len(status._json["entities"]["user_mentions"])>0:
                for i in status._json["entities"]["user_mentions"]:
                    mentions+="{}/".format(i["screen_name"])
                #mentions = mentions.rstrip('\n')
            likes=status._json["favorite_count"]
            retweet=status._json["retweet_count"]
            twit=status._json["full_text"]
            a=twit
            user=status._json["user"]["name"]
            #user=user.encode('UTF-8',errors='ignore')

            twit2=a.find('\n')
            if twit2==-1:
                pass
            else:
                while True:
                    b=a.find('\n')
                    if b==-1:
                        break
                    else:
                        a=a[:b]
                        a+=a[b+1:]
                pass
            #if "extended_entities" in status._json:
                #for url in status._json["extended_entities"]["media"]:
                    #if "url" in url:
                        #url2=url["url"]
                        #pprint(url2)

            #print(twit2)
            #print(a)
            a=a.encode('UTF-8',errors = 'ignore')
        if len(hashtags)==0:
            hashtags="No tuvo hashtags este twit"
        if len(mentions)==0:
            mentions="No tuvo mentions este twit"
        #a=u"{}".format(a)
        #a=unicode(a,"uft-8")
        b=a.decode('utf8')
        suma_seg+=status._json['user']['followers_count']
        #print(b)
        #pprint(status._json)
        #ce=celebridad
        if status._json['user']["followers_count"]>10000:
            ce_user=status._json['user']["name"]
            ce_id=status._json['user']["screen_name"]
            ce_can_followers=status._json["user"]["followers_count"]
            archivo_celebridades.write("{}|{}|{}|{}|{}\n".format(ce_user,yn,ce_id,ce_can_followers,b))
        #var=lista_url[indice]
        archivo_datos.write("{}|{}|{}|{}|{}|{}|{}|{}\n".format(creado,user,yn,b,hashtags,mentions,likes,retweet))
        can+=1
    archivo_datos.close()
    archivo_celebridades.close()
    promedio_seg=suma_seg//can
    promedio_ce=io.open("promedio_seguidores_menciones_alejo.txt",'w',encoding=encoding)
    promedio_ce.write("cantidad seguidores= {} , suma para promedio = {}\n".format(can,suma_seg))
    promedio_ce.write("{}".format(promedio_seg))
    promedio_ce.close()
