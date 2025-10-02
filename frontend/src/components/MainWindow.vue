<template>
    <div class="main-frame">
        <div class="left-frame">
            <MiscBar
            :key="userStore.userData?.id"
            :userName="userStore.userData?.name"
            :email="userStore.userData?.email"
            :bio="userStore.userData?.bio"></MiscBar>
            <Chats></Chats>
        </div>
        <ChatWindow></ChatWindow>
    </div>
</template>

<script setup>
    import { onMounted } from 'vue';
    import Chats from './Chats.vue'
    import ChatWindow from './ChatWindow.vue'
    import MiscBar from './MiscBar.vue'
    import { useUserStore } from '../user-store'

    const userStore = useUserStore();
    onMounted(userStore.loadUserData);
    
</script>

<script>
</script>

<style scoped>
    @import url(../css/fonts.css);
    @import url(../css/colors.css);

    .main-frame {
        display: flex;
        gap: 0.5rem;
        margin: 0 10vw;
    }

    .left-frame {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

</style>
