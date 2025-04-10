<template>
  <div class="content-box">
    <h1>hello</h1>
  </div>
    <div class="ref-box overflow-auto">
      <PostBox />
      <PostBox />
      <PostBox />
      <PostBox />
      <PostBox />
    </div>
  <div class="content-box">
    <h2>this content box</h2>
  </div>
  <div class="ref-box">

  </div>
</template>

<style scoped>
  @reference "../assets/base.css";

  .content-box {
    @apply flex justify-center items-center h-[600px];
  }
  .ref-box {
    @apply h-[600px] bg-neutral-700 shadow-[0_0_15px_var(--c-d-4)]
      flex justify-evenly items-center;
  }
</style>