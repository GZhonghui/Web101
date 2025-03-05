import { createWebHistory, createRouter } from 'vue-router'

import home_page from './home_page.vue'
import sub_page_1 from './sub_page_1.vue'
import sub_page_1_t1 from './views_p1/sub_page_1_t1.vue'
import sub_page_1_t2 from './views_p1/sub_page_1_t2.vue'
import sub_page_2 from './sub_page_2.vue'

// 配置路由
const routes = [
  { path: '/', component: home_page },
  { 
    path: '/p1',
    component: sub_page_1, // 一个路径对应一个组件
    // 配置子路由
    children: [
      { path: 't1', component: sub_page_1_t1 },
      { path: 't2', component: sub_page_1_t2 }
    ]
  },
  { path: '/p2', component: sub_page_2 },
]

export const router = createRouter({
  history: createWebHistory(), // 使用这种模式 URL 才会变化
  routes,
})