#The Content has been made available for informational and educational purposes only
from utils.phone.quidam_core import *

emailsFilesName = "utils/phone/quidam_emails.txt"
listModules = ["instagram", "twitter", "github"]




def possibleDomain(emailInfo):
    EmailsFile = open(emailsFilesName, 'r')
    Emails = EmailsFile.readlines()
    EmailsFile.close()
    emails = []
    print("Possible emails: ")
    emailProvider = emailInfo.split("@")[1]
    for email in Emails:
        email=email.replace("\n", "")
        if emailProvider[0]==email[0]:
            if len(emailProvider.split(".")[0])==len(email.split(".")[0]):
                print(emailInfo.split("@")[0] + "@" + email)
                emails.append(emailInfo.split("@")[0] + "@" + email)
    return emails

def get_forgot_password_data(phone):
    result = {}
    target_phone = phone
    info = instagram(phone)
    if '"status"' not in info:
        print("Email extract with instagram of " + phone + ": " + info)
        result["instagram"] = "Email extract with instagram of " + phone + ": " + info
    else:
        print(phone+" account not found")
        result["instagram"] = phone+" account not found"


    info = twitter(target_phone)
    if len(info) == 2:
        print("The end of the phone number in twitter of " + target_phone + ": " + str(info["phone"]))
        print("Email extract with twitter of " + target_phone + ": " + info["email"])
        emails = possibleDomain(info["email"])
        result["twitter"] = "The end of the phone number in twitter of " + target_phone + ": " + str(info["phone"]) + "\n"
        result["twitter"] += "Email extract with twitter of " + target_phone + ": " + info["email"] + "\n"
        result["twitter"] += "Possible emails: " + "\n"
        result["twitter"] += str(emails)
    elif len(info) == 1:
        print("Email extract with twitter of " + target_phone + ": " + info["email"])
        result["twitter"] = "Email extract with twitter of " + target_phone + ": " + info["email"]
        emails = possibleDomain(info["email"])
        result["twitter"] += "Possible emails: " + "\n"
        result["twitter"] += str(emails)
    else:
        print("Not informations found in twitter")
        result["twitter"] = "Not informations found in twitter"
    info = github(target_phone)
    if len(info) == 0:
        print("Not informations found in github")
        result["github"] = "Not informations found in github"
    else:
        print("All emails found in github:")
        result["github"] = "All emails found in github:\n"
        for e in info:
            print("Email " + e["email"] + " for " + e["name"])
            result["github"] += "Email " + e["email"] + " for " + e["name"] + "\n"
    return result