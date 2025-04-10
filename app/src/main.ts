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
  .component("AsideLayer", defineAsyncComponent(() => 
    import("./components/AsideLayer.vue")
  ))
  .component("FooterLayer", defineAsyncComponent(() => 
    import("./components/FooterLayer.vue")
  ))
  .component("PostOverview", defineAsyncComponent(() =>
    import("./components/PostOverview.vue")
  ))
  .use(router)

app.mount('#app');