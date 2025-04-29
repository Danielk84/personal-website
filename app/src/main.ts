import './base.css';

import { createApp, defineAsyncComponent } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from "./router";

const component = [
  "HeaderLayer", 
  "PagesBar",
  "FirstButton",
  "SecondButton",
  "PostBox",
  "AsideLayer",
  "PostOverview",
  "StyledInput",
  "PaginationManager",
  "FooterLayer",
];
const pinia = createPinia();
const app = createApp(App).use(router).use(pinia);

component.forEach(name => 
  app.component(name, defineAsyncComponent( () => import(`./components/${name}.vue`)))
);

app.mount('#app');