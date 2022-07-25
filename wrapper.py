import base64
import os
import random
import requests
import json

url='https://cae-bootstore.herokuapp.com'
endpoint = "/question"

def get_all_questions():
	return requests.get(url + endpoint + "/all")

def get_questions(token):
	headers = {
		"Content-Type" : "application/json",
		"Authorization": "Bearer " + token
	}

	return requests.get(url + endpoint, headers=headers)

def fprint_question(que):
	pr = f" {que['question']} <:> {que['answer']}"
	print(f">{'—'*(len(pr)-1)}<")
	print(pr)
	print(f" Author: {que['author']}, ID: {que['id']}")

def print_question_list(questions):
	for question in questions:
		fprint_question(question)

def print_all_questions():
	res = get_all_questions()
	if not res:
		print("Error!")
		return
	questions = res.json()["questions"]
	print_question_list(questions)

def register_user(payload):
	payload_json_string=json.dumps(payload)
	headers = {
		'Content-Type': 'application/json'
	}

	return requests.post(
		url + "/user",
		data = payload_json_string,
		headers = headers
	)

def register():
	clear()
	print("Registration...")

	user_dict = {
		"email": input("Email: "),
		"first_name": input("First name: "),
		"last_name": input("Last name: "),
		"password": input("Password: ")
	}
	
	return register_user(user_dict)

def login_user(user_name, password):
	auth_string = user_name + ':' + password
			
	headers = {
		'Authorization': "Basic " + base64.b64encode(auth_string.encode()).decode()
	}

	user_data = requests.get(
		url + "/login",
		headers = headers
	)
	return user_data

def clear():
	os.system('cls' if os.name == 'nt' else 'clear')

def create_question(user):
	data = {
		"question": input("Question: ").strip(),
		"answer": input("Answer: ").strip()
	}
	headers = {
		'Content-Type' : 'application/json',
		'Authorization' : 'Bearer ' + user["token"]
	}
	res = requests.post(url + "/question", data=json.dumps(data), headers=headers)
	if res:
		print("Success!")
	else:
		print(res.text)
		input("Press enter to continue...")

def take_quiz():
	print("Getting questions...")
	res = get_all_questions()
	clear()
	if not res:
		print("There was an error!")
		input("Press enter to continue...")
		return
	questions: list = res.json()["questions"]
	quiz = []
	for _ in range(10):
		quiz.append(questions.pop(questions.index(random.choice(questions))))
	
	points = 0
	for item in quiz:
		quest = item['question']
		inp = input(f"{quest}: ").lower().strip()
		print(f"Answer: {item['answer']}", end=" ")
		if inp in item["answer"].lower().strip():
			points += 1
			print("(You're right)")
		else:
			print("(You're wrong)")
		print("—"*len(quest))

	clear()
	print(f"You got {points} out of 10 points!")
	input("Press enter to continue...")

def try_parse_int(string, expect):
	if string.isdigit():
		return int(string)
	print(expect)
	return None

def has_prop_val(iter, prop: str, val):
	for item in iter:
		if item[prop] == val:
			return True
	return False

def find_prop_val(iter, prop: str, val):
	for item in iter:
		if item[prop] == val:
			return item
	return None

def delete_question(token, id):
	headers = {
		'Authorization': "Bearer " + token
	}

	response=requests.delete(
		url + f"/question/{id}",
		headers = headers
	)
	return response

def edit_question(token, id, old):
	headers = {
		'Authorization': "Bearer " + token
	}

	print("Previous question:", old["question"])
	question = input("Enter new question [leave blank to keep previous]: ")
	print("Previous question:", old["answer"])
	answer = input("Enter new answer [leave blank to keep previous]: ")

	payload = {
		"question": question if len(question) > 0 else old["question"],
		"answer": answer if len(answer) > 0 else old["answer"],
	}

	response=requests.delete(
		url + f"/question/{id}",
		headers = headers,
		data=payload
	)
	return response

def your_questions(user):
	print("Getting your questions...")
	res = get_questions(user["token"])
	if not res:
		print("Something went wrong...")
		input("\nPress enter to continue...")
		return
	questions = res.json()["questions"]
	while True:
		clear()
		print_question_list(questions)
		print("—"*50)
		cmd1 = input("Would you like to...\n 1. Delete a question\n 2. Edit a question\n 3. Go back\n> ")
		if cmd1 == "1":
			id = try_parse_int(input("Input ID of question to delete: "), "Couldn't read input as integer!")
			if id == None:
				input("Press enter to continue...")
				continue
			if not has_prop_val(questions, "id", id):
				print(f"Can't find ID: `{id}`")
				input("Press enter to continue...")
				continue
			res = delete_question(user["token"], id)
			if not res:
				print("Couldn't delete question! (Not sure why, lol)")
			else:
				print("Ok, done!")
			input("Press enter to continue...")
		elif cmd1 == "2":
			id = try_parse_int(input("Input ID of question to edit: "), "Couldn't read input as integer!")
			if id == None:
				input("Press enter to continue...")
				continue
			if not has_prop_val(questions, "id", id):
				print(f"Can't find ID: `{id}`")
				input("Press enter to continue...")
				continue
			res = edit_question(user["token"], id, find_prop_val(questions, "id", id))
			if not res:
				print("Couldn't edit question! (Not sure why, lol)")
			else:
				print("Ok, done!")
			input("Press enter to continue...")
		elif cmd1 == "3":
			return

def empty_or(str1, str2):
	if str1 == "":
		return str2
	return str1

