from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask_mysqldb import MySQL #MYSQL 데이터베이스
import MySQLdb.cursors #MYSQL 데이터베이스
import re
from os.path import exists
from flask import abort
import torch
import os
import mimetypes
import cv2 #이미지출력
from PIL import Image
from torchvision import transforms
from keypoint import *
import tensorflow as tf
from torchvision.models.detection import keypointrcnn_resnet50_fpn
from ultralytics import YOLO
from werkzeug.utils import secure_filename
from flask import send_file
import csv
import shutil 
from datetime import datetime #datetime 설정
from flask import jsonify #비밀번호


#Mysql 부분
app = Flask(__name__)
app.secret_key = 'star12*'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'qwer1234'
app.config['MYSQL_DB'] = 'pythonlogin'

mysql = MySQL(app)


# 시작 페이지
@app.route("/")
def point():
    return render_template('startpoint.html')

# 동적 페이지
@app.route('/<path:name>')
def start(name):
    return render_template(name)

# 백엔드 변경
def change_backend():
   
    plt.switch_backend('Agg')
    

#로그인 페이지
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')  # GET 요청에 대한 처리 추가

    msg = ''
    if 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) #추가한 부분 AND is_active = 1
        cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s AND is_active = 1', (email, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['email'] = account['email']
            session['username'] = account['username'] #수정부분 1204 1020
            return redirect('startpoint.html')
        else:
            msg = '유효하지 않은 사용자명 또는 비밀번호입니다..'
    elif request.method == 'POST':
        msg = '아이디와 비밀번호를 입력해주세요.'
    return render_template('login.html', msg=msg)




#로그아웃세션
@app.route('/logout')
def logout():
    session.clear()
    return redirect('startpoint.html')


# 회원 정보 페이지
@app.route('/profile')
def profile():
    if 'loggedin' in session and session['loggedin']:
        # 회원 정보를 불러오는 SQL 쿼리
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', [session['username']])
        account = cursor.fetchone()

        if account:
            return render_template('profile.html', account=account)
        else:
            return "사용자 정보를 찾을 수 없습니다."
    else:
        return redirect('login')


#회원가입 
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')  # GET 요청에 대한 처리 추가
    msg = ''
    if 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password'] #비밀번호 확인
        if password != confirm_password:
            return render_template('register.html', msg='비밀번호와 비밀번호 확인이 일치하지 않습니다.') 
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s', [email])
        account = cursor.fetchone()
        if account:
            msg = '아이디가 중복이 됩니다. 다시 입력해 주세요.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = '유효하지 않는 이메일 주소입니다.'
        elif not username or not password or not email:
            msg = '회원가입란에 작성을 해주세요'
        else:
            cursor.execute('INSERT INTO accounts (username, password, email, is_active) VALUES (%s, %s, %s, %s)', [username, password, email, 1])
            mysql.connection.commit()
            msg = '성공적으로 가입이 완료되었습니다.'
    elif request.method == 'POST':
        msg = '회원가입란에 작성을 해주세요'
    return render_template('register.html', msg=msg)


app.config['UPLOAD_FOLDER'] = 'static/uploads'


def copy_and_rename_files(source_folder, dest_folder, user_id):
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # 목적지 폴더 생성
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    files_to_copy = ['output_video.mp4', 'circle.png', 'stick.png']

    for filename in files_to_copy:
        source_path = os.path.join(source_folder, filename)
        dest_name = f"{current_time}_{filename}"
        dest_path = os.path.join(dest_folder, dest_name)

        # 파일이 존재하는지 확인
        if os.path.exists(source_path):
            shutil.copy2(source_path, dest_path)
        else:
            print(f"File not found: {source_path}")

        # 파일 정보를 데이터베이스에 저장
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO uploaded_files (user_id, filename) VALUES (%s, %s)', [user_id, dest_name])
        mysql.connection.commit()
        cursor.close()

