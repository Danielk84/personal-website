import './assets/base.css'

import { createApp, defineAsyncComponent } from 'vue'

import App from './App.vue'
import router from "./router"

const component = [
  "HeaderLayer", 
  "PagesBar",
  "FirstButton",
  "SecondButton",
  "PostBox",
  "AsideLayer",
  "PostOverview",
  "FooterLayer",
]

const app = createApp(App).use(router);

component.forEach(name => 
  app.component(name, defineAsyncComponent( () => import(`./components/${name}.vue`)))
);

app.mount('#app');