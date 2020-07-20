import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import time
from bs4 import BeautifulSoup
import os

start = time.time()

casks = "https://formulae.brew.sh/api/cask.json"
casks_get = requests.get(casks)

# print (casks_get.json())

length =  len (casks_get.json())
i = 0

for cask in casks_get.json():
  i += 1
  # print(cask["homepage"])
  url = cask["homepage"]
  
  mdPath = "content/docs/" + cask["token"] + ".md"
  if os.path.exists(mdPath) == False:
  
    try:
      url_get = requests.get(url, verify=False)

    except Exception as exc:
      print(exc)
      # sys.exit()
    else:
      if url_get.status_code == 200 or url_get.status_code == "200":
        html = url_get.content
        soup = BeautifulSoup(html, "html.parser")
        heading = ""
        for h1 in soup.find_all("h1"):
          heading = heading + " " + h1.get_text().replace('\n','')
        
        
        meta = ""
        for meta_tag in soup.find_all('meta', attrs={'name': 'description'}):
          try:
            meta = meta_tag['content'].replace('\n','')
          except Exception as exc:
            print(exc)
          
        with open(mdPath, mode="w") as f: 
          f.write( f"# {cask['name'][0]}\n" )
          f.write(f"- [{cask['name'][0]}]({url})\n")
          f.write(f"  - {heading}\n")
          f.write(f"  - {meta}\n")
          f.write(f"  - `brew cask install {cask['token']}`\n")
            
  print( f"({i} / {length})  {cask['name'][0]}"  )

end = time.time()

t = start - end
print(t)
