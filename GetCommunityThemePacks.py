#GLOBALS####################################
client=None
community_id=None
#LIBS#######################################
import aiohttp
import asyncio
import aminofix as amino
import json
from time import sleep
import time
import shutil
import requests
import os


def CURRENT_DATE():
    return time.strftime("%Y-%m-%d")
def CURRENT_TIME():
    return time.strftime("%Y-%m-%dT%H:%M:%S")
print(f"CURRENT_TIME={CURRENT_TIME()}")
email=input("email/phone number>>>")
password=input("password>>>")
community_link=input("community link>>>")

async def fun_1():
    community_info=(await client.get_community_info(comId=community_id)).json
    themePackUrl=community_info['themePack']['themePackUrl']
    n=themePackUrl.rfind('/')+1
    destination = themePackUrl[n:]
    url = themePackUrl[:n]
    l=destination.find('rev')+3
    r=destination.find('.')
    themeCount=int(destination[l:r])
    print(f"{community_id}.{community_info['themePack']['themeColor']}.{themePackUrl}.{themeCount}")
    path=f"{community_id}.{(community_info['link'])[community_info['link'].rfind('/')+1:]}"
    os.mkdir(path)
    for i in range(themeCount):
        filename=destination.replace(str(themeCount),str(i+1))
        filereq = requests.get(f"{url}{filename}",stream = True)
        with open(f"{path}//{filename}","wb") as receive:
            shutil.copyfileobj(filereq.raw,receive)
        del filereq
        print(f"{url}{filename} downloaded.")

async def fun_2():
    pass

async def get_community_id(link):
    community_info=await amino.asyncfix.Client().get_from_code(code=link)
    id=community_info.path[1:community_info.path.index('/')]
    print(f"community_id={id}")
    return id

async def get_object_id(link):
    id=(await amino.asyncfix.Client().get_from_code(code=link)).objectId
    print(f"chat_id={id}")
    return id

async def main():
    global client, sub_client, community_id
    client=amino.asyncfix.Client()
    if '+' in email: await client.login_phone(phoneNumber=email, password=password)
    else: await client.login(email=email, password=password)
    print("Successfully logined.")
    community_info=await client.get_from_code(code=community_link)
    community_id=community_info.path[1:community_info.path.index('/')]
    ch=int(input("1-Download themes\n2-Nothing\n>"))
    if ch==1:
        await fun_1()
    elif ch==2:
        await fun_2()
    
    
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
