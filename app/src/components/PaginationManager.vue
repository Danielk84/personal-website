<template>
  <div class="flex justify-center items-center gap-8 py-4">
    <div class="base-btn btn-style-1">
      <img src="../assets/previous-pg.svg" alt="Previous-pg" class="base-icon" />
    </div>
    <div class="base-btn btn-style-2">
      2
    </div>
    <div class="base-btn btn-style-1">
      <img src="../assets/next-pg.svg" alt="Next-pg"  class="base-icon" />
    </div>
  </div>
</template>

<style scoped>
  @reference "../base.css";

  .base-btn {
    @apply size-12 rounded-full flex justify-center items-center font-bold;
  }
  .btn-style-1 {
    @apply bg-b-1 text-f-1 hover:scale-105 hover:border-2 border-btn-1
      inset-shadow-sm hover:inset-shadow-btn-1/50;
  }
  .btn-style-2 {
    @apply bg-red-600 text-f-2;
  }
  .base-icon {
    @apply size-6 flex justify-center items-center hover:drop-shadow-xl/25;
  }

</style>