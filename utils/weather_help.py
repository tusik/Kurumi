import io
import math
import random
from enum import Enum
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
            "id": 804,
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

font_name = r"SourceHanSans-VF.ttf.ttc"
class WeatherCondition(Enum):
    THUNDERSTORM_WITH_LIGHT_RAIN = (200, "雷暴", "雷暴伴有小雨", "11d")
    THUNDERSTORM_WITH_RAIN = (201, "雷暴", "雷暴伴有雨", "11d")
    THUNDERSTORM_WITH_HEAVY_RAIN = (202, "雷暴", "雷暴伴有大雨", "11d")
    LIGHT_THUNDERSTORM = (210, "雷暴", "轻度雷暴", "11d")
    THUNDERSTORM = (211, "雷暴", "雷暴", "11d")
    HEAVY_THUNDERSTORM = (212, "雷暴", "重度雷暴", "11d")
    RAGGED_THUNDERSTORM = (221, "雷暴", "不规则雷暴", "11d")
    THUNDERSTORM_WITH_LIGHT_DRIZZLE = (230, "雷暴", "雷暴伴有轻度毛毛雨", "11d")
    THUNDERSTORM_WITH_DRIZZLE = (231, "雷暴", "雷暴伴有毛毛雨", "11d")
    THUNDERSTORM_WITH_HEAVY_DRIZZLE = (232, "雷暴", "雷暴伴有重度毛毛雨", "11d")

    LIGHT_INTENSITY_DRIZZLE = (300, "毛毛雨", "轻度毛毛雨", "09d")
    DRIZZLE = (301, "毛毛雨", "毛毛雨", "09d")
    HEAVY_INTENSITY_DRIZZLE = (302, "毛毛雨", "重度毛毛雨", "09d")
    LIGHT_INTENSITY_DRIZZLE_RAIN = (310, "毛毛雨", "轻度毛毛雨雨", "09d")
    DRIZZLE_RAIN = (311, "毛毛雨", "毛毛雨雨", "09d")
    HEAVY_INTENSITY_DRIZZLE_RAIN = (312, "毛毛雨", "重度毛毛雨雨", "09d")
    SHOWER_RAIN_AND_DRIZZLE = (313, "毛毛雨", "阵雨和毛毛雨", "09d")
    HEAVY_SHOWER_RAIN_AND_DRIZZLE = (314, "毛毛雨", "重度阵雨和毛毛雨", "09d")
    SHOWER_DRIZZLE = (321, "毛毛雨", "毛毛雨阵雨", "09d")

    LIGHT_RAIN = (500, "雨", "小雨", "10d")
    MODERATE_RAIN = (501, "雨", "中雨", "10d")
    HEAVY_INTENSITY_RAIN = (502, "雨", "大雨", "10d")
    VERY_HEAVY_RAIN = (503, "雨", "暴雨", "10d")
    EXTREME_RAIN = (504, "雨", "特大暴雨", "10d")
    FREEZING_RAIN = (511, "雨", "冻雨", "13d")
    LIGHT_INTENSITY_SHOWER_RAIN = (520, "雨", "轻度阵雨", "09d")
    SHOWER_RAIN = (521, "雨", "阵雨", "09d")
    HEAVY_INTENSITY_SHOWER_RAIN = (522, "雨", "重度阵雨", "09d")
    RAGGED_SHOWER_RAIN = (531, "雨", "不规则阵雨", "09d")

    LIGHT_SNOW = (600, "雪", "小雪", "13d")
    SNOW = (601, "雪", "雪", "13d")
    HEAVY_SNOW = (602, "雪", "大雪", "13d")
    SLEET = (611, "雪", "雨夹雪", "13d")
    LIGHT_SHOWER_SLEET = (612, "雪", "轻度雨夹雪阵雨", "13d")
    SHOWER_SLEET = (613, "雪", "雨夹雪阵雨", "13d")
    LIGHT_RAIN_AND_SNOW = (615, "雪", "小雨和雪", "13d")
    RAIN_AND_SNOW = (616, "雪", "雨和雪", "13d")
    LIGHT_SHOWER_SNOW = (620, "雪", "轻度雪阵雨", "13d")
    SHOWER_SNOW = (621, "雪", "雪阵雨", "13d")
    HEAVY_SHOWER_SNOW = (622, "雪", "重度雪阵雨", "13d")

    MIST = (701, "大气", "薄雾", "50d")
    SMOKE = (711, "大气", "烟雾", "50d")
    HAZE = (721, "大气", "霾", "50d")
    SAND_DUST_WHIRLS = (731, "大气", "沙尘暴", "50d")
    FOG = (741, "大气", "雾", "50d")
    SAND = (751, "大气", "沙", "50d")
    DUST = (761, "大气", "尘", "50d")
    VOLCANIC_ASH = (762, "大气", "火山灰", "50d")
    SQUALLS = (771, "大气", "狂风", "50d")
    TORNADO = (781, "大气", "龙卷风", "50d")

    CLEAR_SKY_DAY = (800, "晴", "晴天", "01d")
    CLEAR_SKY_NIGHT = (800, "晴", "晴天", "01n")

    FEW_CLOUDS_DAY = (801, "云", "少云", "02d")
    FEW_CLOUDS_NIGHT = (801, "云", "少云", "02n")
    SCATTERED_CLOUDS_DAY = (802, "云", "多云", "03d")
    SCATTERED_CLOUDS_NIGHT = (802, "云", "多云", "03n")
    BROKEN_CLOUDS_DAY = (803, "云", "阴天", "04d")
    BROKEN_CLOUDS_NIGHT = (803, "云", "阴天", "04n")
    OVERCAST_CLOUDS_DAY = (804, "云", "阴天", "04d")
    OVERCAST_CLOUDS_NIGHT = (804, "云", "阴天", "04n")

    @classmethod
    def get_by_code(cls, code):
        for condition in cls:
            if condition.value[0] == code:
                return condition
        raise ValueError(f"No weather condition found for code {code}")


