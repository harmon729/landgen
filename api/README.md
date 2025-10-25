# LandGen API 后端

## 📁 文件结构

```
api/
├── core.py           # 核心业务逻辑（共享模块）
├── generate.py       # Vercel Serverless 入口
├── main.py           # 本地开发服务器
├── test_local.py     # 测试脚本
├── requirements.txt  # Python 依赖
└── README.md         # 本文档
```

## 🎯 模块职责

### `core.py` - 核心业务逻辑

包含所有共享的业务逻辑：

**数据模型**

- `GenerateRequest`: 请求模型
- `UserProfile`: GitHub 用户资料
- `Repository`: 仓库信息
- `GenerateResponse`: API 响应

**功能函数**

- `fetch_github_user()`: 获取 GitHub 用户信息
- `fetch_github_repos()`: 获取仓库列表
- `fetch_readme()`: 获取 README 内容
- `generate_ai_summary()`: 使用 Gemini AI 生成项目摘要
- `process_generate_request()`: 完整的网站生成流程

### `generate.py` - Vercel 部署入口

- 用于 Vercel Serverless 部署
- 路由：`POST /` (Vercel 映射到 `/api/generate`)
- 精简到 26 行代码

### `main.py` - 本地开发服务器

- 用于本地开发和测试
- 路由：
  - `GET /`: 健康检查
  - `POST /api/generate`: 生成网站
- 包含 uvicorn 启动配置

### `test_local.py` - 测试脚本

- 测试 GitHub API 集成
- 测试 Gemini AI 集成
- 验证完整流程

## 🚀 使用方法

### 本地开发

1. **安装依赖**

```bash
pip install -r requirements.txt
```

2. **设置环境变量**

```bash
# 创建 .env 文件或设置环境变量
export GEMINI_API_KEY=your_gemini_api_key
export GITHUB_TOKEN=your_github_token  # 可选
```

3. **运行测试**

```bash
python test_local.py
```

4. **启动开发服务器**

```bash
python main.py
# 访问 http://localhost:8000
```

### Vercel 部署

Vercel 会自动：

1. 检测 `generate.py`
2. 安装 `requirements.txt` 中的依赖
3. 将 `/api/generate` 路由到 `generate.py`

**环境变量配置**（在 Vercel Dashboard）：

- `GEMINI_API_KEY`: 必需
- `GITHUB_TOKEN`: 可选

## 📊 代码统计

### 重构前

```
generate.py:  244 行
main.py:      293 行
--------------------
总计:        537 行
重复代码:    ~200 行 (37%)
```

### 重构后

```
core.py:       254 行 (新建)
generate.py:    26 行 (-218 行)
main.py:        42 行 (-251 行)
test_local.py:  71 行 (更新)
--------------------
总计:         393 行
重复代码:       0 行 (0%)
```

**改进：**

- ✅ 总代码量减少 27%
- ✅ 消除所有重复代码
- ✅ 可维护性大幅提升

## 🔧 API 端点

### 生产环境 (Vercel)

```
POST https://your-app.vercel.app/api/generate
```

### 本地开发

```
GET  http://localhost:8000/               # 健康检查
POST http://localhost:8000/api/generate   # 生成网站
```

### 请求格式

```json
{
  "username": "torvalds"
}
```

### 响应格式

```json
{
  "success": true,
  "user": {
    "login": "torvalds",
    "name": "Linus Torvalds",
    "avatar_url": "...",
    "bio": "...",
    ...
  },
  "repositories": [
    {
      "name": "linux",
      "description": "...",
      "stargazers_count": 123456,
      "ai_summary": "AI 生成的项目摘要...",
      ...
    }
  ],
  "message": "Successfully generated website for torvalds"
}
```

## 🧪 测试

### 运行完整测试

```bash
python test_local.py
```

### 手动测试

```bash
# 启动服务器
python main.py

# 在另一个终端
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"username":"torvalds"}'
```

## 📝 开发指南

### 添加新功能

1. **在 `core.py` 中实现业务逻辑**

```python
async def new_feature():
    # 实现新功能
    pass
```

2. **两个入口文件自动继承**
   - `generate.py` 和 `main.py` 都使用 `core.py`
   - 无需在两处重复代码

### 修改现有功能

1. **只修改 `core.py`**

```python
# 修改 core.py 中的函数
async def generate_ai_summary(...):
    # 更新实现
    pass
```

2. **两个环境同步生效**
   - 本地开发环境
   - Vercel 生产环境

### 最佳实践

✅ **推荐**

```python
# 从 core 导入
from core import GenerateRequest, process_generate_request
```

❌ **避免**

```python
# 不要在 generate.py 和 main.py 之间互相导入
from generate import something  # 错误！
from main import something      # 错误！
```

## 🔐 安全

### 环境变量

- ✅ API 密钥通过环境变量传递
- ✅ 不在代码中硬编码密钥
- ✅ `.gitignore` 已配置忽略 `.env` 文件

### CORS 配置

- ⚠️ 当前允许所有来源 (`allow_origins=["*"]`)
- 🔒 生产环境建议限制到特定域名

### 速率限制

- ⚠️ 当前无速率限制
- 💡 未来版本可添加 `slowapi` 或类似工具

## 📚 相关文档

- `../REFACTORING_NOTES.md`: 详细的重构说明
- `../PROJECT_HEALTH_REPORT.md`: 项目健康检查报告
- `../ENV_SETUP.md`: 环境变量设置指南
- `../README.md`: 项目主文档

## 🐛 故障排查

### 问题：ImportError: No module named 'core'

**解决方案：**

```bash
# 确保在 api/ 目录下运行
cd api
python test_local.py
```

### 问题：AI summary not available

**原因：**

- `GEMINI_API_KEY` 未设置
- API 配额已用完
- 网络连接问题

**解决方案：**

```bash
# 检查环境变量
echo $GEMINI_API_KEY

# 设置环境变量
export GEMINI_API_KEY=your_key_here
```

### 问题：GitHub API rate limit

**原因：**

- 未认证的请求限制为 60/小时
- 已认证的请求限制为 5000/小时

**解决方案：**

```bash
# 设置 GitHub Token
export GITHUB_TOKEN=your_token_here
```

## 📈 性能

### 典型响应时间

- GitHub 用户信息: ~200ms
- GitHub 仓库列表: ~300ms
- README 获取: ~200ms
- AI 摘要生成: 2-5 秒

**总计: 3-8 秒**

### 优化建议

- 添加 Redis 缓存
- 并行处理多个仓库
- 使用 CDN 缓存静态资源

---

**维护者：** LandGen Team  
**最后更新：** 2025-10-25  
**版本：** v0.1.0 (Refactored)
