from pygame.locals import *
import os
import playsound
import speech_recognition as sr
import time
import wikipedia
import datetime
import re
import requests
import urllib.request as urllib2
from time import strftime
from gtts import gTTS
import pygame
os.environ['SDL_VIDEODRIVER'] = 'dummy'  # Tắt thông báo Pygame


wikipedia.set_lang('vi')
language = 'vi'


# chuyển văn bản thành âm thanh
def speak(text):
    print("Trợ Lý ảo:  ", text)
    tts = gTTS(text=text, lang="vi", slow=False)
    output_directory = r"Am_Thanh"
    output_audio_file = os.path.join(output_directory, "sound.mp3")
    # Lưu file âm thanh
    tts.save(output_audio_file)
    # Phát âm thanh
    playsound.playsound(output_audio_file, True)
    # Xóa file âm thanh sau khi đã phát
    os.remove(output_audio_file)


# chuyển giọng nói thành văn bản
def get_audio():
    ear_robot = sr.Recognizer()
    with sr.Microphone() as source:
        print("Trợ Lý Ảo:  Đang nghe ! -- __ -- !")

        # ear_robot.pause_threshold = 4
        audio = ear_robot.record(source, duration=4)
        # audio = ear_robot.listen(source, phrase_time_limit=5)

        try:
            print(("Trợ Lý Ảo :  ...  "))
            text = ear_robot.recognize_google(audio, language="vi-VN")
            print("Tôi:  ", text)
            return text
        except Exception as ex:
            print("Trợ Lý Ảo:  Lỗi Rồi ! ... !")
            return 0


def get_audio_2():
    ear_robot = sr.Recognizer()
    with sr.Microphone() as source:
        ear_robot.pause_threshold = 2
        print("Đang nghe ===========================")
        audio = ear_robot.listen(source)
    try:
        text = ear_robot.recognize_google(audio, language="vi-VN")
    except:
        speak("Nhận dạng giọng nói thất bại. Vui lòng nhập lệnh ở dưới")
        text = input("Mời nhập: ")
    return text.lower()


def stop():
    speak("Hẹn gặp lại sau nha ! ... ")


def get_text():
    for i in range(3):
        text = get_audio()
        if text:
            return text.lower()
        elif i < 2:
            speak("Trợ Lý Ảo không nghe rõ bạn nói. Vui lòng nói lại nha !")
    time.sleep(3)
    stop()
    return 0


def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Nghe...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="vi")
        print(f"Bạn đã nói: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Không thể nhận diện giọng nói.")
        return ""
    except sr.RequestError as e:
        print(f"Lỗi kết nối đến Google API: {e}")
        return ""


def hello(name):
    day_time = int(strftime('%H'))
    if 0 <= day_time < 11:
        speak(f"Chào bạn {name}. Chúc bạn buổi sáng tốt lành.")
    elif 11 <= day_time < 13:
        speak(f"Chào bạn {name}. Chúc bạn có một buổi trưa thật vui vẻ.")
    elif 13 <= day_time < 18:
        speak(f"Chào bạn {name}. Chúc bạn buổi chiều vui vẻ.")
    elif 18 <= day_time < 22:
        speak(f"Chào bạn {name}. Tối rồi, Bạn đã cơm nước gì chưa ?")
    elif 22 <= day_time <= 23:
        speak(f"Chào Bạn {name}. Muộn rồi bạn nên đi nghủ sớm nha.")
    else:
        speak(f"Thời gian bên tôi chưa đúng hoặc gặp lỗi. Bạn nên xem lại nha.")


def get_time(text):
    now = datetime.datetime.now()
    if 'giờ' in text:
        speak(f"Bây giờ là {now.hour} giờ {now.minute} phút {now.second} giây")
    elif "ngày" in text:
        speak(f"hôm nay là ngày {now.day} tháng {now.month} năm {now.year}")
    else:
        speak("Lý Hành chưa hiểu ý bạn.")


