import jwt
import requests
import json
from time import time

API_KEY = "u6oICOGrQaO8XlGoogL2hA"
API_SEC = "4VV5WU3HZxqYAVC89t0D7Ovoo3h13U1RrRYp"

# create a function to generate a token
# using the pyjwt library
def generateToken():
	token = jwt.encode(
		
		# Create a payload of the token containing
		# API Key & expiration time
		{'iss': API_KEY, 'exp': time() + 5000},
		
		# Secret used to generate token signature
		API_SEC,
		
		# Specify the hashing alg
		algorithm='HS256'
	)
	return token


# create json data for post requests
meetingdetails = {"topic": "The title of your zoom meeting",
				"type": 2,
				"start_time": "2021-12-10T10: 21: 57",
				"duration": "45",
				"timezone": "America/Phoenix",
				"agenda": "test",

				"recurrence": {"type": 1,
								"repeat_interval": 1
								},
				"settings": {"host_video": "true",
							"participant_video": "true",
							"join_before_host": "False",
							"mute_upon_entry": "False",
							"watermark": "true",
							"audio": "voip",
							"auto_recording": "cloud"
							}
				}

# send a request with headers including
# a token and meeting details
def createMeeting():
	
	headers = {'authorization': 'Bearer %s' % generateToken(), 'content-type': 'application/json'}

	r = requests.post(f'https://api.zoom.us/v2/users/me/meetings', headers=headers, data=json.dumps(meetingdetails))

	print("\n creating zoom meeting ... \n")
	# print(r.text)
	# converting the output into json and extracting the details
	status_code = r.status_code
	json_obj = json.loads(r.text)
	if status_code == 201:
			join_URL = json_obj["join_url"]
			uuid = json_obj["uuid"]
			id = json_obj["id"]
			start_URL = json_obj["start_url"]
			topic = json_obj["topic"]

			meeting_dict = {
				"id": id,
				"uuid": uuid,
				"topic": topic,
				"start_url": start_URL,
				"join_url": join_URL,
			}

			print(f'\n here is your zoom meeting link {join_URL}"\n')
			print(f'\n here is your zoom meeting id {id}"\n')
			print(f'\n here is your zoom meeting topic {topic}"\n')

	elif status_code == 400:
		error_message = json_obj["message"]
		print("response -> {}, error message -> {}".format(r, error_message))
	else:
		print(f"status code -> {status_code}")

	with open('meeting_info.txt', 'w') as meeting_info_file: 
		meeting_info_file.write(json.dumps(meeting_dict))
	
#
# you need to enable resistration before you can add the registrant
#
def add_meeting_registrant():
	# read file
#	with open('meeting_info.txt', 'r') as myfile:
#		data=myfile.read()

	# parse file
#	json_obj = json.loads(data)

	meeting_id = "89510586072"
	
	payload = { 'email':"605851356@qq.com", 'first_name':"Lan", 'last_name': "Nie" }
	meeting_ID = str(meeting_id)

	headers = {'authorization': 'Bearer %s' % generateToken(), 'content-type': 'application/json'}
	
	r = requests.post(f'https://api.zoom.us/v2/meetings/{meeting_id}/registrants', headers=headers, data=json.dumps(payload))

	status_code = r.status_code
	y = json.loads(r.text)

	if status_code == 201:
		registrant_id = y["registrant_id"]
		topic = y["topic"]
		print(f"registrant id -> {registrant_id}, topic -> {topic}")
	elif status_code == 400:
		error_message = y["message"]
		print("response -> {}, error message -> {}".format(r, error_message))
	else:
		print(f"status code -> {status_code}")


# run the create meeting function
# createMeeting()
add_meeting_registrant()
