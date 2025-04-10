import './assets/base.css'

import { createApp, defineAsyncComponent } from 'vue'

import App from './App.vue'
import router from "./router"

const app = createApp(App)
  .component("HeaderLayer", defineAsyncComponent(() => 
    import("./components/HeaderLayer.vue")
  ))
  .component("PostBox", defineAsyncComponent(() =>
    import("./components/PostBox.vue")
  ))
  .use(router)

app.mount('#app');