import { createApp } from 'vue'
import App from './components/App.vue'
import router from './router'
import { createPinia } from 'pinia'

import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faUserSecret, faHome, faUser, faPlus, faMessage, faLockOpen, faLock, faXmark, faArrowRight } from '@fortawesome/free-solid-svg-icons';

library.add(faUserSecret, faHome, faUser, faPlus, faMessage, faLockOpen, faLock, faArrowRight, faXmark );

const pinia = createPinia()
const app = createApp(App)

app.use(router).mount('#app')
app.use(pinia)

app.component('font-awesome-icon', FontAwesomeIcon);
