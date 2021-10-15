import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Elb from '../components/Elb.vue'
import Ec2 from '../components/Ec2.vue'
import ElbDetail from '../components/ElbDetail.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    children: [
      {
        path: "elb",
        name: 'Elv',
        component: Elb
      },
      {
        path:"elb/:name",
        name: 'ElbDetail',
        component: ElbDetail,
        props: true
      },
      {
        path: "ec2",
        component: Ec2
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
