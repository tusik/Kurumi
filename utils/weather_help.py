import random

from PIL import Image, ImageDraw, ImageFont
import json

# 给定的天气信息 JSON
example_weather_json = '''
{
    "coord": {
        "lon": 10.99,
        "lat": 44.34
    },
    "weather": [
        {
            "id": 800,
            "main": "Clear",
            "description": "clear sky",
            "icon": "01d"
        }
    ],
    "base": "stations",
    "main": {
        "temp": 293.93,
        "feels_like": 293.81,
        "temp_min": 291.1,
        "temp_max": 294.86,
        "pressure": 1012,
        "humidity": 67,
        "sea_level": 1012,
        "grnd_level": 929
    },
    "visibility": 10000,
    "wind": {
        "speed": 3.22,
        "deg": 197,
        "gust": 5.28
    },
    "clouds": {
        "all": 1
    },
    "dt": 1719726744,
    "sys": {
        "type": 2,
        "id": 2075663,
        "country": "IT",
        "sunrise": 1719718515,
        "sunset": 1719774239
    },
    "timezone": 7200,
    "id": 3163858,
    "name": "Zocca",
    "cod": 200
}
'''


def draw_today(weather_json, save_path):
    # 解析 JSON 数据
    try:
        data = json.loads(weather_json)

        # 提取天气信息
        city = data['name']
        country = data['sys']['country']
        weather_main = data['weather'][0]['main']
        weather_description = data['weather'][0]['description']
        temp = data['main']['temp'] - 273.15  # 转换为摄氏度
        humidity = data['main']['humidity']

        # 创建图像
        width, height = 800, 400
        image = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)

        # 设置字体
        title_font = ImageFont.truetype("arial.ttf", 40)
        info_font = ImageFont.truetype("arial.ttf", 30)
        footer_font = ImageFont.truetype("arial.ttf", 20)

        # 绘制标题
        draw.text((20, 20), f"{city}, {country}", font=title_font, fill=(0, 0, 0))

        # 绘制天气信息
        draw.text((20, 80), f"Weather: {weather_main} - {weather_description}", font=info_font, fill=(0, 0, 0))
        draw.text((20, 130), f"Temperature: {temp:.1f}°C", font=info_font, fill=(0, 0, 0))
        draw.text((20, 180), f"Humidity: {humidity}%", font=info_font, fill=(0, 0, 0))

        # 绘制右下角的文本
        footer_text = "@Kurumi器人"
        bbox = draw.textbbox((0, 0), footer_text, font=footer_font)  # 获取文本的边界框
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text((width - text_width - 20, height - text_height - 20), footer_text, font=footer_font, fill=(0, 0, 0))

        rand_id = random.Random().random()*1000
        file_name = f'{save_path}/{rand_id}_weather_banner.png'
        # 保存图像
        image.save(file_name)
        return file_name
    except:
        return None

