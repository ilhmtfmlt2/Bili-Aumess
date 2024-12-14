# **哔哩哔哩自动回复开启**

> **一个通过扫码登录哔哩哔哩并开启自动回复功能的 Python 脚本**

---

## **🌟 功能特色**

- **📱 二维码登录**：通过二维码快速登录哔哩哔哩，简单快捷。
- **⚡ 自动回复管理**：轻松一键开启或关闭哔哩哔哩动态的自动回复功能。
- **🔒 安全 API 签名**：集成哔哩哔哩 API 签名算法，确保请求安全。
- **🎯 终端二维码显示**：在终端中生成可扫描二维码，方便快捷。
- **📅 会话管理**：自动提取并处理登录所需的 `bili_jct` 和 `SESSDATA`。
- **💻 无需复杂配置**：即刻运行，无需额外配置，自动化操作一键实现。

---

### 😕 不会使用代码？没关系！

如果你不熟悉如何运行代码，直接下载 **打包好的软件**：

👉 [点击这里访问 Bili-Aumess 发布页面](https://github.com/ilhmtfmlt2/Bili-Aumess/releases/tag/mian)

只需下载并运行，即可立即开启自动回复功能。

---

## **🚀 快速开始**

### 1. 克隆项目

```bash
git clone https://github.com/your_username/bilibili-auto-reply.git
cd bilibili-auto-reply
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行脚本

```bash
python main.py
```

运行脚本后，系统会：

1. 在终端中生成二维码，供您用哔哩哔哩 App 扫描登录。
2. 轮询二维码状态，直到登录成功或二维码过期。
3. 登录成功后自动开启 **自动回复功能**。

---

## **📁 项目结构**

```
├── main.py                 # 主脚本文件
├── requirements.txt        # 依赖列表
├── README.md               # 项目文档
└── api/README.md           # API 详细文档
```

---

## **📜 API 文档**

本项目调用了哔哩哔哩的 API 来实现动态自动回复功能的管理。详细 API 文档请参考 [api/README.md](api/README.md)。

### API 示例

接口地址：  
`https://api.vc.bilibili.com/link_setting/v1/link_setting/set`

请求头：

```json
{
  "Cookie": "SESSDATA=<your_sessdata>; bili_jct=<your_bili_jct>"
}
```

请求体：

```json
{
  "keys_reply": "1",
  "csrf_token": "<your_bili_jct>",
  "csrf": "<your_bili_jct>"
}
```

响应：

```json
{
  "code": 0,
  "msg": "0",
  "message": "0",
  "ttl": 1,
  "data": {}
}
```

更多详细信息请访问 [api/README.md](api/README.md)。

---

## **📸 终端二维码示例**

运行脚本后，二维码将在终端中以 ASCII 格式显示：

```
█▀▀▀▀▀█ ▄▄▄▄▄ █ ▄█▀▄ 
█ ███ █▀▄█ █▀▄▀ █ █▀█
█ ▀▀▀ █ █▄ ▄█ ▀▀█ ▄ █
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
```

使用 **哔哩哔哩 App** 扫描即可快速登录。

---

## **⚙️ 进阶用法**

### 1. 修改 API 行为

您可以在 `make_request()` 函数中自定义 API 请求的头信息和参数，满足不同需求：

```python
def make_request(bili_jct, SESSDATA):
    url = "https://api.vc.bilibili.com/link_setting/v1/link_setting/set"
    headers = {
        "Cookie": f"SESSDATA={SESSDATA}; bili_jct={bili_jct}",
        "User-Agent": "Mozilla/5.0"
    }
    data = {"keys_reply": "1", "csrf_token": bili_jct, "csrf": bili_jct}
    response = requests.post(url, headers=headers, data=data)
```

### 2. 错误处理

`poll_qrcode()` 函数内支持对常见错误的处理，例如二维码过期或未扫描：

```python
if response['code'] == 86038:
    print("二维码已过期，请重新获取。")
elif response['code'] == 86039:
    print("等待扫描二维码...")
```

---

## **🌐 常见问题**

### **Q: 什么是 `bili_jct` 和 `SESSDATA`？**
- `bili_jct` 和 `SESSDATA` 是哔哩哔哩会话的关键 Cookie，必须通过成功登录后提取。

### **Q: 为什么二维码无法显示？**
- 确保您的终端支持 ASCII 字符。如果不支持，可以考虑使用图形化 QR 代码库。

### **Q: 如何关闭自动回复？**
- 将请求体中的 `keys_reply` 参数改为 `"0"` 即可关闭自动回复功能。

---

## **💡 贡献方式**

欢迎任何形式的贡献！  
请按以下步骤操作：

1. Fork 此仓库。
2. 创建新分支：`git checkout -b feature/your-feature`。
3. 提交更改：`git commit -m '添加新功能'`。
4. 推送分支：`git push origin feature/your-feature`。
5. 创建 Pull Request，我们会尽快处理。

---

## **📄 开源协议**

本项目基于 MIT 协议开源，详情请参见 [LICENSE](LICENSE)。

---

## **📬 联系方式**

如果您有任何问题或建议，请联系开发者：  
[theoldtimes@foxmail.com](mailto:theoldtimes@foxmail.com)

