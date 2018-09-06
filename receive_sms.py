from flask import Flask, request, redirect
import os
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse
# from difflib import SequenceMatcher
from difflib import get_close_matches
from stations import getStationsDict
from routing import findRoute

# def similar(a, b):
#     return SequenceMatcher(None, a, b).ratio()

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def sms_reply():

	stationsOld = set([
		"North Springs", "Sandy Springs", "Dunwoody", "Medical Center", "Buckhead", "Lindbergh Center", "Arts Center", "Midtown", "North Avenue", "Civic Center", "Peachtree Center", "Five Points", "Garnett", "West End", "Oakland City", "Lakewood/Ft. McPherson", "East Point", "College Park", "Airport",
		"Doraville", "Chamblee", "Brookhaven/Oglethorpe", "Lenox", "Lindbergh Center", "Arts Center", "Midtown", "North Avenue", "Civic Center", "Peachtree Center", "Five Points", "Garnett", "West End", "Oakland City", "Lakewood/Ft. McPherson", "East Point", "College Park", "Airport",
		"Bankhead", "Ashby", "Vine City", "Dome/GWCC/Philips Arena/CNN Center", "Five Points", "Georgia State", "King Memorial", "Inman Park/Reynoldstown", "Edgewood/Candler Park",
		"Hamilton E. Holmes", "West Lake", "Ashby", "Vine City", "Dome/GWCC/Philips Arena/CNN Center", "Five Points", "Georgia State", "King Memorial", "Inman Park/Reynoldstown", "Edgewood/Candler Park", "East Lake", "Decatur", "Avondale", "Kensington", "Indian Creek"
	])
	stationsOld = list(stationsOld)
	stations = []
	for i in stationsOld:
		i = i.lower()
		stations.append(i)

	# Take 1: Old SDK SMS - passed
	# resp = MessagingResponse()
	# resp.message("Hi, I'm MARTAN from mAlerts, here to give you your best rider experience!")
	# return str(resp)

	# Take 2: Simpler SMS - passed
	# response = MessagingResponse()
	# response.message("Hi, I'm MARTAN from mAlerts.")
	# return str(response)

	# Take 3: MMS - passed
	# response = MessagingResponse()
	# message = Message()
	# request_body = request.values.get("Body", None)
	# message.body("Hi, I'm Martan from mAlerts. If you need to refer to the MARTA map, I gotchu. You texted me: " + request_body)
	# message.media("http://www.itsmarta.com/images/train-stations-map.jpg")
	# response.append(message)
	# return str(response)

	response = MessagingResponse()
	message = Message()
	request_body = request.values.get("Body", None)
	lower_request_body = request_body.lower()
	stripped_request_body = lower_request_body.strip(",.!?/&-:;@'...")
	bodyArray = stripped_request_body.split(" ")

	waysToSayHi = ["hi", "hello", "hell", "howdy", "hh", "bonjour", "aloha", "hallo", "halo", "hey", "wassup", "wessup", "what is up", "whats up", "what's up", "hi there", "hithere", "yo", "sup"]

	# checks to see if hi or similar is in text
	for hi in waysToSayHi:
		if hi in bodyArray:
			message.body("Hi, I'm Martan from mAlerts! Please text me an origin and a destination. For example: 'Doraville to Midtown'. Or if you want to see a full MARTA map, text me 'map'.")
			response.append(message)
			return str(response)

	# if text says "map"
	if "map" in bodyArray:
		message.body("Here's the MARTA map!")
		message.media("http://www.itsmarta.com/images/train-stations-map.jpg")
		response.append(message)
		return str(response)

	# if text says "<station> to <station>""
	elif ("to" in bodyArray):
		toIndex = bodyArray.index("to")
		origin = ' '.join(bodyArray[0:toIndex])
		destination = ' '.join(bodyArray[toIndex+1:])

		stationsDict = getStationsDict()
		keys = stationsDict.keys()

		originFinalKeyList = get_close_matches(origin.lower(), keys, 1)
		destinationFinalKeyList = get_close_matches(destination.lower(), keys, 1)

		# if text contains "to" but does not contain valid station names
		if (len(originFinalKeyList) == 0 or len(destinationFinalKeyList) == 0):
			message.body("Hmm, you didn't use the right format... Please text me a valid origin and a destination. For example: Doraville to Midtown")
			response.append(message)
			return str(response)

		originFinalKey = originFinalKeyList[0]
		destinationFinalKey = destinationFinalKeyList[0]

		finalOrigin = stationsDict[originFinalKey]
		finalDestination = stationsDict[destinationFinalKey]

		output = "Cool. So you're going from " + finalOrigin + " to " + finalDestination + "."

		route = findRoute(finalOrigin, finalDestination)

		counter = 0
		for leg in route:
			if counter == 0:
				output += " Take the "
			else:
				output += " Then take the "
			if len(leg["lines"]) == 1:
				output += min(leg["lines"]).name + " line "
			elif len(leg["lines"]) == 2:
				output += min(leg["lines"]).name + " or " + max(leg["lines"]).name + " lines "
			output += leg["direction"].name + "BOUND to "
			output += leg["destination"] + " station."
			counter += 1

		message.body(output)
		response.append(message)
		return str(response)

	# if text says something invalid
	else:
		message.body("Hey, it looks like you said something that's not valid! Just send me a hello or your origin and destination stations. For example: 'Doraville to Midtown'.")
		response.append(message)

	return str(response)


if __name__ == "__main__":
	app.run(debug=True)
