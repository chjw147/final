import math
from pydantic import BaseModel
import cv2
import matplotlib.pyplot as plt
import numpy as np
from werkzeug.utils import secure_filename

right_shoulder_S_ct=0
right_shoulder_C_ct=0
right_shoulder_D_ct=0
right_shoulder_U_ct=0
    
left_shoulder_S_ct=0
left_shoulder_C_ct=0
left_shoulder_D_ct=0
left_shoulder_U_ct=0
    
right_knee_S_ct=0
right_knee_C_ct=0
right_knee_D_ct=0
right_knee_U_ct=0
    
left_knee_S_ct=0
left_knee_C_ct=0
left_knee_D_ct=0
left_knee_U_ct=0
    
waist_S_ct=0
waist_C_ct=0
waist_D_ct=0
waist_U_ct=0

# 앵글 계산 함수
def calculateAngle(point1_x, point1_y, point2_x, point2_y, point3_x, point3_y):

    # Get the required landmarks coordinates.
    x1, y1 = point1_x, point1_y
    x2, y2 = point2_x, point2_y
    x3, y3 = point3_x, point3_y
    
    # Calculate the angle between the three points
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    
#     # Check if the angle is less than zero.
#     if angle < 0:

#         # Add 360 to the found angle.
#         angle += 360
    
    # Return the calculated angle.
    return angle

