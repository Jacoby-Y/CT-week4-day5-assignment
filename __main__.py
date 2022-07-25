import time
from wrapper import *;

def admin_prompt(user):
	while True:
		clear()
		print("Cmds: \n 1. Create question\n 2. Take quiz\n 3. View your questions\n 4. View all questions\n 5. Quit")
		cmd = input("> ").strip()
		if cmd == "1":
			clear()
			create_question(user)
			time.sleep(3)
		elif cmd == "2":
			clear()
			take_quiz()
		elif cmd == "3":
			clear()
			your_questions(user)
		elif cmd == "4":
			clear()
			print_all_questions()
			input("Press enter to continue...")
		elif cmd == "5":
			return
	
def user_prompt(user):
	while True:
		clear()
		print("Cmds: \n 1. Take quiz\n 2. View all questions\n 3. Quit")
		cmd = input("> ").strip()
		if cmd == "1":
			clear()
			take_quiz()
		elif cmd == "2":
			clear()
			print_all_questions()
			input("Press enter to continue...")
		elif cmd == "3":
			return

def main():
	user = {}

	clear()
	print("Welcome to Trivia... Game?")

	while True:
		cmd = empty_or(input("Login or Signup? "), "login").lower()
		if cmd == "login":
			res = login_user(
				empty_or(input("Email: "), "cobyyliniemi@gmail.com"),
				empty_or(input("Password: "), "yliniemi"),
			)
			if res:
				# print(user.json())
				clear()
				user = res.json()
				print("Welcome")
				break
			else:
				print("Error: can't login!")
				time.sleep(3)
				clear()
		elif cmd == "signup":
			print(register())
			clear()

	if user["admin"]:
		admin_prompt()
	else:
		user_prompt()

if __name__ == "__main__":
	main()