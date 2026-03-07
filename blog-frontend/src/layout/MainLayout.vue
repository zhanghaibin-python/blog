<template>
  <el-container class="layout-container">
    <el-header class="app-header">
      <div class="header-inner">
        <div class="logo">
            <h2>Blog System</h2>
        </div>
        <div class="user-info">
           <template v-if="authStore.isAuthenticated">
               <el-dropdown @command="handleCommand">
                    <span class="el-dropdown-link">
                        {{ authStore.user?.username || 'User' }}
                        <el-icon class="el-icon--right"><arrow-down /></el-icon>
                    </span>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
               </el-dropdown>
           </template>
           <template v-else>
               <el-button link @click="$router.push('/login')">登录</el-button>
               <el-button type="primary" size="small" @click="$router.push('/register')">注册</el-button>
           </template>
        </div>
      </div>
    </el-header>
    <el-container>
      <el-aside width="200px" class="app-aside">
        <el-menu :default-active="$route.path" router class="el-menu-vertical-demo">
            <el-menu-item index="/">
                <el-icon><HomeFilled /></el-icon>
                <span>首页</span>
            </el-menu-item>
            <el-menu-item index="/articles/create">
                <el-icon><EditPen /></el-icon>
                <span>写文章</span>
            </el-menu-item>
            <el-menu-item index="/drafts">
                <el-icon><Document /></el-icon>
                <span>草稿箱</span>
            </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main class="app-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { ArrowDown, HomeFilled, EditPen, Document } from '@element-plus/icons-vue'

const authStore = useAuthStore()
const router = useRouter()

const handleCommand = (command) => {
    if (command === 'logout') {
        authStore.logout().then(() => {
            router.push('/login')
        })
    }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}
.app-header {
    border-bottom: 1px solid #dcdfe6;
    padding: 0 20px;
}
.header-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}
.app-aside {
    border-right: 1px solid #dcdfe6;
}
.el-dropdown-link {
  cursor: pointer;
  display: flex;
  align-items: center;
}
</style>
