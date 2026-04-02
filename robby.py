from gpiozero import Robot, Buzzer, LineSensor
import RPi.GPIO as GPIO
import time
from time import sleep

# GPIO ayarları
GPIO.setwarnings(False)  # Uyarıları devre dışı bırak
GPIO.setmode(GPIO.BCM)

# GPIO pinlerinin tanımlanması
TRIG = 23
ECHO = 24
LED_PIN1 = 16  # İlk LED GPIO16'ya bağlı
LED_PIN2 = 25  # İkinci LED GPIO25'e bağlı
BUZZER_PIN = 22  # Buzzer GPIO22'ye bağlı

# GPIO pinlerinin çıkış olarak ayarlanması
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED_PIN1, GPIO.OUT)  # İlk LED için çıkış pini
GPIO.setup(LED_PIN2, GPIO.OUT)  # İkinci LED için çıkış pini

# Buzzer ayarları
buzzer = Buzzer(BUZZER_PIN)

# LED'lerin başlangıç durumlarını ayarlama
GPIO.output(LED_PIN1, GPIO.LOW)  # İlk LED başta sönük
GPIO.output(LED_PIN2, GPIO.LOW)  # İkinci LED başta sönük

# Robot ve çizgi sensörlerinin ayarları
robot = Robot(left=(7, 8), right=(9, 10))
left_sensor = LineSensor(17, pull_up=True)
right_sensor = LineSensor(27, pull_up=True)

speed = 0.8  # Motor hızı
obstacle_distance_threshold = 10  # Engel algılandığında durma mesafesi (cm)

# Mesafe ölçüm fonksiyonu
def measure_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    timeout_start = time.time()  # Zaman aşımı için başlangıç zamanı

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if time.time() - timeout_start > 0.05:  # 50ms zaman aşımı
            return 999

    pulse_end = time.time()
    timeout_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if time.time() - timeout_start > 0.05:
            return 999

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # cm cinsinden mesafe hesaplanır
    return round(distance, 2)

# Korna sesi fonksiyonu (ses azaltılmış)
def horn_sound():
    print("Korna sesi başlıyor...")
    try:
        for _ in range(2):
            buzzer.on()
            sleep(0.1)  # Daha kısa bir bip
            buzzer.off()
            sleep(0.2)  # Kısa bir bekleme
    finally:
        buzzer.off()
    print("Korna sesi bitti.")

# Robotun çizgi takibi ve engel algılama işlevi
def motor_control():
    while True:
        # Mesafeyi ölç
        distance = measure_distance()
        left_detect = int(not left_sensor.value)  # Siyah çizgi 1 olarak algılanır
        right_detect = int(not right_sensor.value)
        print(f"Mesafe: {distance} cm, Sol sensör: {left_detect}, Sağ sensör: {right_detect}")

        # Robot havadaysa dur
        if left_detect == 0 and right_detect == 0 and distance > obstacle_distance_threshold:
            print("Motor durduruluyor.")
            robot.stop()
            GPIO.output(LED_PIN1, GPIO.LOW)
            GPIO.output(LED_PIN2, GPIO.LOW)
            continue

        # Engel algılandıysa dur ve korna çal
        if distance < obstacle_distance_threshold:
            print("Engel algılandı! Duruyor, korna çalıyor ve LED'ler yanıyor.")
            robot.stop()
            GPIO.output(LED_PIN1, GPIO.HIGH)  # LED'leri aç
            GPIO.output(LED_PIN2, GPIO.HIGH)
            horn_sound()  # Korna sesi çal
            continue

        # Çizgi algılandıysa düz devam et
        if left_detect == 1 or right_detect == 1:
            print("Çizgi takip: Düz gidiyor.")
            robot.forward(speed)
            GPIO.output(LED_PIN1, GPIO.LOW)  # LED'leri kapat
            GPIO.output(LED_PIN2, GPIO.LOW)
        else:
            print("Çizgi takip: Duruyor.")
            robot.stop()
            GPIO.output(LED_PIN1, GPIO.LOW)
            GPIO.output(LED_PIN2, GPIO.LOW)

        time.sleep(0.05)  # Döngü hızını kontrol etmek için bekleme süresi

# Ana program döngüsü
try:
    motor_control()
except KeyboardInterrupt:
    print("Program sonlandırıldı")
    robot.stop()
    GPIO.output(LED_PIN1, GPIO.LOW)
    GPIO.output(LED_PIN2, GPIO.LOW)
    buzzer.off()
    GPIO.cleanup()
finally:
    print("Robot durduruluyor ve GPIO temizleniyor...")
    robot.stop()
    GPIO.output(LED_PIN1, GPIO.LOW)
    GPIO.output(LED_PIN2, GPIO.LOW)
    buzzer.off()
    GPIO.cleanup()
