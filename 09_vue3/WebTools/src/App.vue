<script setup>
// setup 表示 Vue 会自动帮我们处理一些逻辑，让我们可以用这些语法

import { ref, reactive } from 'vue';
// 导入名字可以和文件名不一样，但是推荐一样
// 这是手动导入的方式，也可以将组件注册到全局（根组件，APP）
import adv_ui_component from './components/adv_ui.vue';
import content_component from './components/content.vue';

/* ========== 计数器 ========== */
// ref 表示响应式变量，value 表示变量的值
const count = ref(0);

function increase() {
  count.value++;
}

/* ========== 展示海报 ========== */
// 普通变量
let poster_index = 0;
const poster_paths = [
  '/public/poster/1.png',
  '/public/poster/2.png',
  '/public/poster/3.png'
]

// 响应式变量
const poster_path = ref(poster_paths[poster_index]);
function next_poster() {
  poster_index = (poster_index + 1) % poster_paths.length;
  poster_path.value = poster_paths[poster_index];
}

/* ========== 用户信息 ========== */
// reactive 表示响应式对象，可以监听对象属性的变化
const user_info = reactive({
  name: '无名氏',
  age: 18
})
</script>

<template>
  <h1>HTML & Vue <u>模板工程</u></h1>
  <hr>
  <div>
    <!-- 两种事件的触发方式：绑定函数或者直接书写逻辑 -->
    <button @click="increase">增加</button>
    <button @click="count--">减少</button>
    <p>计数：{{ count }}</p>
  </div>
  <div>
    <!-- 使用 public 目录下的图片，这是绝对路径 -->
    <!-- block 表示块级元素，会独占一行 -->
    <!-- :src 表示 src 属性绑定 poster_path 的值 -->
    <img :src="poster_path" style="display: block; margin-bottom: 10px;">
    <button @click="next_poster">Next</button>
    <label>海报：{{ poster_path }}</label>
  </div>
  <div>
    <!-- v-model 表示双向绑定，会自动将输入框的值绑定到 user_info 对象的 name 属性 -->
    <label>姓名：</label>
    <input type="text" v-model="user_info.name">
    <label>年龄：</label>
    <input type="number" v-model="user_info.age">
    <!-- v-if 表示条件渲染，当 user_info.name.length > 0 时，显示该元素 -->
    <p v-if="user_info.name.length > 0">你好，{{ user_info.age }}岁的<strong>「{{ user_info.name }}」</strong>同学！</p>
  </div>
  <!-- 使用组件，注意自定义组件的写法 -->
  <adv_ui_component />
  <content_component />
</template>

<style scoped>
/* scoped 表示这个样式只作用于当前组件 */
h1, p, button, label, input {
  font-family: "SimSun", "STSong", serif;
}
button {
  font-size: 16px;
  padding: 5px 10px;
  margin-right: 10px;
  margin-bottom: 10px;
}
input[type="text"], input[type="number"] {
  font-size: 16px;
  padding: 5px 10px;
  margin-right: 10px;
}
</style>