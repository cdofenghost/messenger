<template>
    <div class="main-frame">
        <Chat></Chat>
        <ChatWindow></ChatWindow>
    </div>
</template>

<script setup>
    import Chat from './Chats.vue'
    import ChatWindow from './ChatWindow.vue'
</script>

<style scoped>
    @import url(../css/fonts.css);
    @import url(../css/colors.css);

    .main-frame {
        display: flex;
        gap: 0.5rem;
        margin: 0 10vw;
    }
</style>
