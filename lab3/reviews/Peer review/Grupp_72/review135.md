### **Lab 3 peer review**

* Reviewing group number: 135  
* Submitting group number: 72

### **Section 1: Core functionality**

1. Does the application run? yes  
2. Does the application display the complete map of tram lines? yes  
3. Is it possible to query shortest path between any two points? yes  
4. Does the application deal with changes correctly? yes  
5. Does the application show current traffic information? yes  
6. Does the application correctly handle invalid input? yes

### **Section 2: Code quality**

The overall code quality is good. The names chosen for functions and variable names inform the reader about what different items do. Group 135 doesn't include unnecessary strings and code which makes the overall appearance good. 

The code from lab2 is reused in Tramviz. For example they write “network=readTramNetwork()” and use it in their Dijkstra function.

Djikstra is used two times in Tramviz: “time, quickpath=djikstra(network, dep, cost=network.specialized\_transition\_time” and “distance, shortpath \=djikstra(network, dep, cost=network.specialized\_geo\_distance)”. Different distances are obtained depending on “dep” which is in the show\_shortest function. 

### **Section 3: Screenshots**

Included in the review map in GitLab.