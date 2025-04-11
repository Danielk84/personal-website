<script setup lang="ts">
  interface Props {
    address: string
    color?: string
  }
 const { 
  color  = "--color-btn-1",
} = defineProps<Props>();
</script>

<template>
  <RouterLink :to="address">
    <div :style="{
        backgroundColor: `var(${color})`,
      }"
      class="m-4 py-2 px-4 h-fit w-fit rounded-3xl">
      <slot></slot>
    </div>
  </RouterLink>
</template>