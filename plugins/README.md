## 插件开发

目前推荐单文件开发模式，暨只用一个py文件完成对输入输出处理过程。

### 开发方式

插件文件都保存与plugins目录下，bot程序会在程序启动时自动扫描并创建Plugin子类的实例对象。

### 插件的基本框架

插件需要继承Plugin，并使用`@KurumiPlugin`装饰器注册插件的名字和基本命令路径。

例如：
```python
@KurumiPlugin(name="Weather", route="天气")
class Weather(Plugin):
```
此插件名为Weather并使用`/天气`作为插件入口。

实现`register_commands`方法对插件消息参数进行处理，默认入口为`main`，当消息参数无法继续匹配到子命令入口之后，则会将参数传递到注册为`main`的函数参数上。

```python
    def register_commands(self):
        @self.cmd("main", "获取天气信息")
        async def weather(self, message: KurumiMessage, params=None):
```

当用户发送`@机器人 /天气 北京`时，首先查找`/天气`插件入口，并在天气插件中没有命中其他函数，于是会将`北京`参数传递给`weather`函数。由此函数处理消息。

## 统一消息结构
KurumiMessage集合频道消息，群消息为一体。将回复内容保存至其中，并调用Plugin的reply函数发送消息。