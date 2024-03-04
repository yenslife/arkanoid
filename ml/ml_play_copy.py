"""
The template of the main script of the machine learning process
        
        Decide the command according to the received scene information
        scene_info be like:
        {
            "frame": 0,
            "status": "GAME_ALIVE",
            "ball": [ 93, 395],
            "ball_served": false,
            "platform": [ 75, 400],
            "bricks": [
                [ 50, 60],
                ...,
                [125, 80]
            ],
            "hard_bricks": [
                [ 35, 50],
                ...,
                [135, 90]
            ]
        }
        注意：這些座標都表示磚塊的左上角座標
        以左上角為基準點

"""
import pickle
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib

class MLPlay:
    def __init__(self,ai_name, *args, **kwargs):
        """
        Constructor
        """
        self.current_ball_x = 0
        self.current_ball_y = 0
        self.current_platform_x = 0
        self.previous_ball_x = 0
        self.previous_ball_y = 0
        self.num_of_bounce = 0
        print(ai_name)

    
    def update(self, scene_info, *args, **kwargs):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
                scene_info["status"] == "GAME_PASS"):
            return "RESET"
        if not scene_info["ball_served"]:
            command = "SERVE_TO_LEFT"
        else:
            # {'direction': 0, 'ball': (20, 63), 'ball_speed': (10, 7), 'platform_dir': 1}
            # 其中 direction 是模型的輸出 -1 表示向左 1 表示向右 0 表示不動
            # ball 是球的位置
            # ball_speed 是球的速度
            # platform_dir 是板子的移動方向
            self.previous_ball_x = self.current_ball_x
            self.previous_ball_y = self.current_ball_y
            self.current_ball_x = scene_info["ball"][0]
            self.current_ball_y = scene_info["ball"][1]
            
            # 讀取模型
            model_name = 'ml/model.pickle'
            
            loaded_model = joblib.load('model.sav')
            
            # 處理資料
            x = []
            y = []
            ball_direction = 0
            ball_direction_vector = (self.current_ball_x - self.previous_ball_x, self.current_ball_y - self.previous_ball_y)
            if ball_direction_vector[0] > 0 and ball_direction_vector[1] > 0:
                ball_direction = 0
            elif ball_direction_vector[0] > 0 and ball_direction_vector[1] < 0:
                ball_direction = 1
            elif ball_direction_vector[0] < 0 and ball_direction_vector[1] > 0:
                ball_direction = 2
            elif ball_direction_vector[0] < 0 and ball_direction_vector[1] < 0:
                ball_direction = 3
            x.append([ball_direction, self.current_ball_x, self.current_ball_y, ball_direction_vector[0], ball_direction_vector[1]])
            # 預測
            prediction = loaded_model.predict(x)
            print(prediction)
            # 輸出指令
            if prediction[0] == 1:
                command = "MOVE_RIGHT"
            elif prediction[0] == -1:
                command = "MOVE_LEFT"
            else:
                command = "NONE"
                  

        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
