import './base.css';

import { createApp, defineAsyncComponent, watch } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from "./router";

const component = [
  "LoadingScreen",
  "HeaderLayer", 
  "PagesBar",
  "FirstButton",
  "SecondButton",
  "PostBox",
  "AsideLayer",
  "PostOverview",
  "StyledInput",
  "PaginationManager",
  "PostOverviewMng",
  "FooterLayer",
];

const pinia = createPinia();

watch(pinia.state, (state) => {
  localStorage.setItem("userAuth", JSON.stringify(state.userAuth));
}, { deep: true });

const app = createApp(App).use(router).use(pinia);

component.forEach(name => 
  app.component(name, defineAsyncComponent( () => import(`./components/${name}.vue`)))
);

app.mount('#app');