def current_weather():
    speak("Bạn muốn xem thời tiết ở đâu ạ.")
    # Đường dẫn trang web để lấy dữ liệu về thời tiết
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    # lưu tên thành phố vào biến city
    city = get_text()
    # nếu biến city != 0 và = False thì để đấy ko xử lí gì cả
    if not city:
        pass
    # api_key lấy trên open weather map
    api_key = "b4750c6250a078a943b3bf920bb138a0"
    # tìm kiếm thông tin thời thời tiết của thành phố
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    # truy cập đường dẫn của dòng 188 lấy dữ liệu thời tiết
    response = requests.get(call_url)
    # lưu dữ liệu thời tiết dưới dạng json và cho vào biến data
    data = response.json()
    # kiểm tra nếu ko gặp lỗi 404 thì xem xét và lấy dữ liệu
    if data["cod"] != "404":
        # lấy value của key main
        city_res = data["main"]
        # nhiệt độ hiện tại
        current_temperature = city_res["temp"]
        # áp suất hiện tại
        current_pressure = city_res["pressure"]
        # độ ẩm hiện tại
        current_humidity = city_res["humidity"]
        # thời gian mặt trời
        suntime = data["sys"]
        # 	lúc mặt trời mọc, mặt trời mọc
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        # lúc mặt trời lặn
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        # thông tin thêm
        wthr = data["weather"]
        # mô tả thời tiết
        weather_description = wthr[0]["description"]
        # Lấy thời gian hệ thống cho vào biến now
        now = datetime.datetime.now()
        # hiển thị thông tin với người dùng
        content = f"""
        Hôm nay là ngày {now.day} tháng {now.month} năm {now.year}
        Mặt trời mọc vào {sunrise.hour} giờ {sunrise.minute} phút
        Mặt trời lặn vào {sunset.hour} giờ {sunset.minute} phút
        Nhiệt độ trung bình là {current_temperature} độ C
        Áp suất không khí là {current_pressure} héc tơ Pascal
        Độ ẩm là {current_humidity}%
        """
        speak(content)
    else:
        # nếu tên thành phố không đúng thì nó nói dòng dưới 227
        speak("Không tìm thấy địa chỉ của bạn")


def tell_me_about():
    try:
        speak("Hãy nói cho tôi nghe Bạn muốn tìm gì ạ ?")
        text = get_text()
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0])
        dem = 0
        for content in contents[1:]:
            if dem < 2:
                speak("Bạn có muốn biết thêm không ???")
                ans = get_text()
                if 'có' not in ans:
                    break
            dem += 1
            speak(content)
        speak("Đây là nội dung tôi vừa tìm được cảm ơn bạn đã lắng nghe")
    except:
        speak(f"{name} không định nghĩa được thuật ngữ của bạn !!!")


