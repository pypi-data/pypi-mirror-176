### Alpha_py

Репозиторий содержит API низкоуровневой системы управления автомобилем [Alpha](alpha.starline.ru), разрабатываемой в рамках проекта [OSCAR](https://gitlab.com/starline/oscar), для беспилотных транспортных средств.


#### Установка с PyPI

```
pip3 install --user alpha_py
```


#### Установка из исходников

```
git clone https://gitlab.com/starline/alpha_py.git && cd alpha_py
pip3 install --user -e .
```


#### Использование

```
import alpha
vehicle = alpha.Vehicle(“/dev/ttyACM0”)
vehicle.drive()
vehicle.steer(20)
vehicle.move(10)
vehicle.manual()
vehicle.led_blink()
vehicle.emergency_stop()
vehicle.recover()
vehicle.left_turn_signal()
vehicle.right_turn_signal()
vehicle.emergency_signals()
vehicle.turn_off_signals()
vehicle.get_vehicle_speed()
```


