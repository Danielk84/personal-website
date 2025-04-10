<template>
  <header class="flex justify-center">
    <div class="bg-b-1 drop-shadow-xl/25 w-97/100 h-16 m-2 backdrop-blur-sm rounded-2xl
      flex justify-evenly items-center fixed z-10">
      <div class="icon"></div>
    <div class="pages">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/about">About Us</RouterLink>
      <RouterLink to="/posts">Posts</RouterLink>
    </div>
    </div>
  </header>
</template>

<style scoped>
  @reference "../assets/base.css";
  .pages {
    @apply flex gap-[2rem];
  }
</style>