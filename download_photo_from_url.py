import requests

def download_photo(url, file_name):
    data = requests.get(url).content
    with open(f'photos/{file_name}','wb') as fi:
        fi.write(data) 