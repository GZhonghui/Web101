import { createApp } from 'vue'
import App from './App.vue'
import { router } from './views/router'

// 导入 router 到 app 中
createApp(App).use(router).mount('#app')
