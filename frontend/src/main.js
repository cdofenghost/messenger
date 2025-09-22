import { createApp } from 'vue'
import App from './components/App.vue'
import router from './router'
import { createPinia } from 'pinia'

const pinia = createPinia()
const app = createApp(App)

app.use(router).mount('#app')
app.use(pinia)
