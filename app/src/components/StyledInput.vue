<script setup lang="ts">
const { type = "text" } = defineProps<{ type?: string }>();
const emit = defineEmits(["setInput"]);

const handleInput = (event: Event) => {
  emit("setInput", (event.target as HTMLInputElement).value);
}
</script>

<template>
  <input :type="type" @input="handleInput"
    class="bg-b-1 p-2 text-f-1 rounded-xl outline-none
    border-btn-1 hover:border-2 base-btn-transition
    min-[430px]:w-70 min-sm:w-80" />
</template>