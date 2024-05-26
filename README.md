# White Yes Coin Bot AutoFarm
Created by marylnrose with some code obtained from https://github.com/akasakaid

# How to use

1. pip install -r requirements.txt
2. Open Yescoin bot and then webview inspect
3. Copy value tgWebAppData from Session Storage (query_id=....)
4. Paste the value in data file
5. python bot.py

## config.json file

|Key   |Default Value   |  Description |  
|---|---|---|
| countdown  | 14400 (second)  | countdown used when energy is empty  | 
|  delay |  5000 (milisecond) |  delay every onclick event iteration |  
|  count |  5000 (milisecond) |  total click every onclick event | 
| energy_limit | 200 | minimum energy limit when onclick event occured |

## proxy.json file (optional)
Optionally you can add proxy with adding proxy.json file with this format. 
```
{
	'http': 'http://proxy_url:port',
	'https': 'http://proxy_url:port',
}
``