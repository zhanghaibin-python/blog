<template>
  <div class="home-container">
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索文章标题..."
        class="input-with-select"
        @keyup.enter="handleSearch"
        clearable
        @clear="handleSearch"
      >
        <template #prepend>
            <el-select v-model="selectedCategory" placeholder="全部分类" style="width: 110px" clearable @change="handleSearch">
                <el-option label="全部分类" value="" />
                <el-option v-for="item in categories" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
        </template>
        <template #append>
          <el-button :icon="Search" @click="handleSearch" />
        </template>
      </el-input>
    </div>

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
import { getCategories } from '@/api/category'
import { Calendar, View, Search } from '@element-plus/icons-vue'

const articles = ref([])
const categories = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const loading = ref(false)
const searchKeyword = ref('')
const selectedCategory = ref('')

const handleSearch = () => {
  currentPage.value = 1
  fetchArticles(1)
}

const fetchCategoryList = async () => {
  try {
    const res = await getCategories()
    categories.value = res
  } catch (error) {
    console.error(error)
  }
}

const fetchArticles = async (page = 1) => {
  loading.value = true
  try {
    const params = { page }
    if (searchKeyword.value && searchKeyword.value.trim()) {
      params.title = searchKeyword.value.trim()
    }
    if (selectedCategory.value) {
        params.category = selectedCategory.value
    }
    const res = await getArticles(params)
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
  fetchCategoryList()
  fetchArticles()
})
</script>

<style scoped>
.home-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px 0;
}

.search-bar {
  margin-bottom: 20px;
  max-width: 600px;
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
