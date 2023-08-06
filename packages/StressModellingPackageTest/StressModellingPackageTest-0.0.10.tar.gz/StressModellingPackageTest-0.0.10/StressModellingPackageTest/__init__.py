import pandas as pd
import math
# !pip install networkx[default]
# !pip install matplotlib==3.1.3
import networkx as nx
import numpy as np
np.random.seed(1000)
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


def init_graph_attr1(G,crop,statesList,taluk_attri_Dict,states,df): 
  nodeAttr = {}
  dis= statesList
  init_graph1(G,states,crop,dis,statesList,df)
  for i in range(len(states)):
      temp = {}
      temp['OldDeltaVector'] = np.zeros(2)
      temp["DeltaVectornodesStress"] = 0 
      temp['NewDeltaVector'] = np.zeros(2)
      temp["sdgvec"] = taluk_attri_Dict[dis[i]]
      temp["tempsdgvec"] = taluk_attri_Dict[dis[i]]
      temp["oldsdgvec"] = taluk_attri_Dict[dis[i]]
      temp["nodesStress"] = 0
      temp["meansdg"] = np.mean(taluk_attri_Dict[dis[i]])
      temp["name"] = dis[i]
      # temp["Tempsdgvec"] = stateSDGDict[i] 
      nodeAttr[i] = temp
  print(nodeAttr)
  nx.set_node_attributes(G, nodeAttr)

def init_graph1(G,states,crop,dis,statesList,df): #states is a dataframe
    G.add_nodes_from([i for i in range(0,len(states))])
    # print(len(states))
    labels = {}
    for i in range(len(states)):
       labels[i] = statesList[i]
       snode=states['S.NO'][i]-1
       temp=states['Neighbours_ID'][i]
       #print(temp)
       if ',' in str(temp):
          sedge_arr=states['Neighbours_ID'][i].split(',')
          #print(sedge_arr)
          for i in range(0,len(sedge_arr)):
              G.add_edge(snode,int(sedge_arr[i])-1)
              
       elif math.isnan(temp) :
          print()
       else :
          G.add_edge(snode,temp-1)
          # print(snode,temp-1)
    my_pos = nx.spring_layout(G, seed = 1000)
    node_sizes = df[crop]*3000
    print(statesList)
    H1=nx.draw(G,pos=my_pos,with_labels=True, labels=labels,node_size=node_sizes,node_color=df[crop].astype(float)*300, cmap=plt.cm.Blues)
    return 

def getMeanSDGGraph2(G,label,num):
  meanSDG = 0
  for n in G.nodes():
    meanSDG += np.mean(np.array(G.nodes[n][label]))
  #print(meanSDG," ",num)
  return meanSDG / num

def getGraphStress2(G,label):
  for n in G.nodes():
    nodeStress = 0
    neigList = list(G.neighbors(n))
    for nei in neigList:
      a = np.array(G.nodes[n][label])
      b = np.array(G.nodes[nei][label])
      nodeStress += np.linalg.norm((a - b), ord=1)
    G.nodes[n]["nodesStress"] = nodeStress
    
  stress = 0
  for n in G.nodes():
    stress += G.nodes[n]["nodesStress"]
  return stress

def StressReduction(G, label1,label2,numSDG):
  for n in G.nodes():
      nodeStress = 0
      neigList = list(G.neighbors(n))
      a = np.zeros(numSDG)
      for nei in neigList:
        a = np. add(a,np.array(G.nodes[nei][label1]))
      if len(neigList)!=0:
        a = a/len(neigList)
        G.nodes[n][label2] = np.add(G.nodes[n][label2],np.add(a,-1*np.array(G.nodes[n][label1]))).tolist()
  for n in G.nodes():
    G.nodes[n][label1] = G.nodes[n][label2].copy()
  return 


def graphCalliberation(numRounds,EpsilonStress,crop,statesList,numSDG,final,attribute_list,taluk_attri_Dict,states,df):
  statesDict = {}
  for i in statesList:
    statesDict[i] = []
  G3= nx.Graph()
  MeanSDGs = []
  MeanStress = [] 
  XAxis = []
  init_graph_attr1(G3,crop,statesList,taluk_attri_Dict,states,df)
  # print("Punjabs SDG 5 after Policy Intervention:",G2.nodes[19]['sdgvec'])
  # PolicyIntervention(G,label,nodeIDs,Policies)
  for i in range(numRounds):
    temp1 = getMeanSDGGraph2(G3,"sdgvec",13)
    temp2 = getGraphStress2(G3,"sdgvec")
    XAxis.append(i)
    #print(" Mean SDG Graph is: ",temp1," Graph Stress is:",temp2)
    MeanSDGs.append(temp1)
    MeanStress.append(temp2)
    for n in G3.nodes(): 
      print(G3.nodes[n]["name"])
      statesDict[G3.nodes[n]["name"]].append(G3.nodes[n]["sdgvec"])
    if temp2>=EpsilonStress:
      # PolicyIntervention(G,Policies,NodeIDs,numSDGs,label)
      StressReduction(G3,"sdgvec" ,"tempsdgvec",numSDG)
    else:
      break
  for n in G3.nodes(): 
    statesDict[G3.nodes[n]["name"]].append(G3.nodes[n]["sdgvec"])
  # data_to_append= []
  # for n in G3.nodes():
  #   data_to_append.append(np.array([n+1]+G3.nodes[n]['sdgvec']))
  #   print([n+1]+G3.nodes[n]['sdgvec']) 
  # df_new = pd.DataFrame(np.array(data_to_append), 
  #            columns=["agroClimaticZone"]+attribute_list)
  # node_sizes = df_new[crop]
  my_pos = nx.spring_layout(G3, seed = 1000)
  labels = {}
  for i in range(len(G3.nodes())):
    labels[i] = statesList[i]
  H2=nx.draw(G3,pos=my_pos,with_labels=True,labels=labels,node_size=node_sizes)
  return statesDict


def StressModelling(numNodes,numSDG,numOfRounds,BeforeATEFile,AfterATEFile,adjList):
    # Importing neccessary libraries
 

    # numNodes = 10  # Input 
    # numSDG = 2  #Input
    # numOfRounds = 3 #Input 
    myseed = 1000
    epsilonStress = 0.5
    maxRounds = 1000 
    numPolicies = 100
    # BeforeATEFile = "/content/sample_data/ATEAfter.xlsx" #Input 
    # AfterATEFile = '/content/sample_data/ATEBefore.xlsx' #Input 
    # adjList = '/content/sample_data/Adjacent list ac zones.xlsx' #Input 
    df = pd.read_excel(BeforeATEFile)
    df2=pd.read_excel(AfterATEFile)
    attribute_list= list(df.columns[2:])
    labels = list(df[df.columns[1]])
    print(attribute_list)
    print(labels)

    df['sdgvec'] = df[attribute_list].values.tolist()
    taluk_attri_Dict = dict(zip(df[df.columns[1]], df.sdgvec))
    df2['sdgvec'] = df2[attribute_list].values.tolist()
    states=pd.read_excel(adjList)
    statesList = list(states[states.columns[1]])
    # G1 = nx.Graph()
    # init_graph_attr1(G1,attribute_list[0])
    final = {}
    return graphCalliberation(numOfRounds,epsilonStress,attribute_list[0],statesList,numSDG,final,attribute_list,taluk_attri_Dict,states,df)