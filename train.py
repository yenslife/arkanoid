import pickle
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


if __name__ == "__main__":
    # 讀取 ml/model.pickle
    data = []
    with open("ml/model.pickle", "rb") as f:
        data = pickle.load(f)
    with open("ml/model1.pickle", "rb") as f:
        data += pickle.load(f)
    with open("ml/model3.pickle", "rb") as f:
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
    model = KNeighborsClassifier(n_neighbors=10)
    # 訓練模型
    model.fit(X_train, y_train)
    # 預測
    print(model.predict(X_test))
    # 評估
    print(model.score(X_test, y_test))
    # 儲存模型
    filename = 'model.sav'
    pickle.dump(model, open(filename, 'wb'))
    