################## 1101 수정
def get_user_id(email):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id FROM accounts WHERE email = %s', [email])
    result = cursor.fetchone()
    cursor.close()

    if result:
        return result['id']
    else:
        return None



#파일업로드
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'videoFile' not in request.files:
        return redirect(request.url)

    file = request.files['videoFile']

    if file.filename == '':
        return redirect(request.url)

    if file:
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(video_path)
        
        # 파일 저장 경로 설정
        video_capture = cv2.VideoCapture(video_path)
        output_folder = f'static/uploads/list'
        backup_folder = f'static/uploads'

        if os.path.exists(output_folder):
            files_in_folder = os.listdir(output_folder)
            for file_in_folder in files_in_folder:
                file_path = os.path.join(output_folder, file_in_folder)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(e)
        else:
            os.makedirs(output_folder) 

        frame_count = 0
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        interval = int(fps * 0.5)

        model = YOLO('yolov8m-pose.pt')

        user_id = get_user_id(session['email']) if 'email' in session else None #1220 수정 if
        
        while video_capture.isOpened():
            for _ in range(interval):
                ret = video_capture.grab()
            ret, frame = video_capture.read()

            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frame_height, frame_width, _ = frame.shape
            frame = cv2.resize(frame, (int(frame_width * (640 / frame_height)), 640))

            results = model.predict(frame, save=False)
            result_keypoint = results[0].keypoints.xyn.cpu().numpy()[0]
            frame, _ = extract_keypoint(frame, result_keypoint, display=False)
            annotated_frame = results[0].plot()

            cv2.imwrite(f'{output_folder}/frame_{frame_count}.jpg', annotated_frame)
            frame_count += 1

        video_capture.release()

        circle()
        stick()

        image_folder = output_folder
        video_name = os.path.join(app.config['UPLOAD_FOLDER'], 'output_video.mp4')
        fps = 2

        images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
        images.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, layers = frame.shape
        video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'H264'), fps, (width, height))
        
        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))
        video.release()   

        if user_id is not None:
            copy_and_rename_files(backup_folder, os.path.join(app.config['UPLOAD_FOLDER'], 'date'), user_id)

        return redirect(url_for('results_page', result_filename='output_video.mp4'))
    return render_template('upload.html', image_list=images)






#인덱스에서 이미지 미리보기
@app.route('/results/<result_filename>')
def results_page(result_filename):

    image_folder = 'static/uploads/list'
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]

    # 비율에 따라 이미지 선택 (예: 30%, 60%, 90%, 100% 지점)
    if len(images) >= 4:
        total_images = len(images)
        selected_images = [images[int((total_images - 1) * ratio)] for ratio in [0.3, 0.6, 0.9, 1.0]]
    else:
        selected_images = []
    #result_video_path = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
    return render_template('index.html', result_video=result_filename, image_list = selected_images)


@app.route('/image.html')
def picture():
    # 이미지 파일 목록 가져오기
    image_folder = 'static/uploads/list'
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]

    # HTML 템플릿으로 이미지 파일 목록 전달
    return render_template('image.html', image_list=images)





@app.route('/index.html')
def imagee():
    # 이미지 파일 목록 가져오기
    image_folder = 'static/uploads/list'
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]

    # 비율에 따라 이미지 선택 (예: 30%, 60%, 90%, 100% 지점)
    if len(images) >= 4:
        total_images = len(images)
        selected_images = [images[int((total_images - 1) * ratio)] for ratio in [0.3, 0.6, 0.9, 1.0]]
    else:
        selected_images = []

    # HTML 템플릿으로 이미지 파일 목록 전달
    return render_template('index.html', image_list=selected_images)

