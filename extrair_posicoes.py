# used libs
import cv2
import numpy as np
import pandas as pd
import os

video_path = 'pendulo.mp4' 

if not os.path.exists(video_path):
    print(f"ERRO: Arquivo {video_path} não encontrado no diretório atual!")
    exit()

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("ERRO: Não foi possível abrir o vídeo.")
    exit()

# useless info
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"FPS: {fps}")
print(f"Total de Frames: {frame_count}")

# data storage list
data = []
frame_num = 0

# color bounds used to find object
lower_bound_hsv = np.array([0, 0, 0])      
upper_bound_hsv = np.array([180, 255, 80]) 

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # converts to hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # mask to isolate object
    mask = cv2.inRange(hsv, lower_bound_hsv, upper_bound_hsv)
    
    # limits of the object
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # processes largest contour
    if contours:
        # largest contour 
        largest_contour = max(contours, key=cv2.contourArea)
        
        # calculates moments for center of mass
        M = cv2.moments(largest_contour)
        
        if M["m00"] != 0:
            # center of mass coodinates
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            
            # find time
            time_s = frame_num / fps
            
            # store data
            data.append({
                'frame': frame_num,
                'tempo': time_s,
                'x': cX,
                'y': cY
            })
                    
    frame_num += 1


cap.release()
# cv2.destroyAllWindows()

# saves to csv
df_output = pd.DataFrame(data)
df_output.to_csv('dados_pendulo.csv', index=False)
print("\n" + "=" * 50)
print(f"Sucesso! Dados salvos em 'dados_pendulo.csv'")
print(f"Frames processados: {frame_num}")
print("=" * 50)