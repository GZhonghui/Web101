const express = require('express');
const path = require('path');
const app = express();

// 信任代理设置
// 在开启 HTTPS 并且使用反向代理的时候，需要设置信任代理
app.set('trust proxy', true);

// 设置静态文件目录
app.use(express.static(path.join(__dirname, 'public')));

// 基本的路由响应
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// 设置监听端口（可以根据需要修改）
const PORT = 3001;

app.listen(PORT, 'localhost', () => {
    console.log(`server is running on http://localhost:${PORT}`);
});
