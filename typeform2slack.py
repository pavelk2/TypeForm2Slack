import requests
import json
import os

typeform_form_id = os.environ['TYPEFORM_FORM_ID']
typeform_API_KEY = os.environ['TYPEFORM_API_KEY']
slack_token = os.environ['SLACK_API_TOKEN']
slack_team = os.environ['SLACK_TEAM']

def getFromTypeForm(typeform_id, typeform_API_KEY):
    url = "https://api.typeform.com/v0/form/"+typeform_id+"?key="+typeform_API_KEY+"&completed=true"
    
    r = requests.get(url)
    results = r.json()
    
    emails = []

    for response in results['responses']:
        for question in response['answers'].keys():
            if "email" in question:
                emails.append(response['answers'][question])
    return emails

def sendSlackInvites(email, slack_token, slack_team):    
    payload = {
        "email": email,
        "token": slack_token,
        "set_active": True
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    url = "https://"+slack_team+".slack.com/api/users.admin.invite"

    r = requests.post(url, data = payload, headers=headers)
    print(r.json())

if __name__ == "__main__":

    emails = getFromTypeForm(typeform_form_id, typeform_API_KEY)
    for email in emails:
        sendSlackInvites(email, slack_token, slack_team)