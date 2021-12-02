import { createRouter, createWebHistory } from 'vue-router'
import Complaint from '../components/Complaint.vue'
import MeetingPointsEvacuationRoutes from '../components/MeetingPointsEvacuationRoutes.vue'
import FloodZones from '../components/FloodZones.vue'

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
  {
    path: '/zonas-inundables',
    name: 'FloodZones',
    component: FloodZones,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
