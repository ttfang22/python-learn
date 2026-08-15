import requests
import json
import os 

api_key = os.getenv('ZHIPU_API_KEY')
if not api_key:
    raise SystemExit('没有找到环境变量')
url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

headers = {
    'Content-Type':'application/json',
    'Authorization':f'Bearer {api_key}'
}

messages = []

while True:
    user_input = input('\n请输入: ')

    if user_input.strip() == '88':
        break
    messages.append({'role':'user','content':user_input})

    body = {
        'model': 'glm-4-flash',
        'messages': messages,
        'temperature': 0.6,
        'stream': True
    }

    try:
        resp = requests.post(url,headers=headers,json=body,stream=True,timeout=60)
        resp.raise_for_status()

        print('AI: ',end='')
        full_answer = '' 

        for line in resp.iter_lines():
            if not line:
                continue
            text = line.decode('utf-8')
            # print(f"DEBUG text=[{text}]") #新增調試
            if text.startswith('data: '):
                chunk_str = text[6:]
                # print(f"DEBUG chunk_str=[{chunk_str}]") #打印切片后的字符串
                if chunk_str == '[DONE]':
                    break
                chunk = json.loads(chunk_str)

                delta = chunk['choices'][0]['delta']
                # print(f"DEBUG delta={delta}") #打印delta
                if delta.get('content'):
                    txt = delta['content']
                    print(txt,end='',flush=True)
                    full_answer += txt
        print() 
        messages.append({'role':'assistant','content':full_answer})

    except requests.exceptions.RequestException as e:
        print(f'\n请求出错:{e}')