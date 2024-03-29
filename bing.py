# 如需使用代理功能请取消注释并按需要修改
#import os
#os.environ["http_proxy"] = "http://127.0.0.1:8080"
#os.environ["https_proxy"] = "http://127.0.0.1:8080"

import traceback
import asyncio
from EdgeGPT import Chatbot, ConversationStyle
from fastapi import FastAPI, Body
import uvicorn

app = FastAPI()

# 参数设置
conversation_style = ConversationStyle.balanced  # 可选择creative,balanced,precise
wss_link = "wss://sydney.bing.com/sydney/ChatHub"

# 手动配置时按需要修改监听地址和端口
HOST = "0.0.0.0"
PORT = 8007

# 手动配置时按需要修改cookie文件路径，将./cookie.json修改为你自己的文件位置（一般不用修改）
chatbot = Chatbot(cookie_path='./cookie.json')
# 直接传参 (Pass in the cookies directly)
#import json
#with open('cookie.json', 'r') as cookie_file:
#    cookie_data = json.load(cookie_file)
#    print(cookie_data)
#chatbot = Chatbot(cookies=cookie_data)

flag = False


@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.post("/bing")
async def chatGPT(body: dict = Body(...)):
    global flag, conversation_style, wss_link
    prompt = body["prompt"]
    print("User: " + prompt)

    if flag:
        return {"message": "接口繁忙，请稍后再试。"}

    try:
        flag = True
        if prompt == "!reset":
            await chatbot.reset()
            print("OK")
            flag = False
            return {"message": "OK"}
        if prompt == "!creative":
            conversation_style = ConversationStyle.creative
            await chatbot.reset()
            print("Creative")
            flag = False
            return {"message": "Creative"}
        if prompt == "!balanced":
            conversation_style = ConversationStyle.balanced
            await chatbot.reset()
            print("Balanced")
            flag = False
            return {"message": "Balanced"}
        if prompt == "!precise":
            conversation_style = ConversationStyle.precise
            await chatbot.reset()
            print("Precise")
            flag = False
            return {"message": "Precise"}
        answer = (await chatbot.ask(prompt, conversation_style, wss_link))["item"]["messages"][1]["adaptiveCards"][0]["body"][0]["text"]
        print("Bingbot: " + answer)
    except:
        traceback.print_exc()
        await chatbot.reset()
        answer = "ERROR"
        pass
    flag = False
    return {"message": answer}

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
