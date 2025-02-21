// 引入 express 框架，express 是 node.js 的 web 框架
// express 需要安装：npm install express
const express = require('express');
const path = require('path'); // 引入 path 模块，用于处理和转换文件路径
const fs = require('fs'); // 引入 fs 模块，用于文件操作

const app = express(); // 创建 express 应用

// ===== 中间件配置 =====
// express.json(): 解析请求中的 JSON 数据，使其可通过 req.body 访问
// express.static(): 提供静态文件服务，使 public 目录下的文件可直接访问
app.use(express.json());
app.use(express.static('public'));

// 用户数据文件路径
const USER_FILE = path.join(__dirname, 'users.json');

// 确保用户文件存在，如不存在则创建空数组文件
if (!fs.existsSync(USER_FILE)) {
    fs.writeFileSync(USER_FILE, JSON.stringify([]));
}

// 如何理解路由
// 路由是 express 应用中的一个重要概念，它定义了客户端请求与服务器端处理函数之间的映射关系。
// 通过定义不同的路由，可以处理不同类型的 HTTP 请求，如 GET、POST、PUT、DELETE 等。
// 路由通常由一个路径和一个处理函数组成，路径用于匹配客户端请求的 URL，处理函数用于处理请求并返回响应。

// HTTP 请求方法
// GET：获取资源，GET 请求的数据通过 URL 传递 例如：/api/user?username=tom&age=18（浏览器通常会缓存 GET 请求）
// POST：创建资源，POST 请求的数据在请求体（body）中传递
// 总结来说，GET：适合获取数据；POST：适合提交数据
// PUT：更新资源
// DELETE：删除资源

// 注册路由：处理用户注册请求
// post 表示请求方法，表示客户端发送 POST 请求到服务器
// /api/register 表示请求的路径，表示客户端请求的 URL 路径
// (req, res) => { ... } 表示处理请求的函数，req 是请求对象，res 是响应对象
app.post('/api/register', (req, res) => {
    const { username, password } = req.body;
    
    // 读取现有用户数据
    const users = JSON.parse(fs.readFileSync(USER_FILE));
    
    // 检查用户名是否已存在
    if (users.find(u => u.username === username)) {
        // 这里使用 return 是因为一旦用户名已存在，就不需要继续执行后面的代码
        return res.status(400).json({ message: 'Username already exists' });
    }
    
    // 添加新用户并保存
    users.push({ username, password });
    fs.writeFileSync(USER_FILE, JSON.stringify(users, null, 2));
    
    // 返回 201 状态码，表示资源创建成功 201 是 HTTP 状态码，表示请求成功并创建了新的资源
    // 这里不需要 return，因为这是函数的最后一条语句，执行完这行代码后函数自然结束
    res.status(201).json({ message: 'Registration successful' });
});

// 登录路由：处理用户登录请求
app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    
    // 读取用户数据
    const users = JSON.parse(fs.readFileSync(USER_FILE));
    
    // 验证用户名和密码
    const user = users.find(u => u.username === username && u.password === password);
    if (!user) {
        return res.status(400).json({ message: 'Invalid username or password' });
    }
    
    res.json({ message: 'Login successful' });
});

// 启动服务器，监听 3000 端口
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});