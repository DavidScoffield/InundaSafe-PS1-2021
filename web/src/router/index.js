import { createRouter, createWebHistory } from 'vue-router'
import Complaint from '../components/Complaint.vue'
import FormNewComplaint from '../components/FormNewComplaint.vue'

const routes = [
    {
        path: '/complaints',
        name: 'Complaints',
        component: Complaint
    },
    {
        path: '/newComplaint',
        name: 'NewComplaint',
        component: FormNewComplaint
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router