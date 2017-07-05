import requests
import json

def getFromTypeForm(form_id, typeform_API_KEY):
    url = "https://api.typeform.com/v0/form/"+form_id+"?key="+typeform_API_KEY+"&completed=true"
    
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
    print r.json()

if __name__ == "__main__":
    with open('credentials.json') as credentials_file:
        credentials = json.load(credentials_file)
    emails = getFromTypeForm(credentials['typeformID'],credentials['typeformAPI_KEY'])
    for email in emails:
        sendSlackInvites(email, credentials['slackAPI_KEY'], credentials['slackTEAM'])