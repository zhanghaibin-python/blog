# Blog Project API 文档

本文档描述了 Blog 项目的 API 接口。

**Base URL**: `/api/v1/`

## 认证 (Authentication)

部分接口需要 JWT 认证。
**Header**: `Authorization: Bearer <access_token>`

---

## 1. 用户模块 (Users)

### 1.1 注册用户 (Register)
*   **URL**: `/users/`
*   **Method**: `POST`
*   **Permission**: AllowAny
*   **Request Body**:
    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```
*   **Response (201 Created)**:
    ```json
    {
        "message": "注册成功"
    }
    ```
*   **Response (400 Bad Request)**:
    ```json
    {
        "username": ["用户名已存在! "]
    }
    ```

### 1.2 用户登录 (Login)
*   **URL**: `/auth/login/`
*   **Method**: `POST`
*   **Permission**: AllowAny
*   **Request Body**:
    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```
*   **Response (200 OK)**:
    ```json
    {
        "message": "登录成功! ",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbG...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbG..."
    }
    ```

### 1.3 获取当前用户信息 (Current User)
*   **URL**: `/users/me/`
*   **Method**: `GET`
*   **Permission**: IsAuthenticated (需要登录)
*   **Headers**: `Authorization: Bearer <token>`
*   **Response (200 OK)**:
    ```json
    {
        "username": "current_username"
    }
    ```
*   **Response (401 Unauthorized)**:
    ```json
    {
        "message": "用户未登录! "
    }
    ```

### 1.4 退出登录 (Logout)
*   **URL**: `/auth/logout/`
*   **Method**: `POST`
*   **Permission**: AllowAny (虽然通常需要登录，但代码未强制)
*   **Response (200 OK)**:
    ```json
    {
        "message": "已退出登录! "
    }
    ```

---

## 2. 文章模块 (Articles)

### 2.1 获取文章列表 (List Articles)
*   **URL**: `/articles/`
*   **Method**: `GET`
*   **Permission**: IsAuthenticated (需要登录 - *注意：代码中限制了必须登录才能查看列表*)
*   **Headers**: `Authorization: Bearer <token>`
*   **Query Parameters**: 无
*   **Response (200 OK)**:
    ```json
    [
        {
            "title": "文章标题",
            "category": "分类名称",
            "tags": "标签名称"
        },
//        ...
    ]
    ```

### 2.2 创建文章 (Create Article)
*   **URL**: `/articles/`
*   **Method**: `POST`
*   **Permission**: IsAuthenticated (需要登录)
*   **Headers**: `Authorization: Bearer <token>`
*   **Request Body**:
    *注意：当前实现仅支持设置标题，分类和标签为只读。*
    ```json
    {
        "title": "新文章标题"
    }
    ```
*   **Response (201 Created)**:
    ```json
    {
        "id": 1,
        "message": "文章创建成功"
    }
    ```

### 2.3 获取文章详情 (Retrieve Article)
*   **URL**: `/articles/<int:pk>/`
*   **Method**: `GET`
*   **Permission**: AllowAny (公开访问)
*   **Response (200 OK)**:
    ```json
    {
        "id": 1,
        "author": "author_username",
        "category": "category_name",
        "title": "文章标题",
        "content": "文章内容...",
        "status": "published",
        "views": 123,
        "created_at": "2023-01-01T12:00:00Z",
        "updated_at": "2023-01-02T12:00:00Z",
        "tags": [ 
//    ...
     ]
    }
    ```

### 2.4 更新文章 (Update Article)
*   **URL**: `/articles/<int:pk>/update/`
*   **Method**: `PATCH`
*   **Permission**: IsAuthenticated (且必须是作者本人)
*   **Headers**: `Authorization: Bearer <token>`
*   **Request Body** (可更新字段):
    ```json
    {
        "title": "更新后的标题",
        "content": "更新后的内容"
    }
    ```
*   **Response (200 OK)**: 返回更新后的文章详情。

---

## 3. 分类模块 (Categories)

### 3.1 获取分类列表 (List Categories)
*   **URL**: `/category/`
*   **Method**: `GET`
*   **Permission**: AllowAny
*   **Response (200 OK)**:
    ```json
    [
        {
            "id": 1,
            "name": "Python"
        },
        {
            "id": 2,
            "name": "Django"
        }
    ]
    ```
