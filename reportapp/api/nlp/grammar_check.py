import sys
import urllib.parse
import urllib.request
from urllib.error import HTTPError
from urllib.error import URLError
import json
class grammar_checker:
	def get_ginger_url(self,text):
	    API_KEY = "6ae0c3a0-afdc-4532-a810-82ded0054236"
	    scheme = "http"
	    netloc = "services.gingersoftware.com"
	    path = "/Ginger/correct/json/GingerTheText"
	    params = ""
	    query = urllib.parse.urlencode([
	        ("lang", "US"),
	        ("clientVersion", "2.0"),
	        ("apiKey", API_KEY),
	        ("text", text)])
	    fragment = ""
	    return(urllib.parse.urlunparse((scheme, netloc, path, params, query, fragment)))


	def get_ginger_result(self,text):
	    url = self.get_ginger_url(text)

	    try:
	        response = urllib.request.urlopen(url)
	    except HTTPError as e:
	            print("HTTP Error:", e.code)
	            quit()
	    except URLError as e:
	            print("URL Error:", e.reason)
	            quit()

	    try:
	        result = json.loads(response.read().decode('utf-8'))
	    except ValueError:
	        print("Value Error: Invalid server response.")
	        quit()

	    return(result)


	def grammar_checker(self,text):
	    results = self.get_ginger_result(text)
	    print(results)
	    if(not results["LightGingerTheTextResult"]):
	        # print("True")
	        return True
	    else:
	    	# print("False")
	        return False

if __name__ == '__main__':
	print(grammar_checker().grammar_checker("Acceleration due to gravity is 9"))
	print(grammar_checker().grammar_checker("accleration due to gravity is 9"))

