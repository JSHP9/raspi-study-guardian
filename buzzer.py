from gpiozero import PWMOutputDevice
import time

buzzer = PWMOutputDevice(17, frequency=2000)
alarm_start = None


def alert(status, cnt):
    global alarm_start

    if status != "SLEEP":
        buzzer.off()
        alarm_start = None
        return

    if cnt == 1:
        frequency = 2000
        interval = 0.6

    elif cnt == 2:
        frequency = 2600
        interval = 0.35

    else:
        frequency = 3200
        interval = 0.2

    # buzzer.frequency = 값을 실행할 때마다 내부 타이머가 초기화로 인해 소리가 끊기는거 방지
    if buzzer.frequency != frequency:
        buzzer.frequency = frequency

    now = time.monotonic()

    if alarm_start is None:
        alarm_start = now

    elapsed = now - alarm_start

    if int(elapsed / interval) % 2 == 0:
        buzzer.value = 0.5
    else:
        buzzer.off()