def extract_keypoint(frame, result_keypoint, display=False):
    class GetKeypoint(BaseModel):
        NOSE:           int = 0
        LEFT_EYE:       int = 1
        RIGHT_EYE:      int = 2
        LEFT_EAR:       int = 3
        RIGHT_EAR:      int = 4
        LEFT_SHOULDER:  int = 5
        RIGHT_SHOULDER: int = 6
        LEFT_ELBOW:     int = 7
        RIGHT_ELBOW:    int = 8
        LEFT_WRIST:     int = 9
        RIGHT_WRIST:    int = 10
        LEFT_HIP:       int = 11
        RIGHT_HIP:      int = 12
        LEFT_KNEE:      int = 13
        RIGHT_KNEE:     int = 14
        LEFT_ANKLE:     int = 15
        RIGHT_ANKLE:    int = 16

    get_keypoint = GetKeypoint()
    right_shouler_score=''
    left_shouler_score=''
    right_knee_score=''
    left_knee_score=''
    waist_score=''
    
    global right_shoulder_S_ct
    global right_shoulder_C_ct
    global right_shoulder_D_ct
    global right_shoulder_U_ct
    
    global left_shoulder_S_ct
    global left_shoulder_C_ct
    global left_shoulder_D_ct
    global left_shoulder_U_ct
    
    global right_knee_S_ct
    global right_knee_C_ct
    global right_knee_D_ct
    global right_knee_U_ct

    global left_knee_S_ct
    global left_knee_C_ct
    global left_knee_D_ct
    global left_knee_U_ct
    
    global waist_S_ct
    global waist_C_ct
    global waist_D_ct
    global waist_U_ct
    
    # Initialize the label of the pose. It is not known at this stage.
    labells = 'left_shoulder'
    labelrs = 'right_shoulder'
    labellk = 'left_knee'
    labelrk = 'right_knee'
    labelw = 'waist'

    
    # shoulder
    left_shoulder_x, left_shoulder_y = result_keypoint[get_keypoint.LEFT_SHOULDER]
    right_shoulder_x, right_shoulder_y = result_keypoint[get_keypoint.RIGHT_SHOULDER]
    # elbow
    left_elbow_x, left_elbow_y = result_keypoint[get_keypoint.LEFT_ELBOW]
    right_elbow_x, right_elbow_y = result_keypoint[get_keypoint.RIGHT_ELBOW]
    # hip
    left_hip_x, left_hip_y = result_keypoint[get_keypoint.LEFT_HIP]
    right_hip_x, right_hip_y = result_keypoint[get_keypoint.RIGHT_HIP]
    # knee
    left_knee_x, left_knee_y = result_keypoint[get_keypoint.LEFT_KNEE]
    right_knee_x, right_knee_y = result_keypoint[get_keypoint.RIGHT_KNEE]
    # ankle
    left_ankle_x, left_ankle_y = result_keypoint[get_keypoint.LEFT_ANKLE]
    right_ankle_x, right_ankle_y = result_keypoint[get_keypoint.RIGHT_ANKLE]
    
    
    # <오른쪽 어깨>
    # 14번, 12번, 24번 landmark
    # 오른쪽 팔꿈치,  오른쪽 어깨, 오른쪽 골반 angle 값 계산
    right_shoulder_angle = calculateAngle(right_elbow_x, right_elbow_y,
                                         right_shoulder_x, right_shoulder_y,
                                         right_hip_x, right_hip_y)

    #<왼쪽 어깨>
    # 13번, 11번, 23번 landmark
    # 왼쪽 팔꿈치, 왼쪽 어깨, 왼쪽 엉덩이, landmark angle 값 계산
    left_shoulder_angle = calculateAngle(left_elbow_x, left_elbow_y,
                                        left_shoulder_x, left_shoulder_y,
                                        left_hip_x, left_hip_y)

    #<왼쪽 무릎>
    # 23번, 25번, 27번 landmark
    # 왼쪽 엉덩이, 왼쪽 무릎, 왼쪽 발목 landmark angle 값 계산
    left_knee_angle = calculateAngle(left_hip_x, left_hip_y,
                                    left_knee_x, left_knee_y,
                                    left_ankle_x, left_ankle_y)

    #<오른쪽 무릎>
    # 24번, 26번, 28번 landmark
    # 오른쪽 엉덩이, 오른쪽 무릎, 오른쪽 발목  landmark angle 값 계산
    right_knee_angle = calculateAngle(right_hip_x, right_hip_y,
                                     right_knee_x, right_knee_y,
                                     right_ankle_x, right_ankle_y)

    #<오른쪽 허리>
    #12, 24, 26 landmark
    #오른쪽 어깨, 오른족 엉덩이, 오른쪽 무릎 landmark angle 값 계산
    right_waist_angle = calculateAngle(right_shoulder_x, right_shoulder_y,
                                      right_hip_x, right_hip_y,
                                       right_knee_x, right_knee_y)
    #<왼쪽 허리>
    #11,23,25 landmark
    #왼쪽 어깨, 왼쪽 엉덩이, 왼쪽 무릎 landmark angle 값 계산
    left_waist_angle = calculateAngle(left_shoulder_x, left_shoulder_y,
                                     left_hip_x, left_hip_y,
                                     left_knee_x, left_knee_y)
    
    # 오른쪽 어깨가 얼마나 들려있는지 파악한다.
    if (right_shoulder_angle >= 0 and right_shoulder_angle < 45) or (right_shoulder_angle >=-45 and right_shoulder_angle < 0) :
        right_shoulder_score = 'Safe'
        right_shoulder_S_ct+=1

    elif (right_shoulder_angle >= 45 and right_shoulder_angle < 90) or (right_shoulder_angle >= -90 and right_shoulder_angle < -45) :
        right_shoulder_score = 'Caution'
        right_shoulder_C_ct+=1

    elif (right_shoulder_angle >= 90 and right_shoulder_angle < 180) or (right_shoulder_angle >= -180 and right_shoulder_angle < -90):
        right_shoulder_score = 'Danger'
        right_shoulder_D_ct+=1
    else :
        right_shoulder_score = 'Unknown Pose'
        right_shoulder_U_ct+=1

    #----------------------------------------------------------------------------------------------------------------
    # 왼쪽 어깨가 얼마나 들려있는지 파악한다.
    if (left_shoulder_angle >= 0 and left_shoulder_angle < 45) or (left_shoulder_angle >= -45 and left_shoulder_angle < 0):
        left_shoulder_score = 'Safe'
        left_shoulder_S_ct+=1

    elif (left_shoulder_angle >= 45 and left_shoulder_angle < 90) or (left_shoulder_angle >= -90 and left_shoulder_angle < -45):
        left_shoulder_score = 'Caution'
        left_shoulder_C_ct+=1

    elif (left_shoulder_angle >= 90 and left_shoulder_angle < 180) or (left_shoulder_angle >= -180 and left_shoulder_angle < -90):
        left_shoulder_score = 'Danger'
        left_shoulder_D_ct+=1
    else :
        left_shoulder_score = 'Unknown Pose'
        left_shoulder_U_ct+=1

    #----------------------------------------------------------------------------------------------------------------
    #오른쪽 다리
    if (right_knee_angle >= 90 and right_knee_angle < 180) or (right_knee_angle >= -180 and right_knee_angle < -90) :
        right_knee_score = 'Safe'
        right_knee_S_ct+=1

    elif (right_knee_angle >= 45  and right_knee_angle < 90) or (right_knee_angle >= -90  and right_knee_angle < -45) :
        right_knee_score = 'Caution'
        right_knee_C_ct+=1

    elif (right_knee_angle >= 0 and right_knee_angle < 45) or (right_knee_angle >= -45 and right_knee_angle < 0) :
        right_knee_score = 'Danger'
        right_knee_D_ct+=1
    else :
        right_knee_score = 'Unknown Pose'
        right_knee_U_ct+=1

    #----------------------------------------------------------------------------------------------------------------
    #왼쪽 다리
    if (left_knee_angle >= 90 and left_knee_angle < 180) or (left_knee_angle >= -180 and left_knee_angle < -90):
        left_knee_score = 'Safe'
        left_knee_S_ct+=1

    elif (left_knee_angle >= 45  and left_knee_angle < 90) or (left_knee_angle >= -90  and left_knee_angle < -45) :
        left_knee_score = 'Caution'
        left_knee_C_ct+=1

    elif (left_knee_angle >= 0 and left_knee_angle < 45) or (left_knee_angle >= -45 and left_knee_angle < 0) :
        left_knee_score = 'Danger'
        left_knee_D_ct+=1
    else :
        left_knee_score = 'Unknown Pose'
        left_knee_U_ct+=1

    #----------------------------------------------------------------------------------------------------------------
    #허리
    if ((right_knee_angle >= 90 and right_knee_angle < 180) or (left_knee_angle >= 90 and left_knee_angle < 180)) or ((right_knee_angle >= -180 and right_knee_angle < -90) or (left_knee_angle >= -180 and left_knee_angle < -90)):
        if right_knee_angle >= left_knee_angle:
            if (right_waist_angle >= 150 and right_waist_angle < 180) or (right_waist_angle >= -180 and right_waist_angle < -150):
                waist_score='Safe'
                waist_S_ct+=1
            elif (right_waist_angle >= 120 and right_waist_angle < 150) or (right_waist_angle >= -150 and right_waist_angle < -120):
                waist_score='Caution'
                waist_C_ct+=1
            elif (right_waist_angle <= 120) or (right_waist_angle >= -120):
                waist_score='Danger'
                waist_D_ct+=1
            else:
                waist_score='Unknown Pose'
                waist_U_ct+=1
        if right_knee_angle < left_knee_angle:
            if (left_waist_angle >= 150 and left_waist_angle < 180) or (left_waist_angle >= -180 and left_waist_angle < -150):
                waist_score='Safe'
                waist_S_ct+=1
            elif (left_waist_angle >= 120 and left_waist_angle < 150) or (left_waist_angle >= -150 and left_waist_angle < -120):
                waist_score='Caution'
                waist_C_ct+=1
            elif (left_waist_angle <= 120) or (left_waist_angle >= -120):
                waist_score='Danger'
                waist_D_ct+=1
            else:
                waist_score='Unknown Pose'
                waist_U_ct+=1
    else :
        if right_knee_angle >= left_knee_angle:
            if (right_waist_angle >= 90) or (right_waist_angle <= -90) :
                waist_score='Safe'
                waist_S_ct+=1
            elif (right_waist_angle >= 45 and right_waist_angle < 90) or (right_waist_angle >= -90 and right_waist_angle < -45):         
                waist_score='Caution'
                waist_C_ct+=1
            elif (right_waist_angle <= 45) or (right_waist_angle >= -45):
                waist_score='Danger'
                waist_D_ct+=1
            else:
                waist_score='Unknown Pose'
                waist_U_ct+=1
        if right_knee_angle < left_knee_angle:
            if (left_waist_angle >= 90) or (left_waist_angle <= -90):
                waist_score='Safe'
                waist_S_ct+=1
            elif (left_waist_angle >= 45 and left_waist_angle < 90) or (left_waist_angle >= -90 and left_waist_angle < -45):
                waist_score='Caution'
                waist_C_ct+=1
            elif (left_waist_angle <= 45) or (left_waist_angle >= -45):
                waist_score='Danger'
                waist_D_ct+=1
            else:
                waist_score='Unknown Pose'
                waist_U_ct+=1
            
    # 포즈 분류가 잘 되었는지 확인
    color = (0,0,255)
    cv2.putText(frame, f"{labelrs}: {right_shoulder_score}", (10, 30),cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    cv2.putText(frame, f"{labells}: {left_shoulder_score}", (10, 60),cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    cv2.putText(frame, f"{labelrk}: {right_knee_score}", (10, 90),cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    cv2.putText(frame, f"{labellk}: {left_knee_score}", (10, 120),cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    cv2.putText(frame, f"{labelw}: {waist_score}", (10, 150),cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    


    # 결과 이미지 보여주기 Check if the resultant image is specified to be displayed.
    if display:

        # 결과 이미지를 BGR TO RGB로 matplotlib을 이용해 꺼내준다.
        plt.figure(figsize=[10,10])
        plt.imshow(frame[:,:,::-1]);plt.title("Output Image");plt.axis('off')

    else:

        # 결과 이미지랑 표시될 label을 return 한다
        return frame, labells
    
def circle():
    # 예시 데이터 (실제 데이터에 따라 수정 필요)
    safe_counts = [waist_S_ct, right_shoulder_S_ct, left_shoulder_S_ct, right_knee_S_ct, left_knee_S_ct]      # 안전
    caution_counts = [waist_C_ct, right_shoulder_C_ct, left_shoulder_C_ct, right_knee_C_ct, left_knee_C_ct]  # 주의
    danger_counts = [waist_D_ct, right_shoulder_D_ct, left_shoulder_D_ct, right_knee_D_ct, left_knee_D_ct] # 위험
    unknown_counts = [waist_U_ct, right_shoulder_U_ct, left_shoulder_U_ct, right_knee_U_ct, left_knee_U_ct]
    categories = ['Waist', 'Right Shoulder', 'Left Shoulder', 'Right Knee', 'Left Knee']

# 전체 카운트 계산
    total_counts = np.array(safe_counts) + np.array(caution_counts) + np.array(danger_counts) + np.array(unknown_counts)

# 비율 계산
    safe_ratios = np.array(safe_counts) / total_counts
    caution_ratios = np.array(caution_counts) / total_counts
    danger_ratios = np.array(danger_counts) / total_counts
    unknown_ratios = np.array(unknown_counts) / total_counts
    
    safe_ratios_list = safe_ratios.tolist()
    caution_ratios_list = caution_ratios.tolist()
    danger_ratios_list = danger_ratios.tolist()
    unknown_ratios_list = unknown_ratios.tolist()
    
    safe_ratios_percent = [round(ratio * 100) for ratio in safe_ratios_list]
    caution_ratios_percent = [round(ratio * 100) for ratio in caution_ratios_list]
    danger_ratios_percent = [round(ratio * 100) for ratio in danger_ratios_list]
    unknown_ratios_percent = [round(ratio * 100) for ratio in unknown_ratios_list]
    
    total = safe_counts[0] + caution_counts[0] + danger_counts[0] + unknown_counts[0]



    with open('static/uploads/w_ratios.txt', 'w') as file:
        file.write(f'전체 프레임 {total}장 중에서 누적 안전 개수는 {safe_counts[0]}개이고 비율은 {safe_ratios_percent[0]}%입니다.\n')
        file.write(f'전체 프레임 {total}장 중에서 누적 주의 개수는 {caution_counts[0]}개이고 비율은 {caution_ratios_percent[0]}%입니다.\n')
        file.write(f'전체 프레임 {total}장 중에서 누적 위험 개수는 {danger_counts[0]}개이고 비율은 {danger_ratios_percent[0]}%입니다.\n')
        
    with open('static/uploads/rs_ratios.txt', 'w') as file:
        file.write(f'전체 프레임 {total}장 중에서 누적 안전 개수는 {safe_counts[1]}개이고 비율은 {safe_ratios_percent[1]}%입니다.\n')
        file.write(f'전체 프레임 {total}장 중에서 누적 주의 개수는 {caution_counts[1]}개이고 비율은 {caution_ratios_percent[1]}%입니다.\n')
        file.write(f'전체 프레임 {total}장 중에서 누적 위험 개수는 {danger_counts[1]}개이고 비율은 {danger_ratios_percent[1]}%입니다.\n')
    
    with open('static/uploads/ls_ratios.txt', 'w') as file:
        file.write(f'전체 프레임 {total}장 중에서 누적 안전 개수는 {safe_counts[2]}개이고 비율은 {safe_ratios_percent[2]}%입니다.\n')
        file.write(f'전체 프레임 {total}장 중에서 누적 주의 개수는 {caution_counts[2]}개이고 비율은 {caution_ratios_percent[2]}%입니다.\n')
        file.write(f'전체 프레임 {total}장 중에서 누적 위험 개수는 {danger_counts[2]}개이고 비율은 {danger_ratios_percent[2]}%입니다.\n')
        
    with open('static/uploads/rk_ratios.txt', 'w') as file:

        file.write(f'전체 프레임 {total}장 중에서 누적 안전 개수는 {safe_counts[3]}개이고 비율은 {safe_ratios_percent[3]}%입니다.\n')
        file.write(f'전체 프레임 {total}장 중에서 누적 주의 개수는 {caution_counts[3]}개이고 비율은 {caution_ratios_percent[3]}%입니다.\n')
        file.write(f'전체 프레임 {total}장 중에서 누적 위험 개수는 {danger_counts[3]}개이고 비율은 {danger_ratios_percent[3]}%입니다.\n')
        
    with open('static/uploads/lk_ratios.txt', 'w') as file:
        file.write(f'전체 프레임 {total}장 중에서 누적 안전 개수는 {safe_counts[4]}개이고 비율은 {safe_ratios_percent[4]}%입니다.\n')
        file.write(f'전체 프레임 {total}장 중에서 누적 주의 개수는 {caution_counts[4]}개이고 비율은 {caution_ratios_percent[4]}%입니다.\n')
        file.write(f'전체 프레임 {total}장 중에서 누적 위험 개수는 {danger_counts[4]}개이고 비율은 {danger_ratios_percent[4]}%입니다.\n')
        
    with open('static/uploads/u_ratios.txt', 'w') as file:
        file.write(f'전체 프레임 {total}장 중에서 허리의 누적 개수는 {unknown_counts[0]}개이고 비율은 {unknown_ratios_percent[0]}%입니다.\n')
        file.write(f'전체 프레임 {total}장 중에서 오른쪽 어깨의 누적 개수는 {unknown_counts[1]}개이고 비율은 {unknown_ratios_percent[1]}%입니다.\n')
        file.write(f'전체 프레임 {total}장 중에서 왼쪽 어깨의 누적 개수는 {unknown_counts[2]}개이고 비율은 {unknown_ratios_percent[2]}%입니다.\n')
        file.write(f'전체 프레임 {total}장 중에서 오른쪽 무릎의 누적 개수는 {unknown_counts[3]}개이고 비율은 {unknown_ratios_percent[3]}%입니다.\n')
        file.write(f'전체 프레임 {total}장 중에서 왼쪽 무릎의 누적 개수는 {unknown_counts[4]}개이고 비율은 {unknown_ratios_percent[4]}%입니다.\n')



# 색상 매핑 딕셔너리 생성
    label_colors = {
        'Safe': 'forestgreen',
        'Caution': 'orange',
        'Danger': 'crimson',
        'Unknown': 'gainsboro'
        }

# 원 그래프 생성
    fig, axs = plt.subplots(1, 5, figsize=(25, 7))
    for i, ax in enumerate(axs):
        labels = []
        values = []
        if safe_ratios[i] != 0:
            labels.append(f'Safe\n{safe_ratios[i]*100:.1f}%')
            values.append(safe_ratios[i])

        if caution_ratios[i] != 0:
            labels.append(f'Caution\n{caution_ratios[i]*100:.1f}%')
            values.append(caution_ratios[i])

        if danger_ratios[i] != 0:
            labels.append(f'Danger\n{danger_ratios[i]*100:.1f}%')
            values.append(danger_ratios[i])

        if unknown_ratios[i] != 0:
            labels.append(f'Unknown\n{unknown_ratios[i]*100:.1f}%')
            values.append(unknown_ratios[i])

        wedges, _, autotexts = ax.pie(values, autopct='%1.1f%%', textprops=dict(color="k", fontsize=14),
                                  colors=[label_colors[label.split("\n")[0]] for label in labels],
                                  wedgeprops=dict(width=1, edgecolor='k'),
                                  startangle=90, counterclock=False)

        for autotext in autotexts:
            autotext.set_visible(False) if autotext.get_text() == '0.0%' else autotext.set_visible(True)

        # 부위명을 그래프 위에 추가
        ax.text(0.5, 1.1, categories[i], horizontalalignment='center', verticalalignment='center', fontsize=17, transform=ax.transAxes)

        # 범례 제거
        ax.legend().remove()

    fig.suptitle('Pose Classification Ratios by Body Parts', fontsize=27, y=0.9)  # 제목
    plt.subplots_adjust(wspace=0.5)  # 그래프 간 간격 조절
    plt.savefig('static/uploads/circle.png')
    


def stick():
    # 예시 데이터 (실제 데이터에 따라 수정 필요)
    safe_counts = [waist_S_ct, right_shoulder_S_ct, left_shoulder_S_ct, right_knee_S_ct, left_knee_S_ct]      # 안전
    caution_counts = [waist_C_ct, right_shoulder_C_ct, left_shoulder_C_ct, right_knee_C_ct, left_knee_C_ct]  # 주의
    danger_counts = [waist_D_ct, right_shoulder_D_ct, left_shoulder_D_ct, right_knee_D_ct, left_knee_D_ct] # 위험
    Unknown_counts = [waist_U_ct, right_shoulder_U_ct, left_shoulder_U_ct, right_knee_U_ct, left_knee_U_ct]
    categories = ['Waist', 'Right Shoulder', 'Left Shoulder', 'Right Knee', 'Left Knee']

    bar_width = 0.15
    index = np.arange(len(categories))

    fig, ax = plt.subplots()

    bar1 = ax.bar(index - bar_width, safe_counts, bar_width, label='Safe', color='forestgreen')
    bar2 = ax.bar(index, caution_counts, bar_width, label='Caution', color='orange')
    bar3 = ax.bar(index + bar_width, danger_counts, bar_width, label='Danger', color='crimson')
    bar4 = ax.bar(index + bar_width + bar_width, Unknown_counts, bar_width, label='Unknown Pose', color='gainsboro')

    ax.set_xlabel('Body Parts')
    ax.set_ylabel('Count')
    ax.set_title('Pose Classification Counts by Body Parts')
    ax.set_xticks(index)
    ax.set_xticklabels(categories)
    ax.legend()
    plt.savefig('static/uploads/stick.png')


