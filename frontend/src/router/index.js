import { createRouter, createWebHistory } from 'vue-router'

import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import StaffDashboard from '../views/StaffDashboard.vue'
import TrekkerDashboard from '../views/TrekkerDashboard.vue'

const routes = [
    {
        path:'/' ,
        component:Login
    },
    {
        path:'/register' ,
        component:Register
    },
    {
        path:'/admin' ,
        component:AdminDashboard,
        meta:{role:'ADMIN'}
    },
    {
        path:'/staff' ,
        component:StaffDashboard,
        meta:{role:'STAFF'}
    },
    {
        path:'/trekker' ,
        component:TrekkerDashboard,
        meta:{role:'TREKKER'}
    }

]
const router = createRouter({history:createWebHistory(),routes})
router.beforeEach((to, from, next)=>{
    if (!to.meta.role){next()
        return 
    }
    const token = localStorage.getItem('token')
    const role = localStorage.getItem('role')
    if (!token){
        next('/')
        return
    }
    if(role != to.meta.role){
        next('/')
        return
    }
    next()
})


export default router