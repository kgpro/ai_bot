'''
Created on may 7, 2024
@uthors:-  KAMLESH GUJRATI && AYUSH KUMAR MALVIYA 
 A CHAT BOT FOR INSTAGRAM VIRTUAL HUMAN 
'''
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import google.generativeai as genai
import json



'''------------------------------------ backed work functions/interaction with googles api--------------------------------------------------'''
def create_model(api_key):
  """
  This function configures and creates the Krina model.
  """
  genai.configure(api_key=api_key)

  generation_config = {
    "temperature": 2,
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
  model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                generation_config=generation_config,
                                system_instruction=system_instruction,
                                safety_settings=safety_settings)
  return model #.

# loading the previous chats..
'''---------chat storing in mngmt---------------'''
def loadfile(filename):
  with open(filename, "r", encoding="utf-8") as file:
    return json.load(file)

def savefile(filename, data):
  with open(filename, "w") as file:
    json.dump(data, file)
'''---------------------------------------------'''

def prepare_chat(model):
  chat_history = loadfile("history.json")

  # starting chat...
  krina = model.start_chat(history=chat_history)
  return krina

# pases text and return the response from the bot
def get_message_from_bot(bot, chat_text):
  response = bot.send_message(chat_text)
  return response.text
'''--------------------------------------------end of the block-------------------------------------------------------------------------------'''

#function for starting web driver
def driver_start():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        service = Service("C:/Users/gujra/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
        driver = webdriver.Chrome(service=service)
        return driver
    except Exception as e:
        print(f"Error initializing driver: {e}")
        return None
def login_instagram(driver,user,pswd):
    #driver.get("https://www.instagram.com/accounts/login/?hl=en")
    driver.execute_script("window.location.href='https://www.instagram.com/accounts/login/?hl=en';")

    time.sleep(7)

    username=driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div[1]/div[2]/form/div/div[1]/div/label/input")
    username.send_keys(user)
    password=driver.find_element( By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div[1]/div[2]/form/div/div[2]/div/label/input")
    password.send_keys(pswd)
    password.send_keys(Keys.ENTER)
    print("Take me to the chats in 20 seconds")
    time.sleep(20)

# function to extract text via xpath from the
def extract_text_from_html(xpath):
#starting chating on command
    div_element = driver.find_element(By.XPATH,xpath)

    # Get the text content of the div element
    text = div_element.text
    return text
    # Print the extracted text

# scraping the details of persons in the group chat [currenty not in use ]
def member_list():
    print("member list scraping initiated take me to the chats in 7 second from now:--")
    time.sleep(7)
    driver.find_element(By.XPATH,
                        "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[2]/div[3]/div").click()
    # it will click the i button

    time.sleep(7)
    members_xpath="/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[2]"
    data=extract_text_from_html(members_xpath)

    driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div/div[1]/div[1]/div/div[2]/div[3]/div").click()
    return data


# chat history scraping
def chat_history():
    print("chat history scraping initiated:-")
    chats_xpath="/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div"
    data=extract_text_from_html(chats_xpath)
    return data

# function for managing the scrap text
# this function will return the dictionary of full massage history and the dictionary of all  massage excluding msg sent by self
def process_text(input_text):
    # Split the input text into lines
    lines = input_text.split('\n')

    # Initialize variables
    messages_history= []
    queue_meseges=[]
    message_dict = {}
    pas=0
    # Iterate through the lines
    for line in lines:
        if pas==1 :#handling and formatting the insta replies misunderstandings /preventing bot to reply self

            if  ";)" in line: # text will be added to the massage from the bot to prevent the self reply
                pas=0
            continue
        if ":" in line or not line.strip():
            # Skip lines that contain a time stamp or are empty
            continue
        elif line == "Enter":
            # Add the message dictionary to the messages list
            if message_dict:
                messages_history.append(message_dict)
                if message_dict["role"] != "You sent":
                    queue_meseges.append(message_dict)
                message_dict = {}

        else:
            # Add the line to the current message dictionary
            if "role" in message_dict:
                message_dict["parts"].append(line)



            else:
                message_dict["role"] = line #
                if "replied to you" in line:
                    pas=1
                message_dict["parts"] = []

    # Add the last message dictionary to the messages list
    if message_dict:
        messages_history.append(message_dict)
    return messages_history, queue_meseges

def fetch_new_text_from_two_files(new_text, previous_text):# call the function in new text arguement new_tex[chat_histry()]
    list_of_new_text=[]
    if previous_text == []:
        list_of_new_text = new_text
    else:
        for i in range(1,len(new_text)):
            if new_text[-i]!=previous_text[-1]:
                list_of_new_text.append(new_text[-i])
            else:
                break
    return list_of_new_text


def formate_text_and_to_messege_queue(dict_queue):
    message_queue=[]
    for dict in dict_queue:
        text=f"[{dict['role']}]"+f"[{dict['parts'][0]}]"
        print(text)
        message_queue.append(text)
    return message_queue


# copy the text passes to it and paste it to the msg box and send it
def do_chats(text):
    pyperclip.copy(text)
    box=driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/div/p")
    box.click()
    box.send_keys(Keys.CONTROL, 'v')
    time.sleep(4)
    box.send_keys(Keys.ENTER)

def load_ai_model():
    model=create_model("YOUR API KEY")
    chats_history_file=loadfile("history.json")
    ai=prepare_chat(model)

    print("Extracting chats in 5 seconds ")
    time.sleep(5)
    return ai

# main function to run programm itratively
def run(x,ai):
    current_text_list=process_text(chat_history())[1]
    previous_text=[]
    message_queue=[]
    print(fetch_new_text_from_two_files(current_text_list, previous_text))

    while True:
     try:

         while True:
             print("1")
             if previous_text==[]:
                 message_queue = formate_text_and_to_messege_queue(current_text_list)
                 previous_text = current_text_list
                 break
             if previous_text!=current_text_list:
                 print("2")
                 message_queue=fetch_new_text_from_two_files(current_text_list, previous_text)
                 message_queue=formate_text_and_to_messege_queue(message_queue)
                 previous_text=current_text_list
                 break
             else:
                 current_text_list=process_text(chat_history())[1]
         for message in message_queue:
             print("3")
             response=get_message_from_bot(ai,message)
             print(response)
             do_chats(response)
             break
     # except IndexError as e:
     #     print(e)
     #     time.sleep(1)
     #     # current_text_list = process_text(chat_history())[1][-1]
     #     # previous_text = []
     #     # message_queue = []
     #     if x==0:
     #         return
     #     run(x-1,ai)

     except Exception as e:
         print("exception occured")
         print(e)
         # current_text_list = process_text(chat_history())[1]
         # previous_text = []
         if x==0:
             return
         run(x-1,ai)

'''----------------------------------- execution part--------------------------------------------'''

var=int(input("developing[1]/execution[2]:-"))
if var==1:
    user='id1'
    pswd="pswd"
else:
    user="id2"
    pswd="pswd"

driver=driver_start() # start the web driver

login_instagram(driver,user,pswd) # loging in into the instagram account

bot=load_ai_model()   # creating ai model

run(1,bot)  # running the main program
