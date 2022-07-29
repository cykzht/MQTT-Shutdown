from msilib.schema import Icon
import paho.mqtt.client as mqtt
import os
import pyautogui
import sys
HOST = "bemfa.com"
PORT = 9501

def read_config():
    if(os.path.exists('config.ini')):
        f = open('config.ini', 'r')
        file = f.readlines()
        f.close()
        if(f!='' and len(file)==2):
            global client_id
            global topic
            client_id = file[0][:-1]
            topic = file[1]
            return 1
        else:
            return 0
    else:
        return 0

def writ_config():
    while(1):
        a = pyautogui.prompt(text='请输入巴法云私钥：', title='巴法云私钥')
        if a is None:
            sys.exit(0)
        elif(a!=''):
            break
        else:
            pyautogui.alert('请输入私钥！')
            continue   
    while(1):
        b = pyautogui.prompt(text='请输入MQTT主题：', title='MQTT主题')
        if a is None:
            sys.exit(0)
        elif(a!=''):
            break
        else:
            pyautogui.alert('请输入主题！')
            continue
    with open('config.ini', 'w') as f:
        f.truncate()
        f.write(a+'\n')
        f.write(b)

#连接并订阅
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)         # 订阅消息

#消息接收
def on_message(client, userdata, msg):
    mesg = str(msg.payload.decode('utf-8'))
    print("主题:"+msg.topic+" 消息:"+mesg)
    if(mesg=='off'):
        os.system('shutdown -s -t 0')

#订阅成功
def on_subscribe(client, userdata, mid, granted_qos):
    print("On Subscribed: qos = %d" % granted_qos)

# 失去连接
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection %s" % rc)
        pyautogui.alert('连接错误，请重新运行程序！')
        with open('config.ini', 'w') as f:
            f.truncate()
        sys.exit(0)

while(1):
    if(read_config()):
        break
    else:
        writ_config()
client = mqtt.Client(client_id)
client.username_pw_set("userName", "passwd")
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_disconnect = on_disconnect
client.connect(HOST, PORT, 60)
client.loop_forever()
