import requests
import json
import asyncio
import logging
from openai import OpenAI
from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from datetime import datetime
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
import pickle
import subprocess

### Model database ###
model_gpt35 = 'openai/gpt-3.5-turbo'
model_gpt4 = 'openai/gpt-4-1106-preview'
model_noromaid = 'neversleep/noromaid-20b'
model_openchat = 'openchat/openchat-7b:free'
model_mythomist = 'gryphe/mythomist-7b:free'
model_mythomax = 'gryphe/mythomax-l2-13b'
model_nousllama13 = 'nousresearch/nous-hermes-llama2-13b'


def getUserFile():
  file = open('users.sf.gds', 'rb')
  all_users_list = pickle.load(file)
  return all_users_list


def closeAndOpenUserFile(all_user_list):
   file = open('users.sf.gds', 'wb')
   pickle.dump(all_user_list, file)
   file = open('users.sf.gds', 'rb')
   all_users_list = pickle.load(file)
   return all_users_list


def findUser(id, userlist):
   for i in userlist:
      if i[0] == id:
         return i
      else:
         pass
   return False


def sendRequestOpenAI(text, model):
  client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
  )

  completion = client.chat.completions.create(
    extra_headers={
    },
    model=model,
    messages=[
      {
        "role": "user",
        "content": text,
      },
    ],
      )
  # print(completion)
  # print(completion.id)
  tmtext = 'https://openrouter.ai/api/v1/generation?id='
  tmtext += completion.id
  spheaders = { "Authorization" : f"Bearer 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" }
  resp = requests.get(url=tmtext, headers=spheaders)
  resp1 = resp.json()
  # print(resp1)
  return completion.choices[0].message.content


def sendRequest(text, model, userlist, id):
  user = findUser(id, userlist)
  usercontext = user[4]
  template_user = {'role': 'user', 'content': 'placeholder'}
  newresp = template_user
  newresp['content'] = text
  if len(usercontext) < 5:
     usercontext.append(newresp)
  else:
     usercontext.pop(0)
     usercontext.append(newresp)
  usercontext.append(newresp)
  print(usercontext)
  response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
      "Authorization": f"Bearer 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",
      "HTTP-Referer": f"telegram.org", # Optional, for including your app on openrouter.ai rankings.
      "X-Title": f"AS1MOV", # Optional. Shows in rankings on openrouter.ai.
    },
    data = json.dumps({
      "model": model,
      "messages": usercontext,
    })
  )
  resp_dict = response.json()
  op = 'RESPONSE: '
  temptext = "https://openrouter.ai/api/v1/generation?id="
  temptext += resp_dict["id"]
  a1 = requests.get(url=temptext, headers={'Authorization': f'Bearer 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'})
  a2 = a1.json()
  rp1 = resp_dict["choices"]
  rp2 = rp1[0]
  rp3 = rp2["message"]
  if len(usercontext) < 5:
     usercontext.append(rp3)
  else:
     usercontext.pop(0)
     usercontext.append(rp3)
  print(usercontext)
  userlist = closeAndOpenUserFile(userlist)
  rp4 = rp3["content"]
  op += rp4
  return op, userlist

def sendRequestNoContext(text, model):
  response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
      "Authorization": f"Bearer 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",
      "HTTP-Referer": f"telegram.org", # Optional, for including your app on openrouter.ai rankings.
      "X-Title": f"AS1MOV", # Optional. Shows in rankings on openrouter.ai.
    },
    data = json.dumps({
      "model": model, # Optional
      "messages": [
        {"role": "user", "content": text}
      ]
    })
  )
  resp_dict = response.json()
  op = 'RESPONSE: '
  temptext = "https://openrouter.ai/api/v1/generation?id="
  temptext += resp_dict["id"]
  a1 = requests.get(url=temptext, headers={'Authorization': f'Bearer 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'})
  a2 = a1.json()
  rp1 = resp_dict["choices"]
  rp2 = rp1[0]
  rp3 = rp2["message"]
  rp4 = rp3["content"]
  op += rp4
  return op

bot = Bot(token="6925589253:AAHucNlyVfHxJ5ErNqU-krI2cqeRmt0OGxo")
dp = Dispatcher()

@dp.message(F.text)
async def mainFunction(message: Message):
    all_user_list = getUserFile()
    userid = message.from_user.id
    user = findUser(userid, all_user_list)
    # print(user)
    if user is not False:
      usercontext = user[3]
      usermodel = user[2]
      usercredits = user[1]
      usermsgs = user[4]
      if message.text != '/start':
          if usercontext is False:
            ans = sendRequestNoContext(message.text, usermodel)
            await message.answer(ans)
            print(str(userid) + ':')
            print(message.text)
            print(ans)
            print('--------------------')
          else:
            ans, all_user_list = sendRequest(message.text, usermodel, all_user_list, userid)
            await message.answer(ans)
            print(str(userid) + ':')
            print(message.text)
            print(ans)
            print('--------------------')
      else:
          await message.answer('Error.')
    else:
       await message.answer("Ошибка. Подождите, пока происходит ваша регистрация...")
       newuser = [userid, 50000, model_gpt35, True, [{"role": "user", "content": "This is a placeholder message. You can ignore it."}]]
       all_user_list.append(newuser)
       all_user_list = closeAndOpenUserFile(all_user_list)
       await message.answer("Готово!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())