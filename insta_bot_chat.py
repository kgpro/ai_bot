'''
Created on may 7, 2024
@uthor:-  KAMLESH GUJRATI
A CHAT BOT NAMED IGRIT
'''

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bot_backend import *

'''-----------STEP : 1 : LOGIN IN THE CHROME--------'''
serve=Service("C:/Users/gujra/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
driver=webdriver.Chrome(service=serve)


driver.get("https://www.instagram.com/accounts/login/?hl=en")

time.sleep(7)

username=driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/div/label/input")
username.send_keys("_miss_igrit_x")
password=driver.find_element( By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]/div/label/input")
password.send_keys("Miss_igrit_of_selenium")
password.send_keys(Keys.ENTER)
print("Take me to the chats in 20 seconds")
time.sleep(20)

'''-----------------LOGIN BLOCK END---------------------'''

''' ---------STEP : 2--------'''

#function for doing chats..


def wait():
    while True:
        signal=input("pass 'se' to continue/end:- ")
        if signal=="se":
            return True
            break

# function to extract text via xpath from the
def extract_text_from_html(xpath):
#starting chating on command
    div_element = driver.find_element(By.XPATH,xpath)

    # Get the text content of the div element
    text = div_element.text
    return text
    # Print the extracted text

# scraping the details of persons
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

    chats_xpath="/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div"
    print("chat history scraping initiated:-")
    time.sleep(2)
    data=extract_text_from_html(chats_xpath)
    return data

# function for managing the scrap text
def process_text(input_text):
    # Split the input text into lines
    lines = input_text.split('\n')

    # Initialize variables
    messages_history= []
    queue_meseges=[]
    message_dict = {}


    # Iterate through the lines
    for line in lines:
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
                message_dict["role"] = line
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
        message_queue.append(text)
    return message_queue

def do_chats(text):
    output = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/p")
    output.send_keys(text)
    time.sleep(1.2)
    driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div/div/div[2]/div/div/div[2]/div/div/div[3]").click()



"""----------------execution part----------"""

model=create_model("AIzaSyCETTjHyxppl7DfsocZu_wtUxGfq37huM4")
chats_history_file=loadfile("history.json")
igrit=prepare_chat(model)

print("Extracting chats in 20 seconds ")
time.sleep(5)
current_text_list=process_text(chat_history())[1]
previous_text=[]
message_queue=[]
print(fetch_new_text_from_two_files(current_text_list, previous_text))

while True:
     try:
         while True:
             print("1")
             if previous_text==[]:
                 message_queue = formate_text_and_to_messege_queue(message_queue)
                 previous_text = current_text_list
                 break
             if previous_text!=current_text_list:
                 print("2")
                 message_queue=fetch_new_text_from_two_files(current_text_list, previous_text)
                 message_queue=formate_text_and_to_messege_queue(message_queue)
                 previous_text=current_text_list
                 print("3")
                 break
             else:
                 print("waiting for messages:")
                 current_text_list=process_text(chat_history())[1]
         for message in message_queue:
             response=get_message_from_bot(igrit,message)
             do_chats(response)
             message_queue.remove(message)
             time.sleep(2)

     except Exception as e:
         print("exception occured")
         print(e)
         current_text_list = process_text(chat_history())[1]
         previous_text = []
         continue

wait()