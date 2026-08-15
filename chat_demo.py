import requests
import os 

api_key = os.getenv('ZHIPU_API_KEY')
if not api_key:
    raise SystemExit('没有设置环境变量')
url = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
duihua = input('请提出问题:')

headers = {
    'content-Type':'application/json',
    'Authorization':f'Bearer {api_key}'
}

body = {
    'model':'glm-4-flash',
    'messages':[
        {'role':'user','content':duihua}
    ],
    'temperature':0.6,
    'stream':False
}

try:
    resp = requests.post(url,headers=headers,json=body,timeout=30)
    resp.raise_for_status()
    res = resp.json()
    answer = res['choices'][0]['message']['content']
    print('AI回答:')
    print(answer)

except requests.exceptions.RequestException as e:
    print('请求出错: ',e)