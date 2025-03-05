<script setup>
</script>

<template>
  <h1>Hello World</h1>
  <div id="top-nav">
    <!-- 跳转路由 -->
    <RouterLink to="/" class="link">Home</RouterLink>
    <RouterLink to="/p1" class="link">Page 1</RouterLink>
    <RouterLink to="/p2" class="link">Page 2</RouterLink>
  </div>
  <hr>
  <!--
    显示路由
    这里的逻辑是，根据当前 URL 匹配路由
    然后渲染【当前组件的子组件】的内容
    比如：当前组件是根组件，那么这里可能渲染 / /p1 /p2 这种一级路由
    然后【当前组件的子组件】的<RouterView />负责渲染下一级路由
  -->
  <RouterView />
</template>

<style scoped>
#top-nav .link {
  margin-right: 10px;
}
</style>
