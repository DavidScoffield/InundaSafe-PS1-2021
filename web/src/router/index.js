import { createRouter, createWebHistory } from 'vue-router'
import Complaint from '../components/Complaint.vue'
import FormNewComplaint from '../components/FormNewComplaint.vue'
import MeetingPointsEvacuationRoutes from '../components/MeetingPointsEvacuationRoutes.vue'
import FloodZonesAll from '../components/FloodZonesAll.vue'
import FloodZone from '../components/FloodZone.vue'
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
    path: '/newComplaint',
    name: 'NewComplaint',
    component: FormNewComplaint,
  },
  {
    path: '/zonas-inundables',
    name: 'FloodZonesAll',
    component: FloodZonesAll,
  },
  {
    path: '/zonas-inundables/:id(\\d+)',
    name: 'FloodZone',
    component: FloodZone,
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
