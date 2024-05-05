import TrichRutDacTrung as ft
import os
from Class import Feature
import LuuTruDacTrung as luu
import jsonpickle as json
import mysql.connector

# Kết nối đến MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="quanghuy123",
  database="features"
)
mycursor = mydb.cursor()
# Đường dẫn đến thư mục chứa các file
folder_path = 'data'

# Lấy tất cả các file trong thư mục
files = os.listdir(folder_path)
print(files)
listFeatures = []
dictionary_list=[]
def test():
    for file in files:
        features = ft.features(os.path.join(folder_path, file))
        for feature in features:
            # feature = Feature(link=os.path.join(folder_path, file), feature=feature)
            listFeatures.append(feature)
            dictionary={file:feature}
            dictionary_list.append(dictionary);
    print('hello')
    print(dictionary_list)
test();

# def save(dictionary_list):
#     data_json = json.dumps(dictionary_list)
#     with open("features/data.json", "w") as file:
#         file.write(data_json)
# save(dictionary_list)
data=dictionary_list
for item in data:
    for key, values in item.items():
        sql = "INSERT INTO features (ten_file, zeroCrossingRate, averageEnergy, averageFrequency, frequencyVariation, averagePitch, pitchVariation) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (key, values[0], values[1], values[2], values[3], values[4], values[5])
        mycursor.execute(sql, val)

# Xác nhận các thay đổi
mydb.commit()

print(mycursor.rowcount, "record inserted.")

# Clusters = luu.ClusterUseKmeans(listFeatures)

# # Luu vào file json
# luu.save(Clusters)