import './assets/base.css'

import { createApp, defineAsyncComponent } from 'vue'

import App from './App.vue'
import router from "./router"

const app = createApp(App)
  .component("HeaderLayer", defineAsyncComponent(() => 
    import("./components/HeaderLayer.vue")
  ))
  .component("PagesBar", defineAsyncComponent(() =>
    import("./components/PagesBar.vue")
  ))
  .component("FirstButton", defineAsyncComponent(() =>
    import("./components/FirstButton.vue")
  ))
  .component("SecondButton", defineAsyncComponent(() => 
    import("./components/SecondButton.vue")
  ))
  .component("PostBox", defineAsyncComponent(() =>
    import("./components/PostBox.vue")
  ))
  .component("AsideLayer", defineAsyncComponent(() => 
    import("./components/AsideLayer.vue")
  ))
  .component("PostOverview", defineAsyncComponent(() =>
    import("./components/PostOverview.vue")
  ))
  .component("FooterLayer", defineAsyncComponent(() => 
    import("./components/FooterLayer.vue")
  ))
.use(router)

app.mount('#app');