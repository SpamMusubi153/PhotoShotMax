# PhotoShootMax.py
# Max Tran
# 11/3/2023

# An entry-level kiosk interface to enable live photo sharing over email 
# during a photo shoot or photobooth.

# This short project was started on 11/3/2023 for a 
# Seattle University A.n.I.Ma.L club and ACM club headshot and networking event. 
# The first major version was finished on the same day.

import os
import time
import random
import glob
import threading
import shutil

import cv2 as cv

#  ----------------------------------------- 
# | User-Configurable Environment Variables |
#  ----------------------------------------- 

# Make sure to escape your slashes and to add an additional two slashes at the end of your path.
SOURCE_HEADSHOT_FOLDER = r""
TARGET_HEADSHOT_FOLDER = r""

# Select "Windows" or "Linux" as the Platform
PLATFORM = "Windows"

REPORT_FILE_NAME = "Results.csv"

QUESTIONS_TO_ASK = [
    # "Hello! If the picture on the screen is yours, please enter your name.",
    "Hello! If the picture on the screen is yours, please enter your Seattle University email.",
    "Would you like to hear about AI and Machine Learning (ML) opportunities through A.n.I.Ma.L club's newsletter? (Y/N)",
    "Would you like to sign up for ACM's newsletter? (Y/N)"
]

# Based on the questions above, select the question type.
# Currently, you may choose between a "Text" question to accept freeform text,
# or a "Y/N" question to accept a yes or no answer. If you select the "Y/N" type, make sure to explain the choice to the user
# in your question text.
QUESTION_TYPE = [
    # "Text",
    "Text",
    "Y/N",
    "Y/N"
]

# Based on the questions asked above, define header labels for the results stored in the results file.
HEADER_LABELS = [
    # "Name",
    "Email",
    "Animal Newsletter",
    "ACM Newsletter"
]

# Scale the image previews by this amount.
IMAGE_SCALE_FACTOR = 0.3

#  ----------------------------
# | Beginning of Program Logic |
#  ---------------------------- 
program_running = True

# Determine how to clear the console based on the specified platform.
CLEAR_STRING = None
if PLATFORM == "Windows":
    CLEAR_STRING = "cls"
elif PLATFORM == "Linux":
    CLEAR_STRING = "clear"
else:
    raise ValueError("Please enter either \"Windows\" or \"Linux\" for your platform type.")

# A miniature function to clear the console.
def clear():
    os.system(CLEAR_STRING)


# A function to save a user's responses to the results file
def save_responses(user_response_array):

    # This manual process of csv creation was intended as practice with working with arrays and list comprehensions (Which are especially fun to use).

    # Ensure that all of the user responses are stored as strings.
    user_response_array = [str(response) for response in user_response_array]

    # Create a string representation of the user responses
    user_response_string = ",".join(user_response_array)

    # If the file has not been previously created, create it now and append a header row.
    create_headers = False
    if not os.path.exists(REPORT_FILE_NAME):
        create_headers = True

    # Open and write to the results file.
    with open(REPORT_FILE_NAME, "at") as file:
        if create_headers:
            header_labels_string = ",".join(HEADER_LABELS)
            file.write(f"{header_labels_string}\n")
            create_headers = False

        file.write(user_response_string)
    
        file.close()


# An asynchronous function to receive user input to the pre-defined questions above.
def ask_questions():

    responses = []

    # Ask each defined question and receive a user response.
    for index, question in enumerate(QUESTIONS_TO_ASK):
        clear()

        response = None
        if QUESTION_TYPE[index] == "Text":
            print(question)
            response = input()

        elif QUESTION_TYPE[index] == "Y/N":
            while True:
                print(question)
                response = input().lower()

                # If an invalid response is provided, repeat the prompt process.
                if (not response == "y") and (not response == "n"):
                    print("You have entered an invalid answer.\nPlease try again and enter either \"Y\" for yes, or \"N\" for no.")
                    time.sleep(1)
                    clear()
                    continue
                
                # If a valid response is provided, format the answer as a complete word.
                else:
                    if response == "y":
                        response = "Yes"
                    elif response == "n":
                        response = "No"
                    else:
                        response = "?"
                    break

        responses.append(response)
        
        # TODO: Remove this condition and implement more uniform queued photo storage.
        if response == "Q":
            return None

        # Display a confirmation message after each user input.
        MESSAGES = [
            "Alright!",
            "Ok!",
            "Sounds good!"
        ]

        print(MESSAGES[random.randint(0, len(MESSAGES) - 1)])
        time.sleep(1)
    
    return responses

def fetch_latest_headshot_path():

    # Obtain the latest headshot image from the raw headshot folder.
    all_headshots = glob.glob(SOURCE_HEADSHOT_FOLDER + "*")
    newest_headshot = max(all_headshots, key=os.path.getctime)

    return newest_headshot

def continuously_display_newest_headshot():
    while program_running:

        # Fetch the latest headshot
        newest_headshot = fetch_latest_headshot_path()

        # Display the headshot if one can be found.
        if newest_headshot is not None:
            headshot = cv.imread(newest_headshot)

            # Resize the headshot so that it can co-exist with the terminal by staying in a smaller area of the screen.
            headshot = cv.resize(headshot, dsize=None, fx=IMAGE_SCALE_FACTOR, fy=IMAGE_SCALE_FACTOR)

            cv.imshow("Your Headshot", headshot)
            cv.waitKey(1000)

        # Otherwise, delay before checking again.
        else:
            time.sleep(1)
            continue


#  --------------------
# | The Main Function |
#  -------------------- 
if __name__ == "__main__":

    # Start the function to continuously display the latest headshot in a separate thread.
    display_thread = threading.Thread(target=continuously_display_newest_headshot)
    display_thread.start()

    while True:

        # Store the current picture.
        source_path = fetch_latest_headshot_path()

        # Prompt the user for contact information and receive the user's responses.
        responses = ask_questions()
        save_responses(responses)

        if responses == None:
            continue

        email = responses[0]
        
        # Move the picture into the destination path
        destination_path = os.path.join(TARGET_HEADSHOT_FOLDER, email)
        shutil.copy(source_path, destination_path)

        clear()
        print("All done! Check your email in a few moments for your picture.")
        time.sleep(2)