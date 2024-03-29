import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'leaflet/dist/leaflet.css'
import './assets/global.css'
// import 'jquery'
import '@popperjs/core'
import 'bootstrap/dist/js/bootstrap.bundle'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import './registerServiceWorker'

createApp(App).use(router).mount('#app')
