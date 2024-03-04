import pickle
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import os


if __name__ == "__main__":
    # 讀取 ml/model.pickle
    data = []
    data_list = os.listdir('data_pickle') 
    for file in data_list:
        with open(f'data_pickle/{file}', 'rb') as f:
            data += pickle.load(f)


    # 資料處理 {'ball': (0, 0), 'ball_speed': (0, 0), 'platform_dir': 0}
    x = []
    y = []
    for i in data:
        x.append([i['ball'][0], i['ball'][1], i['ball_speed'][0], i['ball_speed'][1], i['platform_dir']])
        y.append(i['direction'])

    # 切割資料
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # 建立模型
    model = KNeighborsClassifier(n_neighbors=30)
    # 訓練模型
    print('訓練模型中')
    model.fit(X_train, y_train)
    print('訓練結束')
    # 預測
    print(model.predict(X_test))
    # 評估
    print(model.score(X_test, y_test))
    # 儲存模型
    filename = 'model.sav'
 
