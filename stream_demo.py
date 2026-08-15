import requests
import json
import os
ai_key = os.getenv('ZHIPU_API_KEY')
if not ai_key:
    raise SystemExit('没有找到环境变量')
url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

headers = {
    'content-Type':'application/json',
    'Authorization':f'Bearer {ai_key}'
}

body ={
    'model':'glm-4-flash',
    'messages':[
        {'role':'user','content':'简单介绍一下ＲＡＧ'}
    ],
    'temperature':0.6,
    'stream':True
}

try:
    resp = requests.post(url,headers=headers,json=body,stream=True,timeout=60)

    resp.raise_for_status()

    print('AI:',end='')
    for line in resp.iter_lines():
        if not line:
            continue
        text = line.decode('utf-8')
        if text.startswith('data: '):
            chunk_str = text[6:]
            if chunk_str == '[DONE]':
                break
            chunk = json.loads(chunk_str)
            delta = chunk['choices'][0]['delta']
            if delta.get('content'):
                print(delta['content'],end='',flush=True)
    print('\n')
except requests.exceptions.RequestException as e:
    print('\n出错: ',e)