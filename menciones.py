import tweepy
import json
from pprint import pprint
import sys
import io
if __name__=='__main__':
    encoding='UTF-8'
    archivo_datos=io.open("alejo_urls.txt","w",encoding=encoding)

    #consumer_key,consumer_secret,access_key, access_secret son entregadas por twitter cuando le queremos hacer sus respectivos analisis a los datos.
    consumer_key = ""
    consumer_secret = ""
    access_key = ""
    access_secret =""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    #El user_timeline es    el del usuario
    lista_url=[]
    for status in tweepy.Cursor(api.user_timeline,id="alejoeder",tweet_mode='extended_entities').items():
        #Descomentar la siguiente linea si se desea ver el conetnido del json
        #pprint(status._json)
        if "retweeted_status" in status._json:
            if len(status._json["retweeted_status"]["entities"]["urls"])>0:
                for url in status._json["retweeted_status"]["entities"]["urls"]:
                    if "url" in url:
                        #print("imprimiendo una")

                        lista_url.append(url["url"])
                        break
                #pprint(status._json)
            else:
                if "media" in status._json["retweeted_status"]["entities"]:
                    for url in status._json["retweeted_status"]["entities"]["media"]:
                        if "url" in url:
                            #print("imprimiendo 2")
                            lista_url.append(url["url"])
                            break
                else:
                    lista_url.append("No aparece el url")

        else:
            if len(status._json["entities"]["urls"])>0:
                if "urls" in status._json["entities"]:
                    for url in status._json["entities"]["urls"]:
                        if "url" in url:
                            lista_url.append(url["url"])

                            break
                else:
                    lista_url.append("No aparece url")
            else:
                lista_url.append("No aparece url")

    print(len(lista_url))
    indice=0
    for status in tweepy.Cursor(api.user_timeline,id="alejoeder",tweet_mode='extended').items(len(lista_url)):
        #pprint(status._json)
        hashtags=""
        mentions=""
        url2="Este twit no tiene url"
        likes=0
        retweet=0
        creado=status._json["created_at"]
        if "retweeted_status" in status._json:
            #pprint(status._json)
            yn="retweet"
            if len(status._json["retweeted_status"]["entities"]["hashtags"])>0:
                for i in status._json["retweeted_status"]["entities"]["hashtags"]:
                    hashtags+="{}/".format(i["text"])
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
            #usuario=usuario.encode('UTF-8',errors='ignore')
            #user=user.encode('UTF-8',errors='ignore')
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

            #if "extended_entities" in status._json:
                #for url in status._json["extended_entities"]["media"]:
                    #if "url" in url:
                        #pprint(url2)
                        #url2=url["url"]
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
        #print(b)
        var=lista_url[indice]
        #print(var)
        #pprint(status._json)
        #id=status._json["id"]
        #archivo_datos.write("{}\n".format(id))
        archivo_datos.write("{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(creado,user,yn,b,hashtags,mentions,likes,retweet,var))
        indice+=1

    archivo_datos.close()
