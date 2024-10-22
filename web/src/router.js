import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './views/Homepage.vue';
import ChatPage from './views/ChatPage.vue';
import Test from "@/views/test.vue";

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomePage
    },
    {
        path: '/chat',
        name: 'Chat',
        component: ChatPage
    },
    {
        path: '/test',
        name: 'Test',
        component: Test
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
