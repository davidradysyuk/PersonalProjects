import secrets
import string

password = " "
letters = string.ascii_letters
digits = string.digits
alphabet = letters + digits
password_lengthstr = input("What is the length of your password?")
password_lengthint = int(password_lengthstr)

for i in range(password_lengthint):
    password += ''.join(secrets.choice(alphabet))
print(password)
