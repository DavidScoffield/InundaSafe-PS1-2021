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
    history: createWebHistory(),
    routes,
});

export default router