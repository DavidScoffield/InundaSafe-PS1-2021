import { createRouter, createWebHistory } from 'vue-router'
import Complaint from '../components/Complaint.vue'

const routes = [
    {
        path: '/complaints',
        name: 'Complaints',
        component: Complaint
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router