<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import type { Post } from '../interfaces/PostSerializers.ts';
import useScreenWidth from '../composables/useScreenWidth.ts';
import { getStaticData } from '../composables/fetchData.ts';

const router = useRouter();
const route = useRoute();
const { screenWidth } = useScreenWidth();
const content = ref<Post>()

onMounted(async () => {
  try {
    const { json, statusCode, msg } = await getStaticData<Post>(
      `/post/${route.params.slug}/`,
    );
    if (statusCode !== 200) throw msg;

    content.value = json;
  } catch (error) {
    router.push(`/404/${error}/`);
  }
});
</script>

<template>
  <main class="min-h-[80vh] grid min-lg:grid-cols-3">
    <div v-if="screenWidth > 1024" class="min-lg:col-start-1 min-lg:col-end-2">
      <AsideLayer />
    </div>
    <div v-if="content">
      <div class="min-lg:col-start-2 min-lg:col-end-4
      min-h-lvh m-8 min-lg:p-8 max-lg:p-4">
        <h1>{{ content["title"] }}</h1>
        <p>{{ content.user }}</p>
        <time>{{ content.pub_date }}</time>
        <time>{{ content.last_modify }}</time>
        <article>
          {{ content.body }}
        </article>
      </div>
    </div>
  </main>
</template>