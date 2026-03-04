<template>
  <div class="home-container">
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="5" animated />
    </div>
    <div v-else-if="articles.length === 0" class="empty-container">
      <el-empty description="暂无文章" />
    </div>
    <div v-else>
      <el-card v-for="article in articles" :key="article.id" class="article-card" shadow="hover">
        <template #header>
          <div class="article-header">
            <router-link :to="{ name: 'article-detail', params: { id: article.id } }" class="article-title">
              {{ article.title }}
            </router-link>
            <el-tag v-if="article.category" size="small" type="info">
                {{ typeof article.category === 'object' ? article.category.name : article.category }}
            </el-tag>
          </div>
        </template>
        <div class="article-summary">
          {{ truncate(article.content, 150) }}
        </div>
        <div class="article-meta">
          <span class="meta-item">
            <el-icon><Calendar /></el-icon>
            {{ formatDate(article.created_at) }}
          </span>
          <span class="meta-item">
            <el-icon><View /></el-icon>
            {{ article.views }} 阅读
          </span>
        </div>
      </el-card>
      
      <div class="pagination-container">
          <el-pagination
            background
            layout="prev, pager, next"
            :total="total"
            :page-size="pageSize"
            v-model:current-page="currentPage"
            @current-change="fetchArticles"
          />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getArticles } from '@/api/article'
import { Calendar, View } from '@element-plus/icons-vue'

const articles = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10) // 假设后端默认分页大小为 10
const loading = ref(false)

const fetchArticles = async (page = 1) => {
  loading.value = true
  try {
    const res = await getArticles({ page })
    // res: { count, next, previous, results }
    articles.value = res.results
    total.value = res.count
    currentPage.value = page
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const truncate = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString()
}

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.home-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px 0;
}

.article-card {
  margin-bottom: 20px;
}

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.article-title {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
  text-decoration: none;
}

.article-title:hover {
  color: #409EFF;
}

.article-summary {
  color: #606266;
  line-height: 1.6;
  margin-bottom: 15px;
}

.article-meta {
  display: flex;
  gap: 20px;
  color: #909399;
  font-size: 14px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}
</style>
