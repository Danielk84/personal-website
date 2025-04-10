<template>
  <div class="flex flex-col">
    <HeaderLayer />
    <div class="view">
      <RouterView />
    </div>
    <FooterLayer />
  </div>
</template>

<style scoped>
  .view {
    @apply z-0 my-[60px]
  }
</style>