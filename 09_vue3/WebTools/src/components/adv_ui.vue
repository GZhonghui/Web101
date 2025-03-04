<script setup>
// 使用<script setup>时，不需要显式地导出任何内容，Vue会自动处理

import { ref } from 'vue';

/* ==========滑动条组件========== */
const sliderValue = ref(50);

/* ==========进度条组件========== */
const progressValue = ref(0);
const maxValue = ref(128);

function work() {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve();
    }, 200);
  })
}

async function increaseProgress() {
  while (progressValue.value < maxValue.value) {
    await work();
    progressValue.value += 1;
  }
}
increaseProgress();

/* ==========开关按钮========== */
const switchValue = ref(false);
</script>

<template>
  <h2>高级 UI 组件</h2>
  
  <!-- 滑动条 -->
  <div class="ui-group">
    <h3>滑动条 (Slider)</h3>
    <input 
      type="range" 
      min="0" 
      max="100" 
      v-model="sliderValue"
    >
    <p>当前值: {{ sliderValue }}</p>
  </div>

  <!-- 进度条 -->
  <div class="ui-group">
    <h3>进度条 (Progress)</h3>
    <progress :value="progressValue" :max="maxValue"></progress>
    <p>当前进度: {{ progressValue < maxValue ? `${progressValue}/${maxValue}` : '已完成' }}</p>
  </div>

  <!-- 开关按钮 暂时还没有做任何样式 所以就是一个普通的checkbox -->
  <div class="ui-group">
    <h3>开关按钮 (Switch)</h3>
    <label>是否开启？</label>
    <input type="checkbox" v-model="switchValue">
    <p>当前状态: {{ switchValue ? '开启' : '关闭' }}</p>
  </div>
</template>

<style scoped>
h2, h3, p, label {
  /* 更换一下组件的字体 */
  font-family: "KaiTi", "STKaiti", "AR PL UKai CN", monospace;
  color: #ff0000;
}
.ui-group {
  outline: 1px solid #000000;
  padding: 10px;
  margin: 10px;
  width: 880px;
}
</style>