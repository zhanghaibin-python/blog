<template>
  <div>
    <h1>欢迎回来, {{ userStore.user.username }}</h1>
    <el-button type="danger" @click="handleLogout">退出登录</el-button>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

onMounted(() => {
  userStore.getUserInfoAction()
})

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
</script>