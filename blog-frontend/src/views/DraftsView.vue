<template>
  <div class="drafts-container">
    <h2>我的草稿箱</h2>
    
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="5" animated />
    </div>
    <div v-else-if="articles.length === 0" class="empty-container">
      <el-empty description="暂无草稿" />
    </div>
    <div v-else>
      <el-card v-for="article in articles" :key="article.id" class="article-card" shadow="hover">
        <template #header>
          <div class="article-header">
            <span class="article-title">{{ article.title }}</span>
            <div class="article-actions">
              <el-button type="primary" size="small" @click="handleEdit(article.id)">编辑</el-button>
              <el-button type="success" size="small" @click="handlePublish(article)">发布</el-button>
              <el-popconfirm title="确定删除这篇草稿吗？" @confirm="handleDelete(article.id)">
                <template #reference>
                  <el-button type="danger" size="small">删除</el-button>
                </template>
              </el-popconfirm>
            </div>
          </div>
        </template>
        <div class="article-summary">
          {{ truncate(article.content, 100) }}
        </div>
        <div class="article-meta">
          <span class="meta-item">
            <el-icon><Calendar /></el-icon>
            {{ formatDate(article.created_at) }}
          </span>
          <el-tag size="small" type="info">草稿</el-tag>
        </div>
      </el-card>
      
      <div class="pagination-container">
          <el-pagination
            background
            layout="prev, pager, next"
            :total="total"
            :page-size="pageSize"
            v-model:current-page="currentPage"
            @current-change="fetchDrafts"
          />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getArticles, updateArticle, deleteArticle } from '@/api/article'
import { Calendar } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const articles = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const loading = ref(false)

const fetchDrafts = async (page = 1) => {
  loading.value = true
  try {
    // 注意：这里依赖后端支持 status=draft 参数
    const params = { page, status: 'draft' }
    const res = await getArticles(params)
    articles.value = res.results
    total.value = res.count
    currentPage.value = page
  } catch (error) {
    console.error(error)
    ElMessage.error('获取草稿列表失败')
  } finally {
    loading.value = false
  }
}

const handleEdit = (id) => {
  router.push(`/articles/${id}/edit`)
}

const handlePublish = async (article) => {
  try {
    await updateArticle(article.id, { status: 'published' })
    ElMessage.success('发布成功')
    fetchDrafts(currentPage.value)
  } catch (error) {
    console.error(error)
    ElMessage.error('发布失败')
  }
}

const handleDelete = async (id) => {
  try {
    await deleteArticle(id)
    ElMessage.success('删除成功')
    fetchDrafts(currentPage.value)
  } catch (error) {
    console.error(error)
    ElMessage.error('删除失败')
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
  fetchDrafts()
})
</script>

<style scoped>
.drafts-container {
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
  align-items: center;
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
