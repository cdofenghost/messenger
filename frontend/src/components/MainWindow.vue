<template>
    <div class="main-frame">
        <Chats></Chats>
        <ChatWindow></ChatWindow>
    </div>
</template>

<script setup>
    import Chats from './Chats.vue'
    import ChatWindow from './ChatWindow.vue'
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

</style>
