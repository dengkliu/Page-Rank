"Introduction to Informatics"
"HW7-3"
"PageRank analysis of graph structure. "
"Created by Dengke Liu"
"5/1/2015"

"""the class graph"""          
class Digraph(object):
    def __init__(self):
        self.pages = set([])
        self.links = {}
    def addpage(self, page):
        if page in self.pages:
            raise ValueError('Duplicate node')
        else:
            self.pages.add(page)
            self.links[page] = []
    def addlink(self, link):
        src = link.getSource()
        dest = link.getDestination()
        if not(src in self.pages and dest in self.links):
            raise ValueError('Node not in graph')
        self.links[src].append(dest)   
    def childrenOf(self, page):
        return self.links[page]
    def haspage(self, page):
        return page in self.nodes
    def __str__(self):
        res = ''
        for k in self.links:
            for d in self.links[k]:
                res = res + str(k) + '->' + str(d) + '\n'
        return res[:-1]

"""PageRank function computes the probabilities of 
   the stationary distribution of the nodes in the graph G 
   based on the structure of the incoming links.
      
   Parameters
   -----------
    G : bigraph

    c : float
      the probability at each step a random page is visted, it is 0.15
    
    Returns
    -------
    statdist : dictionary
       Dictionary of nodes with the probabilities of stational distribution as value
"""

def Probupdate(G, c, statdist, numnode):
    "define a new dictionary to store the updated probability"
    newdist={}
    "update the probability for each page"
    for page1 in statdist:
        prob=0
        for page2 in statdist:
            "if page 2 has links to page 1, then add the probability"
            "the probabiliy that page 2 is visited is statdist[page2]"
            "every pages linked by page 2 have equal chance to be visited"
            "add up all the probabilies for page 1 from links in other pages including page 2"
            if page1 in G.links[page2]:
                prob+=1/float(len(G.links[page2]))*statdist[page2]
            "the new probability for page 1"
        newdist[page1]=c+(1-c)*prob
    return newdist
      
def PageRank(G):
             
    if len(G.links) == 0:
        return {}
    
    numnode=len(G.links)
    "the original stationary distribution is uniform"
    statdist = dict.fromkeys(G.links, 1.0 /float(numnode))
    
    "update the probability for each page"
    while True:
        laststep=statdist
        statdist=Probupdate(G, 0.15, laststep, numnode)
        print statdist
        "comparing the change in probabilities"
        difference=[]
        for page in laststep:
            difference.append((statdist[page]-laststep[page])**2)
        if max(difference)<0.0000001:
            break
    return statdist

def get_input_descriptor():
    name=None
    while (name!='Page Network.csv'):
        name=raw_input('open what file: ')
    file_obj=open('Page Network.csv','r')
    return file_obj

def CreateGraph(G,file_object):
    "create the graph form the input file"
    pages=['A','B','C','D','E','F','G','H','I','J','K']
    for line in file_object:
        link=[]
        page,link1,link2,link3,link4,link5,link6,link7,link8,link9,link10,link11=line.split(",")
        G.addpage(page)
        link=[link1,link2,link3,link4,link5,link6,link7,link8,link9,link10,link11]
        i=0
        for l in link:
            if l=='1':
                G.links[page].append(pages[i])
            i+=1
    return G

def main():
    file_object=get_input_descriptor()
    G=Digraph()
    G= CreateGraph(G,file_object)
    print G.links
    statdist=PageRank(G)
    "nomorlize the stationary distribution"
    total=float(sum(statdist.values()))
    statdist = dict((page, prob /float(total)) for page, prob in statdist.items())
    
    for key in sorted(statdist.keys()):
                    print key+' prbability of stationary distrition:'+str(statdist[key])

main()


