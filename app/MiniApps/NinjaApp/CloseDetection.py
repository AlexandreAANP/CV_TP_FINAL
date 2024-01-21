import time
class CloseDetection:
    def __init__(self, seconds_to_close:int, width:int, height:int):
        self.timer = None
        self.seconds_to_close = seconds_to_close
        self.width = width
        self.height = height

    
    def should_close(self, landmarks):
        if not landmarks or not landmarks.pose_landmarks:
            return False
        if self.__are_arms_crossed(landmarks.pose_landmarks.landmark):
            if not self.timer:
                self.timer = time.time()
            else:
                if time.time() - self.timer > self.seconds_to_close:
                    self.timer = None
                    return True
        return False
    
    
    def __are_arms_crossed(self, landmarks):
        R_ELBOW = self.__convert_coords_to_pixel_position((landmarks[14].x, landmarks[14].y))  
        R_WRIST = self.__convert_coords_to_pixel_position((landmarks[15].x, landmarks[15].y))
        L_ELBOW = self.__convert_coords_to_pixel_position((landmarks[13].x, landmarks[13].y)) 
        L_WRIST = self.__convert_coords_to_pixel_position((landmarks[16].x, landmarks[16].y))
        rigth_line = self.__equation_of_line(R_ELBOW, R_WRIST)
        left_line = self.__equation_of_line(L_ELBOW, L_WRIST)
        return self.__check_if_lines_cross_in_range(rigth_line, left_line, (0, self.width))
    
    def __convert_coords_to_pixel_position(self, coords:tuple):
        x = coords[0]
        y = coords[1]
        if x < 0:
            x = 0
        if x > 1:
            x = 1
        if y < 0:
            y = 0
        if y > 1:
            y = 1
        return (int(coords[0]*self.width), int(coords[1]*self.height))  
    
    def __check_if_lines_cross_in_range(self, line1:tuple, line2:tuple, range:tuple):
        divisor = line1[0] - line2[0]
        if divisor == 0:
            return False
        crossed_point_x = line2[1] - line1[1] / divisor
        if crossed_point_x > range[0] and crossed_point_x < range[1]:
            return True
        return False
    def __equation_of_line(self, point1, point2):
        # y = mx + b
        # m = (y2-y1)/(x2-x1)
        # b = y1 - m*x1
        if point2[0] - point1[0] == 0:
            return (0, 0)
        m = (point2[1] - point1[1]) / (point2[0] - point1[0])
        b = point1[1] - m * point1[0]
        return (m, b)