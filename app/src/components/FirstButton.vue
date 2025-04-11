<script setup lang="ts">
import type BaseBtnData from '../types/BaseBtnData';

const { 
  color  = "--color-btn-1",
} = defineProps<BaseBtnData>();
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