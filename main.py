import websocket, json, pyminizip
import _thread as thread
bankpin = "pushbullet 액세스 토큰"


def on_message(ws, message):
    obj = json.loads(message)
    if obj["type"] == "push":
        push = obj["push"]

        try:
            title = push["title"]
            if "출금" in title or "송금" in title:
                return
        except:
            pass
        body = push["body"].replace("\n"," ")
        appname = push["package_name"]

        if appname == "com.IBK.SmartPush.app":
            sp = body.split(" ")
            displayname = sp[2]
            amount = int(sp[1].replace("원", "").replace(",",""))
            print(f"{displayname}이 {amount} 입금")

        elif appname == "com.nh.mobilenoti":
            displayname = message[5]
            amount = int(message[1].replace("입금", "").replace("원", "").replace(",",""))
            print(f"{displayname}이 {amount} 입금")

        elif appname == "com.wooribank.smart.npib":
            sp = body.split(" ")
            displayname = sp[1]
            amount = int(sp[5].replace("원", "").replace(",",""))
            print(f"{displayname}이 {amount} 입금")

        elif appname == "com.kakaobank.channel":
            sp = body.split(" ")
            displayname = sp[5]
            amount = int(sp[4].replace(",", "").replace("원", ""))
            print(f"{displayname}이 {amount} 입금")

        elif appname == "com.kbstar.reboot":
            sp = body.split(' ')
            displayname = sp[0].replace('님이', '')
            amount = int(sp[1].replace('원을', '').replace(',', ''))
            print(f"{displayname}이 {amount} 입금")

        else:
            print("등록되지 않은 은행")
            return

def on_error(ws, error):
    print("error:",error)

def on_close(ws):
    print("Closed")

def on_open(ws):
    print("Opened")
    

if __name__ == "__main__":
    #websocket.enableTrace(True)
    
    ws = websocket.WebSocketApp("wss://stream.pushbullet.com/websocket/"+bankpin,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
    
