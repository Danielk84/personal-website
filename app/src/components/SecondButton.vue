<script setup lang="ts">
import type BaseBtnData from '../types/BaseBtnData';

interface BtnData extends BaseBtnData {
  bColor: string
}

const {
  color = "--color-f-2",
  bColor = "--color-btn-1",
} = defineProps<BtnData>();
</script>

<template>
  <RouterLink :to="address">
    <div :style="{
        backgroundColor: `var(${color})`,
        borderColor: `var(${bColor})`,
      }"
      class="m-4 py-2 px-4 h-fit w-fit rounded-3xl">
      <slot></slot>
    </div>
  </RouterLink>
</template>