import math
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
def init_firebase():
    cred = credentials.Certificate("D:/ETTT/ICRSS/serviceAccountKey.json")
    if (not len(firebase_admin._apps)):
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    path_2 ="stores"
    collection_ref = db.collection(path_2)
    docs = collection_ref.stream()
    return docs
def get_firebase_data(docs):  
    data = {}
    locat_dict={}
    stores_list=[]
    try:
        for doc in docs:
            stores_list.append(doc.to_dict()["name"])
            a=doc.to_dict().pop('name')
            b=doc.to_dict().pop('long')
            c=doc.to_dict().pop('lati')
            locat_dict[a]=c+","+b
        data['locat_dict'] = locat_dict
        data['stores_list'] = stores_list
        return data
    except:
        print("指定文件的路徑{}不存在，請檢查路徑是否正確".format(path_2))
#print(locat_dict)
def distance(lat1,lon1,lat2,lon2):#之後要將使用者的lat2和lon2改寫
#    lat2 =22.726330
#    lon2 =120.314498
    radius = 6371 # km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
#    round(x,y)======>x取小數點到第y位
    return round(d,2)
#print(distance(22.724545,120.314968))
    # firebase connect init function init_firebase()
    # get firebase data functiuon stores_list, locat_list=get_firebase data()
    # 
    # done
def get_store_locate(store,lat2,lon2, datalist):
#因為推薦出來的產品是店家+商品 ex:品味達人牛肉麵
#所以讓 i去跑所有店家的名稱，如果店家+商品有包含 i的話，就代表找到店家
#第二個迴圈跑的是 找到店家名稱後，去找到到相對應的經緯度
#再利用.split()，用逗號分割得到緯度跟經度傳到 distance這個function計算距離
    stores_list = datalist['stores_list']
    locat_dict = datalist['locat_dict']
    for i in stores_list:
        store = store.split('|')[0]
        for j in locat_dict:
            if j ==store:  
                up_lac =locat_dict[j].split(',')
                d=distance(float(up_lac[0]),float(up_lac[1]),lat2,lon2)
                return d
#                   print("距離海科大門口是{} Km".format(distance(float(up_lac[0]),float(up_lac[1]))))       
#find_store = str(input("請輸入店家:"))
#print(get_store_locate(find_store,22.726330,120.314498))