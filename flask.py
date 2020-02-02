from flask import Flask, request
import get_firebase_to_csv
import math
import get_location
import sys
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST']) 
def In():
    if request.method == 'POST':
        class recommender():
            def __init__(self,path,user,lat,lon): #__inin__會直接執行，不需要被呼叫
                self.path =path  #self.path表示在 __init__這個function的變數，後面的path是外面傳進來的
                self.user =user  #跟上面一樣
                self.user_rating ={} #建立self.user_rating 這個字典來存放User之間共同評分過的
                self.load_data(path) #呼叫self.load_data這個function，並把path傳過去
                self.lat=lat
                self.lon=lon
            def load_data(self,path):

                with open(path,encoding="utf-8") as f: 
                    lines = f.readlines() #讀取 f裡面的資料存於變數 lines
                user_name =[]  #建立一個叫 user_name 的list來放 User1~User10
                for i in lines[0].strip().split(',')[1:]: # 欄位的部分不跑，所以從lines[1]開始到最後一列
                    user_name.append(i) #將每個 i存入list裡面，也就是User1~User10存入user_name[]
                for i in lines[1:]: #從第1列開始跑，因為欄位在第0欄
                    foods = i.strip().split(',')
                    food =foods[0].strip()
                    for index in range(1,len(foods)): #len(foods)=11
                        if not foods[index]=='':#如果foods 沒有空白的， 也就是有評分的
                            if user_name[index-1] not in self.user_rating:#若self.user_rating沒有user_name[index-1]這個值
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
            def run(self, datalist):
                nearst = self.k_nearst(5)               
                top_k = self.recomend_k(nearst,5)   
                response = []
                g={}
#                print(top_k)
                for item in top_k:
                    response.append("{}{}".format(item[0],str(item[1])))  
                    g[item[0]]=get_location.get_store_locate(item[0],self.lat, self.lon, datalist)
#                    g.append(get_location.get_store_locate(item[0],self.lat, self.lon, datalist))
                return g
                   # return response
        docs = get_location.init_firebase()
        datalist = get_location.get_firebase_data(docs)
        path ='D:/ETTT/ICRSS/get_firestore_rating.csv'
        username = request.values['username']
        lat = float(request.values['lat'])
        lon = float(request.values['lon'])
        a =recommender(path,username,lat,lon) #建立變數 a 來呼叫reconnender 並將參數傳出去      
        response = a.run(datalist)            
        return str(response)
    return "<form method='post' action='/'>Uid:<input type='text' name='username' />" \
            "</br>" \
            "<form method='post' action='/'>Lat:<input type='text' name='lat' />" \
            "</br>" \
            "<form method='post' action='/'>Lon:<input type='text' name='lon' />" \
            "</br>" \
           "<button type='submit'>Submit</button></form>"
if __name__ == '__main__':
    app.debug = True
    app.run()    
