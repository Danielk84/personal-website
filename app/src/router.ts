import { createRouter, createWebHashHistory } from 'vue-router';

export default createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: "/", component: () => import("./pages/Home.vue") },
    { path: "/about", component: () => import("./pages/About.vue") },
    { path: "/posts", component: () => import("./pages/Posts.vue") },
    { path: "/post", component: () => import("./pages/Post.vue") },
    { path: "/login-panel", component: () => import("./pages/LoginPanel.vue") },
    { path: "/401", component: () => import("./pages/Unauthorized.vue")},
    { path: "/403", component: () => import("./pages/Forbidden.vue") },
    { path: "/:pathMatch(.*)", component: () => import("./pages/NotFound.vue") },
  ],
});
