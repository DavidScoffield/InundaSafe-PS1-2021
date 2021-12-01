import { createRouter, createWebHistory } from 'vue-router'
import Complaint from '../components/Complaint.vue'
import MeetingPointsEvacuationRoutes from '../components/MeetingPointsEvacuationRoutes.vue'

const routes = [
  {
    path: '/complaints',
    name: 'Complaints',
    component: Complaint,
  },
  {
    path: '/puntos-recorridos',
    name: 'MeetingPointsEvacuationRoutes',
    component: MeetingPointsEvacuationRoutes,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
