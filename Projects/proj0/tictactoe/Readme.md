# Tictactoe实验重要的几个点：  
## 1.核心是minimax算法  
minimax算法可以这样来理解：  
假设我现在是Player_X，那么我下一步的action1必须使得newBoard对于Player_O来说是不利的。  
#### 但是我应该换位思考，如果我进行action1，那么Player_O也会进行一个action2，从而尽可能地提高他的得分。  
双方会在这种博弈下做出各自的最优解
## 2.minimax的几个关键点  
#### 首先，假定博弈双方都是极为保守的理性人。即：对于我的actions，我会得到newBoards，对于newBoards我会推想对方的actions从而得到newnewBoards。
此时我可以通过某种方式预知newnewBoards的分数，但我会评估每个newBoard对应的newnewBoards，找出最低分来代表我的newBoard的分数。  
这是因为，我是极为保守的并且对方也是极具智慧的，所以我应该在最劣情况下找到最优解。  
#### 其次，minimax是一个极为漫长的递归过程。  
在博弈开始的初期，先行者的选择是非常多的，他需要对每个选择进行推演再推演（递归），从而得到optimal choice。在这种情况下，计算量是非常大的。  
## 3.对minimax算法的优化  
目前有两个思路
#### 一是，限制递归深度，从而减少不必要的时间开销。  
#### 二是，对newBoard的分数评价使用贪婪算法（剪枝？）。  
具体的说，是保存目前max的min分数值，记为tmp_score，在对newBoard的评价过程中，如果有一个newnewBoard的分数低于tmp_score，则立即终止对这一支（newBoard）的评估，从而减少不必要的时间开销。  
