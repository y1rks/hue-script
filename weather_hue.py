#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Raspberry Pi + Open-Meteo + Hue（phue） 夜は消灯版

from phue import Bridge
import requests, sys, datetime

# ===== 設定 =====
BRIDGE_IP = "192.168.11.14"           # HueブリッジのIP
LIGHTS = ["Hue color lamp 1"]          # 対象ライト名（Hueアプリ/ブリッジの名前）
LAT, LON = 35.68, 139.76               # 緯度・経度（例：東京）
NIGHT_HOURS = set(range(18, 24)) | set(range(0, 9))  # 夜の時間帯
# =================

def pick_color(code):
    # Open-Meteo weathercode のざっくり分類
    rain = {51,53,55,61,63,65,80,81,82,95,96,99}
    snow = {71,73,75,77,85,86}
    cloudy = {1,2,3,45,48}
    # デフォルト（晴れ）= 暖色
    data = {"hue": 8000, "sat": 180, "bri": 138}
    if code in rain:
        data = {"hue": 46920, "sat": 254, "bri": 120}  # 雨=青
    elif code in snow:
        data = {"ct": 153, "bri": 152}                 # 雪=冷白
    elif code in cloudy:
        data = {"ct": 238, "bri": 108}                 # くもり=中性白
    return data

def turn_off_night(b, ts):
    for name in LIGHTS:
        b.set_light(name, "on", False)
    print(f"[{ts}] Night hours: turned OFF {LIGHTS}")

def main():
    now = datetime.datetime.now()
    ts = now.strftime("%Y-%m-%d %H:%M:%S")
    hour = now.hour

    try:
        b = Bridge(BRIDGE_IP); b.connect()
    except Exception as e:
        print(f"[{ts}] Hue connect error: {e}")
        sys.exit(2)

    # 夜は消灯して終了
    if hour in NIGHT_HOURS:
        try:
            turn_off_night(b, ts)
            sys.exit(0)
        except Exception as e:
            print(f"[{ts}] Hue off error: {e}")
            sys.exit(2)

    # ここから昼間の処理（天気で色変更）
    try:
        w = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": LAT, "longitude": LON, "current_weather": True},
            timeout=10
        ).json()
        code = w["current_weather"]["weathercode"]
    except Exception as e:
        print(f"[{ts}] Weather fetch error: {e}")
        sys.exit(1)

    payload = pick_color(code)

    try:
        for name in LIGHTS:
            b.set_light(name, "on", True)
            if "ct" in payload:
                b.set_light(name, "ct", payload["ct"])
                b.set_light(name, "bri", payload["bri"])
            else:
                for k, v in payload.items():
                    b.set_light(name, k, v)
        print(f"[{ts}] Daytime OK: code={code}, set={payload}")
    except Exception as e:
        print(f"[{ts}] Hue error: {e}")
        sys.exit(2)

if __name__ == "__main__":
    main()
