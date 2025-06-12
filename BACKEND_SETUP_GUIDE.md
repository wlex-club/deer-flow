# 🔧 DeerFlow 后端连接问题解决指南

## 问题描述
当你看到以下错误时：
```
Failed to fetch
Error: Failed to fetch
src\core\api\rag.ts (19:10) @ getRAGConfig
```

这意味着前端无法连接到后端API服务器。

## 🚀 快速解决方案

### 方法一：使用自动启动脚本（推荐）

1. **双击运行启动脚本**：
   - Windows: 双击 `start-backend.bat`
   - PowerShell: 双击 `start-backend.ps1`

2. **等待服务器启动**，直到看到：
   ```
   ✅ Server is running
   📍 Server will be available at: http://localhost:8000
   ```

3. **刷新网页**，错误应该消失

### 方法二：手动启动

1. **打开PowerShell**（在项目目录右键 → "在终端中打开"）

2. **激活虚拟环境**：
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. **启动服务器**：
   ```powershell
   uv run server.py --reload
   ```

## 🔍 问题诊断

现在前端会自动显示后端连接状态：

- 🟢 **Backend Connected** - 一切正常
- 🟡 **Connecting...** - 正在连接中
- 🔴 **Backend Offline** - 需要启动后端服务器

## 📋 常见问题

### 1. 虚拟环境问题
如果看到"Virtual environment not found"：
```bash
# 重新创建虚拟环境
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 端口占用
如果看到"Port 8000 is already in use"：
```powershell
# 查找占用端口的进程
netstat -ano | findstr :8000
# 终止进程（替换XXXX为实际PID）
taskkill /PID XXXX /F
```

### 3. 依赖缺失
如果看到"Module not found"错误：
```bash
.venv\Scripts\activate
pip install fastapi uvicorn python-multipart
```

### 4. 配置文件缺失
如果看到配置相关错误：
```bash
# 复制配置文件模板
copy conf.yaml.example conf.yaml
# 然后编辑 conf.yaml 文件，添加你的API密钥
```

## 🎯 验证步骤

1. **检查服务器状态**：
   - 访问 http://localhost:8000/api/rag/config
   - 应该返回JSON格式的配置信息

2. **检查前端连接**：
   - 打开浏览器开发者工具（F12）
   - 查看Console标签，应该看到：
     ```
     🔍 Checking server status at: http://localhost:8000/api/rag/config
     ✅ Server is running and responsive
     ```

3. **检查网络状态指示器**：
   - 页面右下角应该显示"Backend Connected"

## 🔄 如果问题仍然存在

1. **重启所有服务**：
   ```bash
   # 停止前端 (Ctrl+C)
   # 停止后端 (Ctrl+C)
   # 重新启动后端
   uv run server.py --reload
   # 重新启动前端
   npm run dev
   ```

2. **清除缓存**：
   ```bash
   # 清除Next.js缓存
   npm run build
   # 或者删除 .next 文件夹
   ```

3. **检查防火墙设置**：
   - 确保Windows防火墙允许Python访问网络
   - 确保端口8000没有被其他程序占用

## 📞 获取帮助

如果以上方法都无法解决问题，请：

1. 打开浏览器开发者工具（F12）
2. 查看Console和Network标签中的详细错误信息
3. 运行服务器时截图终端输出
4. 提供具体的错误信息以获得更好的帮助

---

**💡 提示**: 现在前端会自动检测后端状态并提供详细的诊断信息，只需查看浏览器控制台即可获得具体的解决建议！ 