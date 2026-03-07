<template>
  <div class="article-form-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>编辑文章</h2>
        </div>
      </template>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入文章标题" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="form.category" placeholder="请选择分类" style="width: 100%;">
            <el-option v-for="item in categories" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <MdEditor v-model="form.content" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit('published')" :loading="submitting">发布</el-button>
          <el-button type="info" @click="handleSubmit('draft')" :loading="submitting">存为草稿</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getArticle, updateArticle } from '@/api/article'
import { getCategories } from '@/api/category'
import { ElMessage } from 'element-plus'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'

const router = useRouter()
const route = useRoute()
const formRef = ref(null)
const submitting = ref(false)
const categories = ref([])

const form = reactive({
  title: '',
  content: '',
  category: '',
  status: 'published'
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }]
}

const fetchCategories = async () => {
  try {
    const res = await getCategories()
    categories.value = res
  } catch (error) {
    console.error(error)
  }
}

const fetchArticle = async () => {
  try {
    const id = route.params.id
    const res = await getArticle(id)
    form.title = res.title
    form.content = res.content
    // 后端返回的 category 是对象 {id, name}
    form.category = res.category ? res.category.id : ''
    form.status = res.status || 'published'
  } catch (error) {
    console.error(error)
    ElMessage.error('获取文章失败')
    router.push('/')
  }
}

const handleSubmit = async (status) => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        const id = route.params.id
        form.status = status // 确保更新状态
        await updateArticle(id, form)
        ElMessage.success(status === 'published' ? '发布成功' : '已存为草稿')
        router.push(status === 'published' ? `/articles/${id}` : '/drafts')
      } catch (error) {
        console.error(error)
      } finally {
        submitting.value = false
      }
    }
  })
}

onMounted(async () => {
  await fetchCategories()
  await fetchArticle()
})
</script>

<style scoped>
.article-form-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
</style>
