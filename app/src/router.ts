import { createRouter, createWebHashHistory } from 'vue-router';

export default createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: "/", component: () => import("./pages/Home.vue") },
    { path: "/about", component: () => import("./pages/About.vue") },
    { path: "/posts", component: () => import("./pages/Posts.vue") },
    { path: "/post", component: () => import("./pages/Post.vue") },
  ],
});
