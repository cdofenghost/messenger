<template>
    <div class="main-frame">
        <div class="left-frame">
            <MiscBar></MiscBar>
            <Chats></Chats>
        </div>
        <ChatWindow></ChatWindow>
    </div>
</template>

<script setup>
    import Chats from './Chats.vue'
    import ChatWindow from './ChatWindow.vue'
    import MiscBar from './MiscBar.vue'
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