def baothuc():
    invalid = True
    while (invalid):
        # Get a valid user input for the alarm time
        speak("bạn muốn đặt báo thức vào lúc mấy giờ")
        text = get_text()
        alarmTime = [int(n) for n in text.split(":")]
        if alarmTime[0] >= 24 or alarmTime[0] < 0:
            invalid = True
        elif alarmTime[1] >= 60 or alarmTime[1] < 0:
            invalid = True
        else:
            invalid = False

    # Number of seconds in an Hour, Minute, and Second
    seconds_hms = [3600, 60, 1]

    # Convert the alarm time to seconds
    alarmSeconds = sum(
        [a*b for a, b in zip(seconds_hms[:len(alarmTime)], alarmTime)])

    now = datetime.datetime.now()
    currentTimeInSeconds = sum(
        [a*b for a, b in zip(seconds_hms, [now.hour, now.minute, now.second])])

    secondsUntilAlarm = alarmSeconds - currentTimeInSeconds

    if secondsUntilAlarm < 0:
        secondsUntilAlarm += 86400  # number of seconds in a day

    print("Alarm is set!")
    print("The alarm will ring at %s" %
          datetime.timedelta(seconds=secondsUntilAlarm))

    time.sleep(secondsUntilAlarm)

    pygame.mixer.init()
    pygame.mixer.music.load(r'Am_Thanh\baothuc.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # stop = get_text()
        # if "tắt báo thức" in stop:
        pygame.time.Clock().tick(1)


def demnguoc():
    speak("bạn muốn đếm ngược bao nhiêu thời gian")
    text = get_text()
    alarmTime = re.findall(r'\d+', text)
    if int(alarmTime[0]) > 0:
        secondsUntilAlarm = int(alarmTime[0])*60
    print("Alarm is set!")
    print("The alarm will ring at %s" %
          datetime.timedelta(seconds=secondsUntilAlarm))

    for i in range(0, secondsUntilAlarm):
        time.sleep(1)
        secondsUntilAlarm -= 1
        print(datetime.timedelta(seconds=secondsUntilAlarm))

    # speak("Ring Ring... time to wake up!")
    # playsound.playsound(r'D:\CHATBOX\MUSICAL\baothuc.mp3')
    # sound = pygame.mixer.Sound('baothuc.mp3')
    # sound.play()
    pygame.mixer.init()
    pygame.mixer.music.load(r'Am_Thanh\baothuc.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def kechuyen():
    speak('Tôi có một số câu chuyện xoay quanh tình yêu, chiến tranh, hòa bình, cuộc sống hàng ngày, phiêu lưu, khoa học viễn tưởng, lịch sử và văn hóa ')

    speak('Bạn muốn nghe chuyện gì nào?')
    text2 = get_text()
    if 'tình yêu' in text2 or 'tình' in text2:
        pygame.mixer.init()
        pygame.mixer.music.load(r'Am_Thanh\TINHYEU.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(120)
    elif 'chiến tranh' in text2 or 'trận chiến' in text2:
        pygame.mixer.init()
        pygame.mixer.music.load(r'Am_Thanh\CHIENTRANH.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(72)
    elif 'hòa bình' in text2 or 'độc lập' in text2:
        pygame.mixer.init()
        pygame.mixer.music.load(r'Am_Thanh\HOABINH.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(81)
    elif 'cuộc sống hàng ngày' in text2 or 'cuộc sống' in text2 or 'sinh hoạt' in text2 or 'đơn giản' in text2:
        pygame.mixer.init()
        pygame.mixer.music.load(r'Am_Thanh\CUOCSONG.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(114)
    elif 'phiêu lưu' in text2 or 'khám phá' in text2 or 'thám hiểm' in text2:
        pygame.mixer.init()
        pygame.mixer.music.load(r'Am_Thanh\PHUULU.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(54)
    elif 'khoa học viễn tưởng' in text2 or 'khoa học' in text2 or 'viễn tưởng' in text2 or 'tương lai' in text2:
        pygame.mixer.init()
        pygame.mixer.music.load(r'Am_Thanh\khoahoc.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(44)
    elif 'lịch sử' in text2 or 'xưa' in text2 or 'lâu' in text2 or 'trước kia' in text2:
        pygame.mixer.init()
        pygame.mixer.music.load(r'Am_Thanh\LICHSU.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(49)
    elif 'văn hóa' in text2 or 'tốt đẹp' in text2 or 'truyền thống' in text2:
        pygame.mixer.init()
        pygame.mixer.music.load(r'Am_Thanh\VANHOA.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(47)


# speak("Xin chào. Bạn tên là gì ?")
# global robot_name
# robot_name = "ly hanh"
# global name
# name = get_text()
n = 1
while n:
    command = recognize_speech()
    if "trợ lý ảo" in command:
        speak(f'Xin chào bạn {os.getlogin()}.')
        speak(f'Bạn cần trợ lý ảo giúp gì không ạ ?')
        while True:
            text = get_text()
            if ('tạm biệt' in text) or ('hẹn gặp lại' in text):
                stop()
                break
            elif "chào trợ lý" in text:
                hello(os.getlogin())
            elif "hiện tại" in text:
                get_time(text)
            elif "thời tiết" in text:
                current_weather()
            elif "định nghĩa" in text:
                tell_me_about()
            elif "đặt báo thức" in text:
                baothuc()
            elif "đếm ngược" in text:
                demnguoc()
            elif 'kể' in text or 'kể chuyện' in text or 'chuyện' in text or 'buồn' in text or 'chán' in text or 'nói' in text:
                kechuyen()
            elif "kết thúc" in text:
                n = 0
                break
