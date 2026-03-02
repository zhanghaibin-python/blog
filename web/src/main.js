import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'    // 引入 Element Plus 样式
import App from './App.vue'
import router from './router'


const app = createApp(App)


app.use(createPinia())    // 启用pinia
app.use(router)     // 启用router
app.use(ElementPlus)    // 启用 Element Plus

app.mount('#app')
