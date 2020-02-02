# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 14:11:26 2019

@author: 賴奕廷
"""
import math
import firebase_test 
#os.system("python D:/ETTT/firebase_project/firebase_test.py")
class recommender():
    def __init__(self,path,user): #__inin__會直接執行，不需要被呼叫
        self.path =path  #self.path表示在 __init__這個function的變數，後面的path是外面傳進來的
        self.user =user  #跟上面一樣
        self.user_rating ={} #建立self.user_rating 這個字典來存放User之間共同評分過的
        self.load_data(path) #呼叫self.load_data這個function，並把path傳過去
    def load_data(self,path):
        #打開path這個路徑的檔案並存於變數 f
#        因為檔案編碼是UTF-8-BOM，所以要先轉換成UTF-8
        with open(path,encoding="utf-8") as f: 
            lines = f.readlines() #讀取 f裡面的資料存於變數 lines
        user_name =[]  #建立一個叫 user_name 的list來放 User1~User10
        for i in lines[0].strip().split(',')[1:]: # 欄位的部分不跑，所以從lines[1]開始到最後一列
            user_name.append(i) #將每個 i存入list裡面，也就是User1~User10存入user_name[]
            '''
            直接print(line[0])------> ,User1,User2,User3,User4,User5,User6,User7,User8,User9,User10
            print(line[0].strip())--->,User1,User2,User3,User4,User5,User6,User7,User8,User9,User10
            雖然結果一樣，但是python有自動換行，所以strip()功用可以把字串的頭尾空白給刪除
            也就是把隱形的 \n拿掉
            split(',')能把字串透過 '逗號' 分割 並回傳成一個list
            輸出結果----------->['User1', 'User2', 'User3', 'User4', 'User5', 'User6', 'User7', 'User8', 'User9', 'User10']
            若少了strip()這個動作，
            輸出結果會變成----->['User1', 'User2', 'User3', 'User4', 'User5', 'User6', 'User7', 'User8', 'User9', 'User10','\n']
            '''
        for i in lines[1:]: #從第1列開始跑，因為欄位在第0欄
            foods = i.strip().split(',')
            food =foods[0].strip()
            for index in range(1,len(foods)): #len(foods)=11
                if not foods[index]=='':#如果foods 沒有空白的， 也就是有評分的
                    if user_name[index-1] not in self.user_rating:#若self.user_rating沒有user_name[index-1]這個值
                        self.user_rating[user_name[index-1]]={food:int(foods[index])}
                    else:
                        self.user_rating[user_name[index-1]][food] = int(foods[index])
            #print(self.user_rating)
            '''
            print(i)--->Food1,,4,5,4,5,4,,,2,4  ~Food7 的資料
            用strip()來去頭尾的空白以及隱藏的\n，再用split(',')函式利用逗號分割字串並回傳成一個list
            由變數foods接收-->['Food1', '', '4', '5', '4', '5', '4', '', '', '2', '4']...
                             ['Food7', '', '4', '', '3', '4', '4', '4', '2', '', '2']
            再取foods的第0欄位，也就是Food1 ~Food7到變數food
  
            實際跑一次迴圈:
                i從line[1]開始跑，所以foods =['Food1', '', '4', '5', '4', '5', '4', '', '', '2', '4']
                                     food =Food1
                index從1開始跑，所以if not foods[index]==''這個條件式
                                   等同於 if not foods[1]==''
                                   對上去看food[1]剛好是''，所以不符合條件，
                index換2去跑，foods[2]=4，符合條件，進入到下一個條件句
                if user_name[index-1] not in self.user_rating這句等同下面那句
                if user_name[2-1] not in self.user_rating，而一開始我們是建立空的dict，換言之
                裡頭根本不會有user_name[1]，也就是User2的資料，所以會執行下面這段
                self.user_rating[user_name[index-1]]={food:int(foods[index])}，
                self.user_rating[User2]={Food1:4}，第一個關聯資料就存入
            假設i跑到line[2]，所以foods=['Food2', '', '5', '', '', '4', '5', '5', '5', '', '4']
                                 food =Food2
                index換2去跑，所以foods[2]=5，而if user_name[index-1] not in self.user_rating這句
                user_name[1]=User2，self.user_rating已經有User2的資料，所以跑
                self.user_rating[user_name[index-1]][food] = int(foods[index])，
                self.user_rating[User2[Food2]]=5
                
            '''
    def pearson_distance(self,usr1,usr2):
        sum_x_y = 0
        sum_x = 0
        sum_y = 0
        sum_x_2 = 0
        sum_y_2 = 0
        n = 0
        for movie in usr1.keys():
            if movie in usr2.keys():
                n += 1
                x = usr1[movie]
                y = usr2[movie]
                sum_x_y += x*y
                sum_x += x
                sum_y += y
                sum_x_2 += x**2
                sum_y_2 += y**2
        if n==0:return 0
        denominator = math.sqrt(sum_x_2-float(sum_x**2)/n) * math.sqrt(sum_y_2-float(sum_y**2)/n)
        if denominator==0:return 0
        return (sum_x_y - float(sum_x*sum_y)/n)/denominator
    def recomend_k(self,neatst,k):
        recommend = {}
        total_distance = 0
        for item in neatst: 
            total_distance+=item[1]
        for item in neatst:
            u_name = item[0]
            weight = float(item[1])/total_distance
            for movie,rate in self.user_rating[u_name].items():
                if movie not in self.user_rating[self.user].keys():
                    if movie not in recommend.keys():
                        recommend[movie] = rate*weight
                    else:
                        recommend[movie] += rate*weight
        #print(recommend)   
        top_k = list(recommend.items())
        top_k.sort(key=lambda x:x[1],reverse=True)
        if k>len(top_k):return top_k
        else:return top_k[:k]
    def k_nearst(self,k):
        distances = []
        for usr,rate in self.user_rating.items():
            if not usr == self.user:
                distance = self.pearson_distance(self.user_rating[self.user],self.user_rating[usr])
                if distance != 0:distances.append((usr,distance))        
        distances.sort(key=lambda item:item[1],reverse=True)
        #print(distances)u
        if k>len(distances):return distances
        else:return distances[:k]            
    def run(self):
        nearst = self.k_nearst(5)
        top_k = self.recomend_k(nearst,5)
        for item in top_k:
            print("為您推薦的食物:{} 推薦指數:{}".format(item[0],str(item[1]))) 
path ='D:/ETTT/ICRSS/get_firestore_rating.csv'
user_str = str(input("請輸入姓名:"))
print("{}您好! ".format(user_str))
a =recommender(path,user_str) #建立變數 a 來呼叫reconnender 並將參數傳出去
a.run()