import { createRouter, createWebHistory } from 'vue-router'

import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import StaffDashboard from '../views/StaffDashboard.vue'
import TrekkerDashboard from '../views/TrekkerDashboard.vue'
import ManageTreks from '../views/ManageTreks.vue'
import ManageStaff from '../views/ManageStaff.vue'
import ManageUsers from '../views/ManageUsers.vue'
import ManageBookings from '../views/ManageBookings.vue'
import Participants from "../views/Participants.vue"

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
        path:'/admin/treks' ,
        component:ManageTreks,
        meta:{role:'ADMIN'}
    },
    {
        path:'/admin/staff' ,
        component:ManageStaff,
        meta:{role:'ADMIN'}
    },
    {
        path:'/admin/users' ,
        component:ManageUsers,
        meta:{role:'ADMIN'}
    },
    {
        path:'/admin/bookings' ,
        component:ManageBookings,
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
    },
    {
        path: "/staff/participants/:id",
        component: Participants,
        meta:{role:'STAFF'}
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