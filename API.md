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
      "code": 200,
      "msg": "success",
      "data": {
          "username": "your_username"
      }
}
    ```
*   **Response (400 Bad Request)**:
    ```json
    {
      "code": 400,
      "msg": "error",
      "data": {
        "username": [
            "已存在一位使用该名字的用户。"
        ]
    }
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
        "code": 200,
        "msg": "success",
        "data": {
            "message": "登录成功! ",
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbG...",
            "access": "eyJ0eXAiOiJKV1QiLCJhbG..."
        }
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
        "code": 200,
        "msg": "success",
        "data": {
            "username": "testuser"
        }
    }
    ```
*   **Response (401 Unauthorized)**:
    ```json
    {
       "code": 401,
       "msg": "error",
       "data": {
          "message": "用户未登录! "
        }
    }
    ```

### 1.4 退出登录 (Logout)
*   **URL**: `/auth/logout/`
*   **Method**: `POST`
*   **Permission**: AllowAny
*   **Request Body**:
    ```json
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbG..."
    }
    ```
*   **Response (200 OK)**:
    ```json
    {
        "code": 200,
        "msg": "success",
        "data": {
            "detail": "Successfully logged out."
        }
    }
    ```

---

## 2. 文章模块 (Articles)

### 2.1 获取文章列表 (List Articles)
*   **URL**: `/articles/`
*   **Method**: `GET`
*   **Permission**: IsAuthenticatedOrReadOnly (get请求可直接放行) 
*   **Headers**: `Authorization: Bearer <token>`
*   **Query Parameters**: 无
*   **Response (200 OK)**:
    ```json
    {
        "code": 200,
        "msg": "success",
        "data": {
            "count": 0,
            "next": null,
            "previous": null,
            "results": []
        }
    }
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
        "title": "Django 入门教程",
        "content": "本文介绍 Django 的基本安装和第一个项目创建方法。",
        "category": 1,   
        "tags": [],
         "status": "draft"
    }
    ```
*   **Response (201 Created)**:
    ```json
    {
        "code": 200,
        "msg": "success",
        "data": {
            "title": "Django 入门教程",
            "category": 1,
            "tags": [],
            "content": "本文介绍 Django 的基本安装和第一个项目创建方法。",
            "status": "draft"
        }
    }
    ```

### 2.3 获取文章详情 (Retrieve Article)
*   **URL**: `/articles/<int:pk>/`
*   **Method**: `GET`
*   **Permission**: IsAuthenticatedOrReadOnly (未登录时只能进行get操作)
*   **Response (200 OK)**:
    ```json
    {
        "code": 200,
        "msg": "success",
        "data": {
            "id": 1,
            "title": "Django 入门教程",
            "category": {
                "id": 1,
                "name": "Django"
            },
         "tags": [],
         "views": 0,
         "created_at": "2026-03-01T09:41:45.897463+08:00"
        }
    }
    ```

### 2.4 更新文章 (Update Article)
*   **URL**: `/articles/<int:pk>/update/`
*   **Method**: `PATCH`/ `PUT`
*   **Permission**: IsAuthorOrReadOnly (登录且必须是作者本人)
*   **Headers**: `Authorization: Bearer <token>`
*   **Request Body** (可更新字段):
    ```json
    {
        "title": "Django基础教程"
     }
    ```
*   **Response (200 OK)**: 
    ```json
    {
        "code": 200,
        "msg": "success",
        "data": {
            "title": "Django基础教程",
            "category": 1,
            "tags": [],
            "content": "本文介绍 Django 的基本安装和第一个项目创建方法。",
            "status": "draft"
        }
    }
    ```

---

## 3. 分类模块 (Categories)

### 3.1 获取分类列表 (List Categories)
*   **URL**: `/category/`
*   **Method**: `GET`
*   **Permission**: AllowAny
*   **Response (200 OK)**:
    ```json
    {
      "code": 200,
      "msg": "success",
      "data": [
          {
              "id": 1,
              "name": "Django"
          }
      ]
    }
    ```
