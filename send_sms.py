from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = ""
# Your Auth Token from twilio.com/console
auth_token  = ""

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+17064614889", 
    from_="+16787265889",
    body="Hi g money!")

print(message.sid)