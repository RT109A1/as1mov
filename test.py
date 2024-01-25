import requests
import json
import asyncio
import logging
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

def sendRequest(text, model):
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
  print(resp_dict["id"])
  temptext += resp_dict["id"]
  print(temptext)
  a1 = requests.post(url=temptext, headers={'Authorization': f'Bearer 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'})
  a2 = a1.json()
  print(a2)
  rp1 = resp_dict["choices"]
  rp2 = rp1[0]
  rp3 = rp2["message"]
  rp4 = rp3["content"]
  print(resp_dict)
  op += rp4
  return op

bot = Bot(token="6925589253:AAHucNlyVfHxJ5ErNqU-krI2cqeRmt0OGxo")
dp = Dispatcher()

@dp.message(F.text)
async def mainFunction(message: Message):
    userid = message.from_user.id
    if message.text != '/start':
        ans = sendRequest(message.text, model_mythomax)
        await message.answer(ans)
        # print(str(userid) + ':')
        # print(message.text)
        # print(ans)
        print('--------------------')
    else:
        await message.answer('Error.')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())