def create_radial_gradient(size, center, max_radius, start_color, end_color):
    width, height = size
    img = Image.new('RGBA', size)
    draw = ImageDraw.Draw(img)

    r1, g1, b1 = start_color
    r2, g2, b2 = end_color

    for x in range(width):
        for y in range(height):
            # 计算当前像素到中心点的距离
            distance = math.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
            # 计算颜色插值
            if distance > max_radius:
                distance = max_radius
            ratio = distance / max_radius
            r = int(r1 + ratio * (r2 - r1))
            g = int(g1 + ratio * (g2 - g1))
            b = int(b1 + ratio * (b2 - b1))
            draw.point((x, y), (r, g, b,255))

    return img


def draw_weather_icon(weather_code, img):
    wc = WeatherCondition.get_by_code(weather_code)
    weather_icon = Image.open(f'resource/weather/{wc.value[3]}@4x.png').convert("RGBA").resize((128,128))
    x, y = img.size
    img.paste(weather_icon, (x - 128 - 20, 20), weather_icon)

    return img


def draw_background(weather_code):
    size = (800, 400)
    center = (800 - 64 - 20, 64 + 20)
    max_radius = 888
    weather = int(weather_code / 100)
    start_color = (173, 216, 230)
    end_color = (204, 204, 204)
    if weather == 5:
        start_color = (135, 206, 250)
        end_color = (80, 100, 120)
    elif weather == 8:
        start_color = (56, 154, 186)
        end_color = (204, 204, 204)
        max_radius = 2000 - (weather_code - 800) * 400
    elif weather == 2:
        start_color = (255, 255, 255)
        end_color = (108, 108, 118)
        max_radius = 2000 - (weather_code - 800) * 400

    img = create_radial_gradient(size, center, max_radius, start_color, end_color)
    return img


def draw_today(weather_json, save_path):
    # 解析 JSON 数据
    try:
        data = json.loads(weather_json)

        # 提取天气信息
        city = data['name']
        country = data['sys']['country']
        weather_main = data['weather'][0]['main']
        weather_code = data['weather'][0]["id"]
        weather_description = data['weather'][0]['description']
        temp = data['main']['temp'] - 273.15  # 转换为摄氏度
        humidity = data['main']['humidity']

        # 创建图像
        width, height = 800, 400
        #image = Image.new('RGB', (width, height), color=(255, 255, 255))
        image = draw_background(weather_code)
        draw = ImageDraw.Draw(image)

        # 设置字体
        title_font = ImageFont.truetype(font_name, 40)
        info_font = ImageFont.truetype(font_name, 30)
        footer_font = ImageFont.truetype(font_name, 20)

        # 绘制标题
        draw.text((20, 20), f"{city}, {country}", font=title_font, fill=(0, 0, 0))

        # 绘制天气信息
        draw.text((20, 80), f"Weather: {weather_main} - {weather_description}", font=info_font, fill=(0, 0, 0))
        draw.text((20, 130), f"Temperature: {temp:.1f}°C", font=info_font, fill=(0, 0, 0))
        draw.text((20, 180), f"Humidity: {humidity}%", font=info_font, fill=(0, 0, 0))

        # 绘制右下角的文本
        footer_text = "@Kurumi"
        bbox = draw.textbbox((0, 0), footer_text, font=footer_font)  # 获取文本的边界框
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text((width - text_width - 20, height - text_height - 20), footer_text, font=footer_font, fill=(0, 0, 0))

        image = draw_weather_icon(weather_code, image)

        rand_id = int(random.Random().random() * 10000)
        file_name = f'{save_path}/{rand_id}_weather_banner.png'
        # 保存图像
        image.save(file_name)
        return file_name
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    draw_today(example_weather_json, 'D:/cache/')
