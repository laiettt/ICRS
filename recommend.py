# -*- coding: utf-8 -*-
import math
import get_firebase_to_csv 
class recommender():
    def __init__(self,path,user):
        self.path =path
        self.user =user
        self.user_rating ={}
        self.load_data(path)
    def load_data(self,path):
        with open(path,encoding="utf-8") as f: 
            lines = f.readlines()
        user_name =[]
        for i in lines[0].strip().split(',')[1:]:
            user_name.append(i)
        for i in lines[1:]:
            foods = i.strip().split(',')
            food =foods[0].strip()
            for index in range(1,len(foods)):
                if not foods[index]=='':
                    if user_name[index-1] not in self.user_rating:
                        self.user_rating[user_name[index-1]]={food:int(foods[index])}
                    else:
                        self.user_rating[user_name[index-1]][food] = int(foods[index])
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
a =recommender(path,user_str)
a.run()