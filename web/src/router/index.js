import { createRouter, createWebHistory } from 'vue-router'
import MeetingPointsEvacuationRoutes from '../components/MeetingPointsEvacuationRoutes.vue'

const routes = [
    {
        path: '/puntos-recorridos',
        name: 'MeetingPointsEvacuationRoutes',
        component: MeetingPointsEvacuationRoutes
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router