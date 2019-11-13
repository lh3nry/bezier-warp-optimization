import chart_studio

username = 'lh3nry' # your username
api_key = '' # your api key - go to profile > settings > regenerate key
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)
print('Updated Credentials')