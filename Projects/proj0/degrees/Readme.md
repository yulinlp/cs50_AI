#Degree实验重要的几个点：  
1.把实际问题抽象为搜索问题：  
Node.state <=> person_id  
Node.action <=> which movie the person from <=> movie_id  
Node.parent <=> which pre_neighbour the person have <=>last person_id  
2.利用Queue数据结构来完成广度优先搜索：  
用source初始化Queue->出队一个Node，经过判断是否为target，若不是就把其邻居节点入队->循环  
3.利用explored_set跟踪入过队的Node，防止duplication  
