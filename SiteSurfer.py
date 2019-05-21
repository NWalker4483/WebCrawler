import re
from mechanize import Browser
import json
from urllib.parse import urlparse
from consutils import writeout

# Takes in a Url and returns them in a simplified form 
#i.e. https://www.stackabuse.com/reading-and-writing-json-to-a-file-in-python/ becomes stackabuse.com/
def getBareUrl(link_str):
  data = urlparse(link_str)
  new_str = data.netloc
  if "www." in new_str:
    a = new_str
    new_str = a[len(a)-a[::-1].find(".www"):]

  return new_str

# Extract all links present on a webpage and return them in a list
def getLinks(br,link,get_base=False,timeout=6):
    br.open("https://" + link)
    if get_base:
        return [i.base_url for i in br.links()]
    return [i.url for i in br.links()]
    
def AddNode(parent,curr,data,seen):
    if (parent.strip() == "") or (curr.strip() == ""):
      return data
    new_node = { "data": { "id": seen[curr], "name": curr} }
    data["elements"]["nodes"].append(new_node)
    return data

def AddEdge(fro,to,size,data,seen):
    if (fro.strip() == "") or (to.strip() == ""):
      return data
    if seen[fro] == seen[to]:
      return data
    new_edge = { "data": { "source": seen[fro], "target": seen[to] ,"size": size} }
    data["elements"]["edges"].append(new_edge)
    return data

def StoreEdge(edge,edge_dict):
  if edge[0] == edge[1]:
    return edge_list
  if edge in edge_dict:
    edge_dict[edge] = edge_dict[edge] + 1
    writeout(f"{edge[0]} Reconnected to {edge[1]}",color="green")
  else:
    edge_dict[edge] = 1
  return edge_list

br = Browser()
br.set_handle_robots(False)
br.set_handle_equiv(False) 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
start = "moz.com/top500"
Q = [start]
seen = {start: "1"}
data = {
    "elements": {
    "nodes": [{"data": {"id": "1", "name": start}}],
    "edges": []
  }
}
step = 0
link = ''
edge_list = dict()  #[(source,target,size)]
while len(Q)!= 0:
    try:
      curr = Q.pop()
      writeout(f"Now Searching {getBareUrl('https://' + curr)}",color="yellow")
      neigh_q = set()
      for link in getLinks(br,curr):
        site = getBareUrl(link)
        if site.strip() == "":
          continue
        if site not in seen:
            new_id = str(len(seen))
            seen[site] = new_id
            data = AddNode(curr,site,data,seen)
            #if site not in neigh_q:
            edge_list = StoreEdge((curr,site),edge_list)
            Q.append(site)
        else:
          #if site not in neigh_q:
          edge_list = StoreEdge((curr,site),edge_list)
        neigh_q.add(site)
    except KeyboardInterrupt:
      break
    except Exception as e:
      writeout(str(e),color="red")
      writeout(f"Failure at {link} from {getBareUrl(curr)}",color="red")
# Add Finalized Edges to the JSON
for edge, size in zip(edge_list,edge_list.values()):
  source, target = edge[0],edge[1]
  data = AddEdge(source,target,size,data,seen)
with open('sites.json', 'w') as outfile:  
          json.dump(data, outfile) 





"""
 "elements": {
    "nodes": [
      { "data": { "id": "0", "name": "temp.com"} },
      { "data": { "id": "1", "name": "temp2.com"} }
    ],
    "edges": [
      { "data": { "source": "0", "target": "1" } }
    ]
  }
}
"""