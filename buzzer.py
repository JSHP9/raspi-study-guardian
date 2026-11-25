from gpiozero import PWMOutputDevice

#2000Hz PWM 신호 생성
buzzer = PWMOutputDevice(17, frequency=2000)

def alert(status):
    if status == "SLEEP":
        buzzer.value = 0.5  # PWM 신호 출력
    else:
        buzzer.off()       # 부저 끄기
