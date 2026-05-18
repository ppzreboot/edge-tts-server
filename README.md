# edge-tts-server

把 [edge-tts](https://github.com/rany2/edge-tts)（微软 Edge 在线语音合成）包成 **HTTP API**。

> **许可说明：** 本项目代码可自由使用；依赖库 [edge-tts](https://github.com/rany2/edge-tts) 采用 **GPL-3.0**。若你分发或商用集成该库，请注意 GPL 合规要求。


## 环境变量

> 注意，下面的 api_key 不需要你在哪里购买，而是相当于你自己设置的密码。只有持有正确的密码，才能得到正常响应。

| 变量 | 必填 | 默认值 |
|------|------|--------|
| `PORT` | 否 | `8000` | 监听端口 |
| `ENABLE_DOCS` | 否 | 关闭 | 设为 `true` 时开启 `/docs`、`/redoc` |
| `API_KEY` | 生产建议必填 | 空 | 访问密钥 |
| `MAX_TEXT_LENGTH` | 否 | `5000` | `text` 最大字符数 |

参考 [`.env.example`](.env.example)。


## 本地测试

### 准备 Python

需要 **Python 3.10+**。

```bash
python3 --version
```

### 创建虚拟环境并安装依赖

```bash
cd edge-tts-server
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 启动服务

```bash
cp .env.example .env                  # 按需修改
export $(grep -v '^#' .env | xargs)   # 或手动 export 各变量

python app.py
```

**交互式 API 文档：** 需 `ENABLE_DOCS=true`，然后打开 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)。


## 部署到 Vercel

```bash
npm i -g vercel
vercel login
cd edge-tts-server
vercel deploy --prod
```

在 Vercel 控制台至少设置：

- `API_KEY`：生产密钥
- `ENABLE_DOCS`：`false`（或不设置）
- `MAX_TEXT_LENGTH`：按需

`PORT` 由平台注入，无需配置。

官方文档：[Deploy a FastAPI app on Vercel](https://vercel.com/docs/frameworks/backend/fastapi)

---

## 接口说明

### `GET /health`
健康检查。

- **响应：** `200`，`{"status":"ok"}`

### `GET /voices`
可用音色列表。

#### 请求

- **Header:**
  - `Authorization: Bearer <API_KEY>`
- **查询参数:**

| 参数 | 必填 | 说明 |
|------|------|------|
| `locale` | 否 | 按语言区域前缀过滤，如 `zh-CN`、`en-US` |

#### 成功响应

```json
{
  "prosody": {
    "rate": { "format": "^[+-]\\d+%$", "range": "[-50%, +100%]", "example": "+10%" },
    "volume": { "format": "^[+-]\\d+%$", "range": "[-50%, +50%]", "example": "-20%" },
    "pitch": { "format": "^[+-]\\d+Hz$", "range": "[-50Hz, +50Hz]", "example": "+5Hz" }
  },
  "count": 2,
  "voices": [
    {
      "Name": "Microsoft Server Speech Text to Speech Voice (zh-CN, XiaoxiaoNeural)",
      "ShortName": "zh-CN-XiaoxiaoNeural",
      "Gender": "Female",
      "Locale": "zh-CN",
      "FriendlyName": "Microsoft Xiaoxiao Online (Natural) - Chinese (Mainland)"
    }
  ]
}
```

合成时请使用每条音色的 **`ShortName`** 作为 `POST /tts` 的 `voice` 字段。

### `POST /tts`

将文本合成为 MP3。

#### 请求

- **Header:**
  - `Content-Type: application/json`
  - `Authorization: Bearer <API_KEY>`

- **Body(JSON) :**

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `text` | string | 是 | — | 要朗读的文本，长度 ≤ `MAX_TEXT_LENGTH` |
| `voice` | string | 否 | `zh-CN-XiaoxiaoNeural` | 音色 `ShortName`，见 `GET /voices` |
| `rate` | string | 否 | `+0%` | 语速，见上文「韵律参数」 |
| `volume` | string | 否 | `+0%` | 音量 |
| `pitch` | string | 否 | `+0Hz` | 音高 |

#### 响应

| Status | 含义 |
|--------|------|
| `200` | 成功，`Content-Type: audio/mpeg`，body 为 MP3 |
| `401` | 未提供或错误的 `Authorization` |
| `422` | 请求体不合法（如 `text` 超长、`rate` 超出范围） |
| `502` | 上游 TTS 或音色列表失败 |

---

## 常见问题

**Q：和 Azure Speech API 有什么区别？**  
本服务通过 edge-tts 调用 Edge 同款在线能力，无需微软 API Key，但属于非官方接口。
