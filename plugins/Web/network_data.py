#-------------------------------------------------------------------------------
# Name:        network_data.py
# Purpose:     Captures network data when selected.
#
# Author:      Akshay K T
#
# Created:     16-11-2023
#-------------------------------------------------------------------------------
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
class NetworkData:
    def __init__(self, driver):
        self.driver = driver
    def network_data(self):
        from plugins.Core import constants  
        config_path = constants.CONFIG_PATH
        check_key = "network_data"
        with open(config_path,"r") as file:
            configdata = json.load(file)
        if check_key in configdata and configdata[check_key] == "Yes":
            print("Network Data Capture Selected")
            network_logs = []
            timeout = 5 #reduce time
            entries = self.driver.execute_script("return window.performance.getEntries()")
            max_retries = 0 #change as needed(reduced time)
            for entry in entries:
                request_duration = entry.get("duration", "")
                request_url = entry.get("name", "")
                initiator_type = entry.get("initiatorType", "")
                url = request_url
                
                session = requests.Session() #start a session 
                retry_strategy = Retry(
                    total=max_retries,
                    backoff_factor=0.1,  # Adjust as needed
                    status_forcelist=[500, 502, 503, 504],
                    method_whitelist=["GET"],
                )
                
                adapter = HTTPAdapter(max_retries=retry_strategy)
                session.mount("http://", adapter)
                session.mount("https://", adapter)
                
                try:
                    response = session.get(url, verify=False, timeout=timeout)
                    response.raise_for_status() 
        
                    get_name_url = request_url.rfind("/")
                    request_name = request_url[get_name_url + 1:]
                    if initiator_type not in ["XMLHttpRequest", "fetch", "xmlhttprequest"]:
                        if initiator_type in ["img", "link", "css"]:
                            entry_data = {
                                "Name": request_name,
                                "Request URL": request_url,
                                "Status Code": response.status_code,
                            }
                        else:
                            entry_data = {
                                "Name": request_name,
                                "Request URL": request_url,
                                "Status Code": response.status_code,
                                "Request Method": response.request.method,
                                "Duration": request_duration,
                                "Request Headers": dict(response.request.headers),
                                "Response Headers": dict(response.headers),
                                "Initiator Type": initiator_type,
                                "Response Content": "",
                            }
                    else:
                        entry_data = {
                            "Name": request_name,
                            "Request URL": request_url,
                            "Status Code": response.status_code,
                            "Request Method": response.request.method,
                            "Duration": request_duration,
                            "Request Headers": dict(response.request.headers),
                            "Response Headers": dict(response.headers),
                            "Initiator Type": initiator_type,
                            "Response Content": response.text,
                        }
                    network_logs.append(entry_data)
                    output_file = "network_data.json"
                    with open(output_file, "w") as json_file:
                        json.dump(network_logs, json_file, indent=4)
                        
                except requests.exceptions.RequestException as e:
                    get_name_url = request_url.rfind("/")
                    request_name = request_url[get_name_url + 1:]
                    if any(code in str(e) for code in ['400', '401', '402', '403', '404', '405']):
                        entry_data = {
                            "Name": request_name,
                            "Request URL": request_url,
                            "Status Code": response.status_code,
                            "Request Method": response.request.method,
                            "Duration": request_duration,
                            "Request Headers": dict(response.request.headers),
                            "Response Headers": dict(response.headers),
                            "Initiator Type": initiator_type,
                            "Response Content": response.text,
                        }
                        network_logs.append(entry_data)
                        output_file = "network_data.json"
                        with open(output_file, "w") as json_file:
                            json.dump(network_logs, json_file, indent=4)
                    # print(f"An exception occurred for {url}: {e}")
                    continue
    