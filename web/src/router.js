import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './views/Homepage.vue';
import ChatPage from "@/views/ChatPage.vue";

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomePage
    },
    {
        path: '/chat',
        name: 'ChatPage',
        component: ChatPage
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
