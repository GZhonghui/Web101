# 04_https 启用 HTTPS 服务 并且 使用反向代理

## 环境
- 证书使用 [acme.sh](https://wiki.gzher.com/doku.php?id=%E8%BD%AF%E4%BB%B6:linux:%E5%AE%89%E8%A3%85ssl%E8%AF%81%E4%B9%A6) 申请
- node v23.4.0
- express@4.21.2

## Node 端 server.js
```js
// 需要开启信任代理
// 当使用反向代理时，实际的客户端 IP 地址会被代理服务器（Apache2）的 IP 地址替代
// 设置 trust proxy 后，Express 会信任代理服务器传递的 HTTP 头（如 X-Forwarded-For, X-Forwarded-Proto 等）
// 从而可以获取到真实的客户端 IP 地址
app.set('trust proxy', true);

...

// 绑定地址和端口的时候，使用 localhost:<非常用端口> 即可
const PORT = 3001;

app.listen(PORT, 'localhost', () => {
    console.log(`server is running on http://localhost:${PORT}`);
});

...

// 其他代码保持不变即可
```

## Apache 端
```shell
# 启用 SSL 和代理模块
sudo a2enmod ssl
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod headers
sudo a2enmod remoteip
```

```
# HTTP 虚拟主机配置 (/etc/apache2/sites-available/your-site.conf)
<VirtualHost *:80>
    ServerName example.com
    ServerAdmin webmaster@example.com

    # 重定向所有 HTTP 流量到 HTTPS
    # 直接重定向到首页 这种做法比较简单
    Redirect permanent / https://example.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName example.com
    
    # 启用 SSL
    SSLEngine on
    SSLCertificateFile /path/to/your/certificate.crt
    SSLCertificateKeyFile /path/to/your/private.key
    SSLCertificateChainFile /path/to/chain.crt  # 如果需要的话
    
    # 启用代理
    ProxyPreserveHost On
    
    # 添加请求头转发
    RequestHeader set X-Forwarded-Proto "https"
    RequestHeader set X-Forwarded-SSL "on"
    
    # 转发真实的客户端IP
    ProxyAddHeaders On
    RemoteIPHeader X-Forwarded-For
    
    ProxyPass / http://localhost:3001/
    ProxyPassReverse / http://localhost:3001/
    
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

```