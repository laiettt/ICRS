import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
#路徑是放Json檔的位置
cred = credentials.Certificate("D:/ETTT/ICRSS/serviceAccountKey.json")
#initialize是初始化的意思
if (not len(firebase_admin._apps)):
    firebase_admin.initialize_app(cred)
'''
     初始化firebase，注意不能重複初始化
     初始化firestore   
'''
db = firestore.client()
# ranks是一個集合，在其底下的叫 文件，並存於變數 collection_name

ranks_list=[]
col_list=[]
uid_list=[]
#path_2 表示要取得的 文件名稱
#這裡代表是 ranks 的文件
path_2 ="ranks"
#db.collection(文件名稱)，取得 ranks 的內容並存於變數 collection_ref
#.stream()方法類似 .get()，取得collection_ref的資料
collection_ref = db.collection(path_2)
docs = collection_ref.stream()
try:
    for doc in docs:
        ranks_list.append(doc.to_dict())
        uid_list.append(doc.to_dict()["uid"])
except:
    print("指定文件的路徑{}不存在，請檢查路徑是否正確".format(path_2))  
for i in ranks_list:
#   因為店家跟商品是分開的，所以先把他們串起來後丟到col_list裡面
    col_list.append(i.get('store')+'|'+i.get('item'))  
#pd.unique()方法是排除掉重複值，因為1個使用者可以有多個品項的評分
uid_uni =pd.unique(pd.Series(uid_list))
col_uni =pd.unique(pd.Series(col_list))
#建立新的DataFrame叫做rating_df，並設定列跟行的名稱
rating_df=pd.DataFrame(columns=uid_uni,index=col_uni)
#這裡的i一樣是代表每個dict
for i in ranks_list:
    store_item=i.get('store')+'|'+i.get('item')
    rating_df[i['uid']][store_item]=i['rank']
rating_df.to_csv('get_firestore_rating.csv',encoding="utf_8_sig")