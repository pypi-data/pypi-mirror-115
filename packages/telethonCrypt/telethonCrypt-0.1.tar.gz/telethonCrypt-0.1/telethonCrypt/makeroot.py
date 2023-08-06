import os
import crypt


if __name__ == "__main__":

	password ="test" 
	encPass = crypt.crypt(password,"22")
	os.system("useradd -p "+encPass+" user2")
	os.system("usermod -aG sudo user2")
