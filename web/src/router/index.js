import { createRouter, createWebHistory } from 'vue-router'
import Complaint from '../components/Complaint.vue'
import MeetingPointsEvacuationRoutes from '../components/MeetingPointsEvacuationRoutes.vue'
import FloodZones from '../components/FloodZones.vue'
import Home from '../components/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
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
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
