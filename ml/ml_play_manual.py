"""
The template of the main script of the machine learning process
"""
import pygame
import os
import pickle


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
        self.ball_served = False

    def update(self, scene_info, keyboard=None, *args, **kwargs):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        self.previous_ball_x = self.current_ball_x
        self.previous_ball_y = self.current_ball_y
        self.current_ball_x = scene_info["ball"][0]
        self.current_ball_y = scene_info["ball"][1]
        if keyboard is None:
            keyboard = []
        if (scene_info["status"] == "GAME_OVER" or
                scene_info["status"] == "GAME_PASS"):
            return "RESET"

        if pygame.K_q in keyboard:
            command = "SERVE_TO_LEFT"
            self.ball_served = True
        elif pygame.K_e in keyboard:
            command = "SERVE_TO_RIGHT"
            self.ball_served = True
        elif pygame.K_LEFT in keyboard or pygame.K_a in keyboard:
            command = "MOVE_LEFT"
        elif pygame.K_RIGHT in keyboard or pygame.K_d in keyboard:
            command = "MOVE_RIGHT"
        else:
            command = "NONE"
        # 搜集資料
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
