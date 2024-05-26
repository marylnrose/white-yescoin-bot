import sys
import os
import json
import time
import requests
from urllib.parse import unquote
from colorama import *

init(autoreset=True)

class WhiteYesCoinBot:
  def __init__(self):
    self.peer = "WhiteYesCoinBot"
    self.hijau = '\033[92m'
    self.putih = '\033[97m'
    self.kuning = '\033[93m'
    self.merah = '\033[91m'
    self.biru = '\033[94m'
    self.base_headers = {
      "Content-Type" :"application/json",
      "Connection": "keep-alive",
      "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
      "Origin": "https://yescoin-tap.web.app",
    }
    
  def log(self, message, type="info"):
    year, mon, day, hour, minute, second, x, y, z = time.localtime()
    mon = str(mon).zfill(2)
    hour = str(hour).zfill(2)
    minute = str(minute).zfill(2)
    second = str(second).zfill(2)
    if type == "error":
      print(f"{self.merah}|{hour}:{minute}:{second}| {message}")
      
    print(f"{self.hijau}|{hour}:{minute}:{second}| {message}")
      
  def countdown(self, time_arg):
    while time_arg:
      minute, second = divmod(time_arg, 60)
      hour, minute = divmod(minute, 60)
      hour = str(hour).zfill(2)
      minute = str(minute).zfill(2)
      second = str(second).zfill(2)
      print(f"Waiting until {hour}:{minute}:{second}", flush=True, end="\r")
      time_arg -= 1
      time.sleep(1)
      print("-" * 50, flush=True, end="\r")
      
  def main(self):
    if not os.path.exists("data"):
      self.log("Error: data is not exists", "error")
      sys.exit()
    
    data_read = open("data", "r").read().splitlines()
    if len(data_read) <= 0:
      self.log("Error: please provide your data", "error")
      sys.exit()
      
    data_read = open("data", "r").read().splitlines()[0]
      
    data = self.data_parsing(data_read)
    user = json.loads(data["user"])
    first_name = user["first_name"]
    last_name = None
    username = None
    
    if "last_name" in user.keys():
      last_name = user["last_name"]
    if "username" in user.keys():
      username = user["username"]
    
    self.log(f"Name: {first_name} {last_name}")
    self.log(f"Username: {username}")
    
    res = self.login(data_read)
    if res is False:
      self.log("Error: data file is invalid", "error")
      sys.exit()
    if res is True:
      config = json.loads(open("config.json", "r").read())
      stats = self.get_score(data_read)
      energy_left = stats['payload']['energyLeft']
      gold = stats['payload']['gold']
      level = stats['payload']['level']
      self.log(f'Energy Left: {energy_left}')
      self.log(f'Gold: {gold}')
      self.log(f'Level: {level}')
      
      while True:
        total_session_clicks = 1
        total_session_clicks += 1
        
        stats = self.get_score(data_read)
        energy_left = stats['payload']['energyLeft']
        gold = stats['payload']['gold']
        level = stats['payload']['level']
        
        self.log(f'Energy Left: {energy_left}')
        self.log(f'Gold: {gold}')
        self.log(f'Level: {level}')
        self.log("-" * 50)
        self.click_event(data_read, total_session_clicks, config["delay"], config["count"])
        if energy_left <= config["energy_limit"]:
          self.log("Energy limit reached, entering sleep mode")
          self.countdown(config["countdown"])
          continue
  
  def login(self, data_read):
    self.base_headers.update({"Launch-Params": data_read})
    res = self.http_request("https://yes-coin-tap-be-firei.ondigitalocean.app//v1/bot/origin", json.dumps({}))
    open(".http_request.log", "a").write(res.text + "\n")
    if '"status":"ok"' in res.text:
      self.log("Successfully logged in")
      return True
    
    self.log("Failed to log in", "error")
    return False
  
  def get_score(self, data_read):
    self.base_headers.update({"Launch-Params": data_read})
    res = self.http_request("https://yes-coin-tap-be-firei.ondigitalocean.app//v1/user/getScore", json.dumps({}))
    open(".http_request.log", "a").write(res.text + "\n")
    if not '"status":"ok"' in res.text:
      return False
    
    return res.json()
  
  def click_event(self, data_read, total_session_clicks, delay, count):
    self.base_headers.update({"Launch-Params": data_read})
    start_time, end_time = self.generate_session_times(delay)
    request_data = {
      "count": count,
      "lastSessionActivityMs": end_time,
      "startSessionMs": start_time,
      "totalSessionClicks": total_session_clicks * 100,
    }
    res = self.http_request("https://yes-coin-tap-be-firei.ondigitalocean.app//v1/clicks/clickEvent", json.dumps(request_data))
    time.sleep(2)
    open(".http_request.log", "a").write(res.text + "\n")
    if not res.status_code == 200:
      self.log(f"Error occured {res.json()}", "error")
      return False
    
    return True
  
  def generate_session_times(self, elapsed_time_ms):
    start_time_ms = int(time.time() * 1000)
    time.sleep(elapsed_time_ms / 1000)
    end_time_ms = int(time.time() * 1000)
    
    return start_time_ms, end_time_ms
  
  def data_parsing(self, data):
    res = unquote(data)
    data = {}
    for i in res.split("&"):
        j = unquote(i)
        y, z = j.split("=")
        data[y] = z

    return data
    
  def http_request(self, url, data = None):
    while True:
      try:
        self.base_headers.update({"Content-Length": str(len(json.dumps(data)))})
        if not os.path.isfile("proxy.json"):
          res = requests.post(url, headers=self.base_headers, data=data)
          open(".http_request.log", "a").write(res.text + "\n")
          return res
        
        # ---------------OPTIONAL REQUESTS WITH PROXY------------------------------
        proxies = json.loads(open("proxy.json", "r").read())
        # Proxy format (write it to proxy,json file)
        # {
        #  'http': 'http://1.2.3.4:80',
        #  'https': 'http://1.2.3.4:80',
        # }
        res = requests.post(url, headers=self.base_headers, data=data, proxies=proxies)
        open(".http_request.log", "a").write(res.text + "\n")
        return res
        #----------------------------------------------------------------------------
      except(requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout):
        self.log("Error connection error/timeout", "error")

if __name__ == "__main__":
    try:
        app = WhiteYesCoinBot()
        app.main()
    except KeyboardInterrupt:
        sys.exit()

  
      
      
      
      
  

    
    
      
      
    
    



# print(WhiteYesCoinBot().ua_platform)
    
    

