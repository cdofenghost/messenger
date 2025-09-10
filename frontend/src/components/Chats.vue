<template>
    <div class="chats-frame">
        <Chat></Chat>
        <Chat></Chat>
        <Chat></Chat>
    </div>
</template>

<script setup>
import Chat from './Chat.vue'
</script>

<style scoped>
    @import url(../css/fonts.css);
    @import url(../css/colors.css);

    .chats-frame {
        display: flex;
        flex-direction: column;

        height: fit-content;

        gap: 0.25rem;
        background-color: var(--primary-color);
        
        padding: 0.25rem;
        border-radius: 0.25rem;
    }
</style>
