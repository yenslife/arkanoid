"""
The template of the main script of the machine learning process
"""
import random
import pickle
import os

class MLPlay:
    def __init__(self,ai_name, *args, **kwargs):
        """
        Constructor
        """
        self.current_ball_x = 0
        self.current_ball_y = 0
        self.previous_ball_x = 0
        self.previous_ball_y = 0
        self.target_x = 0
        self.data = []
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
            self.previous_ball_x = self.current_ball_x
            self.previous_ball_y = self.current_ball_y
            self.current_ball_x = scene_info["ball"][0]
            self.current_ball_y = scene_info["ball"][1]
            # 正在下降且在判斷區
            if (scene_info['ball'][1] > self.previous_ball_y) and (0 < scene_info['ball'][1] < 400) and (10 < scene_info['ball'][0] < 190):
                time = ((395 - scene_info['ball'][1]) / (scene_info['ball'][1] - self.previous_ball_y))
                step = time * (scene_info['ball'][0] - self.previous_ball_x)
                Eular = (step + scene_info['ball'][0] + 780) % 390
                if Eular > 195:
                    self.target_x = 390 - Eular
                else:
                    self.target_x = Eular

            err = random.randint(-5, 5)
            if self.target_x > scene_info["platform"][0] + 20 + err:
                command = "MOVE_RIGHT"
            elif self.target_x < scene_info["platform"][0] + 20 + err:
                command = "MOVE_LEFT"
            else:
                command = "NONE"

        if (scene_info['ball'][1] > self.previous_ball_y):
            # 如果球正在下降才要搜集資料
            data_dir = {}
            # 右下0 右上1 左下2 左上3
            data_dir['direction'] = 0
            ball_direction_vector = (self.current_ball_x - self.previous_ball_x, self.current_ball_y - self.previous_ball_y)
            if ball_direction_vector[0] > 0 and ball_direction_vector[1] > 0:
                data_dir['direction'] = 0
            elif ball_direction_vector[0] > 0 and ball_direction_vector[1] < 0:
                data_dir['direction'] = 1
            elif ball_direction_vector[0] < 0 and ball_direction_vector[1] > 0:
                data_dir['direction'] = 2
            elif ball_direction_vector[0] < 0 and ball_direction_vector[1] < 0:
                data_dir['direction'] = 3
            data_dir['ball'] = (self.current_ball_x, self.current_ball_y)

            # 球的 x 方向以及 y 方向的速度
            data_dir['ball_speed'] = ball_direction_vector

            # 平台移動方向 -1 向左 1 向右 0 不動
            if command == "MOVE_LEFT":
                data_dir['platform_dir'] = -1
            elif command == "MOVE_RIGHT":
                data_dir['platform_dir'] = 1
            else:
                data_dir['platform_dir'] = 0
        
            self.data.append(data_dir)
        

        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
        pickle_list = os.listdir('data_pickle')
        pickle_list = [int(i.replace('.pickle', '').replace('num', '')) for i in pickle_list]
        pickle_list = sorted(pickle_list, key=lambda x: x, reverse=False)
        print(pickle_list)
        number = 0 if len(pickle_list) == 0 else pickle_list[-1] + 1
        filename = f'data_pickle/num{number}.pickle'
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)
