# Session 基礎設定

- flask 裡的 session 必須要設定 ​​SECRET_KEY​

# Session 過期時間

- session 預設過期時間在關閉瀏覽器之後
- 如果設定 session.permanent=True, 則預設在 31 天後過期
- 可自定義過期時間
    ```python
    # 表示在 2 小時後過期
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2) 
    ```
    
# 將 session 存在 server 端

透過 flask-session 將 session 存在 server 端, 可支援以下方式
- redis (較優, 讀寫速度快)
- memcached
- filesystem
- mongodb
- sqlalchmey

```bash=
pip install flask-session
pip install redis
```