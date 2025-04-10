<template>
  <header class="bar">
    <div class="icon"></div>
    <div class="pages">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/about">About Us</RouterLink>
      <RouterLink to="/posts">Posts</RouterLink>
    </div>
  </header>
</template>

<style scoped>
  @reference "../assets/base.css";

  .bar {
    @apply bg-gradient-to-br from-[var(--c-f-1)] to-[var(--c-d-4)]
      backdrop-blur-sm brightness-110 z-20 fixed
      flex justify-evenly items-center
      w-[100%] h-[50px]
      rounded-b-2xl
      border-[var(--c-a-4)] border-b-4
      shadow-[0_0_20px_var(--c-a-4)];
  }
  .pages {
    @apply flex gap-[2rem];
  }
</style>