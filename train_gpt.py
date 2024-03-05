import pickle
import os
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import StratifiedShuffleSplit

def load_data_from_pickle(folder_path):
    """
    从指定文件夹加载 pickle 格式的数据
    """
    data = []
    data_files = os.listdir(folder_path)
    for file in data_files:
        if os.path.getsize(os.path.join(folder_path, file)) > 0: # Pickle - EOFError: Ran out of input
            with open(os.path.join(folder_path, file), 'rb') as f:
                try: # Pickle - EOFError: Ran out of input
                    data += pickle.load(f)
                except Exception as e:
                    print(e, file)
    return data


def preprocess_data(data):
    """
    資料預處理：提取特徵(切記這邊不用標準化，因為這樣模型會抓不到特徵)
    """
    X = np.array([[d['ball'][0], d['ball'][1], d['ball_speed'][0], d['ball_speed'][1], d['direction'], d['platform_x']] for d in data])
    y = np.array([d['platform_dir'] for d in data])
    
    return X, y


def train_model(X_train, y_train):
    """
    使用网格搜索交叉验证来训练 KNN 模型并返回最佳模型
    """
    knn = KNeighborsClassifier()
    # param_grid = {'n_neighbors': [3, 5, 7, 13, 17, 19]}
    # param_grid = {'n_neighbors': [3, 5, 7]}
    # param_grid = {'n_neighbors': [13]}
    param_grid = {'n_neighbors': range(1, 5)}
    cv = StratifiedShuffleSplit(n_splits=2, test_size=0.3, random_state=12)
    # grid_search = GridSearchCV(knn, param_grid, cv=cv, scoring='accuracy', verbose=3)
    grid_search = GridSearchCV(knn, param_grid, cv=cv, verbose=3, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    
    best_knn = grid_search.best_estimator_
    print("Best parameters:", grid_search.best_params_)
    print("Best cross-validation score:", grid_search.best_score_)
    
    return best_knn


def evaluate_model(model, X_test, y_test):
    """
    评估模型性能并打印评估结果
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Test accuracy:", accuracy)
    print("Classification report:")
    print(classification_report(y_test, y_pred))


if __name__ == "__main__":
    # 加载数据
    data_folder = 'data_pickle'
    data = load_data_from_pickle(data_folder)
    print(f"資料筆數：{len(data)}")
    
    # 数据预处理
    X, y = preprocess_data(data)
    
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 训练模型
    print("Training model...")
    best_knn = train_model(X_train, y_train)
    
    # 评估模型
    print("\nEvaluating model on test data...")
    evaluate_model(best_knn, X_test, y_test)
    
    # 保存模型
    model_filename = 'best_knn_model.sav'
    with open(model_filename, 'wb') as f:
        pickle.dump(best_knn, f)
    print(f"Model saved as '{model_filename}'")
    pickle.dump(best_knn, open(model_filename, 'wb'))
