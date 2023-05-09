import requests
import json
url = "https://the-trivia-api.com/v2/questions?limit=1"
def get_quiz():
  response = requests.get(url)
  if response.status_code==200:
    response = response.content.decode('utf-8')
    return json.loads(response)[0]
  else:
    # The request failed - print the status code and reason
    print("Request failed with status code: " + str(response.status_code))
    print("Reason: " + response.reason)
