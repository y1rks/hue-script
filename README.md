# hue-script

cron 設定

```
crontab -e
```

cron 設定内容

```
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin:/home/pi/.venvs/weatherhue/bin
MAILTO=""

# 1時間おきに更新
0 * * * * /home/pi/.venvs/weatherhue/bin/python /home/pi/weather_hue.py

# 起動直後に1回（ネットが上がるまで少し待つ）
@reboot sleep 60; /home/pi/.venvs/weatherhue/bin/python /home/pi/weather_hue.py
```

python 修正

```
vim ~/weather_hue.py
```

テスト実行

```
~/.venvs/weatherhue/bin/python ~/weather_hue.py
```
