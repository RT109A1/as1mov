import requests
import json

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer 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",
    "HTTP-Referer": f"telegram.org", # Optional, for including your app on openrouter.ai rankings.
    "X-Title": f"AS1MOV", # Optional. Shows in rankings on openrouter.ai.
  },
  data = json.dumps({
    "model": "gryphe/mythomist-7b", # Optional
    "messages": [
      {"role": "user", "content": "What is the meaning of life?"}
    ]
  })
)
print(response.json())
