import pickle
import os
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report


def load_data_from_pickle(folder_path):
    """
    从指定文件夹加载 pickle 格式的数据
    """
    data = []
    data_files = os.listdir(folder_path)
    for file in data_files:
        with open(os.path.join(folder_path, file), 'rb') as f:
            data += pickle.load(f)
    return data


def preprocess_data(data):
    """
    数据预处理：提取特征和标签，并进行标准化处理
    """
    X = np.array([[d['ball'][0], d['ball'][1], d['ball_speed'][0], d['ball_speed'][1], d['platform_dir']] for d in data])
    y = np.array([d['direction'] for d in data])
    
    # 数据标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y


def train_model(X_train, y_train):
    """
    使用网格搜索交叉验证来训练 KNN 模型并返回最佳模型
    """
    knn = KNeighborsClassifier()
    param_grid = {'n_neighbors': [3, 5, 7, 10]}
    grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='accuracy')
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
