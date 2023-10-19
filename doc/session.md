- flask 裡的 session 必須要設定 ​​SECRET_KEY​
- session 預設過期時間在關閉瀏覽器之後
- 如果設定 session.permanent=True, 則預設在 31 天後過期
- 可自定義過期時間
    ```python
    # 表示在 2 小時後過期
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hour=2) 
    ```
    