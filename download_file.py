#!usr/bin/env python
import requests

#download a file
def download(url):
    get_response = requests.get(url)
    file_name= url.split("/")[-1]

    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)

download("https://images.theconversation.com/files/336248/original/file-20200520-152302-97x8pw.jpg")
