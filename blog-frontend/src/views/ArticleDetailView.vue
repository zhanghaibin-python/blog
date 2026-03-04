<template>
  <div class="article-detail-container">
    <el-skeleton v-if="loading" :rows="10" animated />
    <div v-else-if="article">
      <div class="article-header">
        <h1>{{ article.title }}</h1>
        <div class="article-meta">
           <span class="meta-item">
             <el-icon><Calendar /></el-icon>
             {{ formatDate(article.created_at) }}
           </span>
           <span class="meta-item">
             <el-icon><View /></el-icon>
             {{ article.views }} 阅读
           </span>
           <span class="meta-item" v-if="article.category">
             <el-tag size="small">{{ article.category.name }}</el-tag>
           </span>
        </div>
      </div>
      
      <el-divider />
      
      <div class="article-content">
        <!-- 如果内容是 markdown，可以使用 markdown-it 等库渲染，这里直接显示文本 -->
        <div style="white-space: pre-wrap;">{{ article.content }}</div>
      </div>
      
      <div class="article-actions" v-if="authStore.isAuthenticated">
          <el-button type="primary" :icon="Edit" @click="$router.push(`/articles/${article.id}/edit`)">编辑文章</el-button>
      </div>
    </div>
    <el-empty v-else description="文章不存在" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getArticle } from '@/api/article'
import { useAuthStore } from '@/stores/auth'
import { Calendar, View, Edit } from '@element-plus/icons-vue'

const route = useRoute()
const authStore = useAuthStore()

const article = ref(null)
const loading = ref(false)

const fetchArticle = async () => {
  loading.value = true
  try {
    const id = route.params.id
    const res = await getArticle(id)
    article.value = res
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString()
}

onMounted(() => {
  fetchArticle()
})
</script>

<style scoped>
.article-detail-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: #fff;
  min-height: 80vh;
}

.article-header h1 {
  font-size: 32px;
  margin-bottom: 20px;
  color: #303133;
}

.article-meta {
  display: flex;
  gap: 20px;
  color: #909399;
  font-size: 14px;
  align-items: center;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.article-content {
  line-height: 1.8;
  font-size: 16px;
  color: #303133;
  margin-bottom: 40px;
}

.article-actions {
    margin-top: 40px;
    border-top: 1px solid #ebeef5;
    padding-top: 20px;
    text-align: right;
}
</style>
