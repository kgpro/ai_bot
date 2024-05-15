'''
Created on may 1, 2024
@uthor:-  KAMLESH GUJRATI
A CHAT BOT NAMED IGRIT
'''

import google.generativeai as genai
import json

def create_model(api_key):
  """
  This function configures and creates the Krina model.
  """
  genai.configure(api_key=api_key)

  generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
  }

  safety_settings = [

  ]
  user=input(" \n\n\nSo tell me, what do you want me to act like(kamlesh/krina) ?:--")
  if user == "kamlesh":
    instructions="kamlesh.txt"
  else:
    if user!="krina":
      print("I am loading krina model for you\n\n")
    instructions="KRINA INSTRUCTIONS.txt"
  with open(instructions,"r",encoding="utf-8") as krinafile:
    instruction=krinafile.read()

  system_instruction =instruction
  model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                generation_config=generation_config,
                                system_instruction=system_instruction,
                                safety_settings=safety_settings)
  return model #.

# loading the previous chats..
def loadfile(filename):
  with open(filename, "r", encoding="utf-8") as file:
    return json.load(file)

def savefile(filename, data):
  with open(filename, "w") as file:
    json.dump(data, file)

def prepare_chat(model):
  chat_history = loadfile("history.json")

  # starting chat...
  krina = model.start_chat(history=chat_history)
  return krina

def get_message_from_bot(bot, chat_text):
  response = bot.send_message(chat_text)
  return response.text


# bot=create_model("AIzaSyCETTjHyxppl7DfsocZu_wtUxGfq37huM4")
# krina=prepare_chat(bot)
# while True:
#   message=input("you:-")
#   print(get_message_from_bot(krina,message))


