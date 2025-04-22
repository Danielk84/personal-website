<template>
  <div class="content-box h-[50vh]">
    <h1>hello</h1>
  </div>
    <div class="ref-box ref-box-color overflow-auto">
      <PostBox />
      <PostBox />
      <PostBox />
      <PostBox />
      <PostBox />
    </div>
  <div class="content-box h-[600px]">
    <h2>this content box</h2>
  </div>
  <div class="ref-box ref-box-color">

  </div>
</template>

<style scoped>
  @reference "../assets/base.css";

  .content-box {
    @apply flex justify-center items-center;
  }
  .ref-box {
    @apply drop-shadow-xl/25 h-fit p-4
      flex justify-evenly items-center flex-wrap;
  }
</style>