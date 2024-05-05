# 資料庫 期末專題

## 歌曲資料庫

### 實體型態 :

1. **歌曲 (Song)：**
    - 屬性：
        - 歌曲ID (SongID)：唯一識別每首歌曲的編號。
        - 歌曲名稱 (Title)：歌曲的標題。
        - 藝術家 (Artist)：執行或創作該歌曲的藝術家。 多值
        - 專輯 (Album)：歌曲所屬的專輯。
        - 發布年份 (ReleaseYear)：歌曲的發布年份。
        - 時長 (Duration)：歌曲的播放時長。
2. **播放清單 (Playlist)：**
    - 屬性：
        - 清單ID (PlaylistID)：唯一識別每個播放清單的編號。
        - 清單名稱 (Name)：播放清單的名稱或標題。
        - 創建日期 (CreationDate)：播放清單的創建日期。
        - 歌曲列表 (SongList) : 清單包含的歌曲
3. **使用者 (User)：**
    - 屬性：
        - 使用者ID (UserID)：唯一識別每個使用者的編號。
        - 使用者名稱 (Username)：使用者的名稱或暱稱。
        - 密碼 (Password)：使用者的登入密碼。
        - 註冊日期 (RegistrationDate)：使用者的註冊日期。

### 關聯綱目

- Song
    - SongID -PK
    - Title
    - Album
    - ReleaseYear
    - Duration
- Artist
    - SongID -PK -FK
    - name -PK
- Playlist
    - PlaylistID -PK
    - Username
    - CreationDate
- SongList
    - PlaylistID -PK -FK
    - SongID -PK -FK
- User
    - UserID -PK
    - Username
    - Password
    - RegistrationDate

### 程式架構

- 使用網頁設計
- **Flask**, **Flask-SQLAlchemy (**[https://medium.com/seaniap/python-web-flask-使用sqlalchemy資料庫-8fc49c584ddb](https://medium.com/seaniap/python-web-flask-%E4%BD%BF%E7%94%A8sqlalchemy%E8%B3%87%E6%96%99%E5%BA%AB-8fc49c584ddb)**)**
- 使用者登入系統
- 搜尋歌曲方式
    - 曲名
    - 創作者
- 播放清單操作 (對當前使用者)
    - 創建播放清單
    - 刪除播放清單
    - 新增歌曲到撥放清單
    - 從播放清單中刪除歌曲