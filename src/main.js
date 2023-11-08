import './assets/main.css'

import { createApp } from 'vue'
import { IonIcon } from '@ionic/vue';
import App from './App.vue'
import router from './router'
import store from './store/index'

const app = createApp(App)

app.component('IonIcon', IonIcon);

app.use(router);

app.use(store);

app.mount('#app');
