
# API接口说明


### 接口地址

`https://api.vc.bilibili.com/link_setting/v1/link_setting/set`

---

## 功能描述

该接口用于设置 Bilibili 回复功能开关，支持开启和关闭自动回复。

---

## 请求方式

`POST`

---

## 请求参数

### Headers

| 参数名    | 类型   | 是否必需 | 描述                   |
|-----------|--------|----------|------------------------|
| `bili_jct` | String | 是        | 用户的 CSRF Token      |
| `SESSDATA` | String | 是        | 用户的登录 Session 数据 |

### Body

| 参数名       | 类型   | 是否必需 | 描述                              |
|--------------|--------|----------|-----------------------------------|
| `keys_reply` | String | 是        | 回复功能开关，`1` 表示开启，`0` 表示关闭 |
| `csrf_token` | String | 是        | CSRF Token，与 `csrf` 参数值一致  |
| `csrf`       | String | 是        | CSRF Token，与 `csrf_token` 参数值一致 |

> **注意**: `csrf`、`csrf_token` 和 `bili_jct` 的值必须保持一致。

---

## 示例

### 请求示例

#### Headers

```json
{
  "bili_jct": "your_csrf_token",
  "SESSDATA": "your_sessdata"
}
```

#### Body

```json
{
  "keys_reply": "1",
  "csrf_token": "b4cef918bb0486a4bd0d7b9213d0948d",
  "csrf": "b4cef918bb0486a4bd0d7b9213d0948d"
}
```

---

## 响应说明

| 参数名    | 类型   | 描述                          |
|-----------|--------|-------------------------------|
| `code`    | Int    | 状态码，`0` 表示请求成功      |
| `msg`     | String | 响应消息，通常为 `"0"`         |
| `message` | String | 与 `msg` 内容一致             |
| `ttl`     | Int    | TTL 值，通常为 `1`            |
| `data`    | Object | 返回数据内容，通常为空        |

---

## 响应示例

```json
{
  "code": 0,
  "msg": "0",
  "message": "0",
  "ttl": 1,
  "data": {}
}
```

> **注意**: 如果 HTTP 响应状态码为 `200`，且 `code` 为 `0`，则表示操作成功。

---

## 功能说明

1. **功能开关**:
   - `keys_reply` 值为 `1`：开启自动回复功能。
   - `keys_reply` 值为 `0`：关闭自动回复功能。
2. **请求前提**:
   - 用户必须已登录，并且 `bili_jct` 和 `SESSDATA` 是有效的。
3. **参数一致性**:
   - `csrf`、`csrf_token` 和 `bili_jct` 必须保持一致。

---

## 状态码说明

| 状态码 | 描述       |
|--------|------------|
| `200`    | 请求成功   |
| `0`    | 请求成功   |
| 其他    | 请求失败，请根据响应内容排查问题 |

---

> **注意**: 该接口Python运行时候可能出现返回结果不规则原因未知，状态码为200即为开启成功可以忽视。

## License

本项目基于 [MIT License](./LICENSE) 开源。
