import bcrypt


#function that prints out the result of a password check
def checkPW(pw, hash):
    if bcrypt.checkpw(pw, hash):
        print("match")
    else:
        print("does not match")


#create parameters
password = 'password'
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)



#check two passwords, first the correct password, and then an incorrect string
checkPW(password.encode('utf-8'), hashed)
checkPW("notthecorrectpassword".encode('utf-8'), hashed)