#####회원탈퇴 , 회원가입 부분 isactive 수정, 로그인 부분 isactive수정, profile.html 수정
@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    if 'loggedin' in session and session['loggedin']:
        if request.method == 'POST':
            # 사용자 정보 가져오기
            username = session['username']

            # 데이터베이스에서 사용자 계정을 삭제로 표시
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE accounts SET is_active = 0 WHERE username = %s', [username])
            mysql.connection.commit()
            cursor.close()

            # 사용자 로그아웃
            session.clear()

            return redirect(url_for('point'))  # 삭제 후 시작 페이지로 리디렉션

        return render_template('delete_account.html')  # 확인 페이지 표시
    else:
        return redirect(url_for('login'))


###회원정보 변경 
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'loggedin' in session and session['loggedin']:
        if request.method == 'POST':
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']

            # 현재 비밀번호 확인
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE email = %s', [session['email']])
            account = cursor.fetchone()

            if account and account['password'] == current_password:
                if new_password == confirm_password:
                    # 새로운 비밀번호를 데이터베이스에 업데이트
                    cursor.execute('UPDATE accounts SET password = %s WHERE email = %s', [new_password, session['email']])
                    mysql.connection.commit()
                    cursor.close()
                    return render_template('password_change_success.html')
                else:
                    return render_template('password_change.html', error='새로운 비밀번호가 일치하지 않습니다.')
            else:
                return render_template('password_change.html', error='현재 비밀번호가 올바르지 않습니다.')

        return render_template('password_change.html')
    else:
        return redirect(url_for('login'))


## 이전기록 분석

app.config['MY_UPLOAD_FOLDER'] = 'static/uploads/date'

def get_user_id(email):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id FROM accounts WHERE email = %s', [email])
    result = cursor.fetchone()
    cursor.close()

    if result:
        return result['id']
    else:
        return None

@app.route('/tables.html')
def tables():
    try:
        # 현재 로그인한 사용자의 이메일을 가져옴
        user_email = session['email']

        # 사용자의 이메일을 기반으로 사용자 ID를 가져옴
        user_id = get_user_id(user_email)

        # 사용자 ID를 기반으로 해당 사용자의 파일 정보를 가져옴
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM uploaded_files WHERE user_id = %s', [user_id])
        data = cur.fetchall()

        for row in data:
            # 파일 URL 추가
            row['file_url'] = url_for('uploaded_file', filename=row['filename'])
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        cur.close()

    return render_template('tables.html', data=data)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # 변경된 변수명 사용
    return send_from_directory(app.config['MY_UPLOAD_FOLDER'], filename)



########### 3개 부위함수

@app.route('/waist.html')
def waist():
    # 파일에서 내용을 읽어옴
    with open('static/uploads/w_ratios.txt', 'r') as file:
        wa = file.read().replace('\n', '<br>')

    # 읽어온 내용을 HTML 템플릿으로 전달
    return render_template('waist.html', wa=wa)

@app.route('/shoulder.html')
def shoulder():
    # 파일에서 내용을 읽어옴
    with open('static/uploads/rs_ratios.txt', 'r') as file:
        rs = file.read().replace('\n', '<br>')
    with open('static/uploads/ls_ratios.txt', 'r') as file:
        ls = file.read().replace('\n', '<br>')

    # 읽어온 내용을 HTML 템플릿으로 전달
    return render_template('shoulder.html', rs = rs, ls = ls)

@app.route('/knee.html')
def knee():
    # 파일에서 내용을 읽어옴
    with open('static/uploads/rk_ratios.txt', 'r') as file:
        rk = file.read().replace('\n', '<br>')
    with open('static/uploads/lk_ratios.txt', 'r') as file:
        lk = file.read().replace('\n', '<br>')

    # 읽어온 내용을 HTML 템플릿으로 전달
    return render_template('knee.html', rk = rk, lk = lk)

@app.route('/unknown.html')
def unknownpose():
    # 파일에서 내용을 읽어옴
    with open('static/uploads/u_ratios.txt', 'r') as file:
        un = file.read().replace('\n', '<br>')

    # 읽어온 내용을 HTML 템플릿으로 전달
    return render_template('unknown.html', un = un)
####


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    app.debug = True

