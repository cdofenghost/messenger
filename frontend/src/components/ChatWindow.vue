<template>
    <div class="chat-container">
        <div class="chat-bar">
            <div class="chat-icon">
                <img src="../static/imgs/666175.png"></img>
            </div>
            <div class="detail-info">
                <div class="chat-name nunito-600">Chat Name</div>
                <div class="chat-member-count nunito-400">5 members</div>
            </div>
        </div>
        <div class="chat">
            <Message></Message>
            <Message></Message>
            <Message></Message>
            <Message></Message>
            <Message></Message>
            <Message></Message>
            <Message></Message>
            <Message></Message>
            <Message></Message>
            <Message></Message>
            <Message></Message>
            <Message></Message>
            <div class="input-bar">
                <textarea class="nunito-400" placeholder="Message" type="text"></textarea>
            </div>  
        </div>
    </div>
</template>

<script setup>
    import Message from './Message.vue'
</script>

<style scoped>
    @import url(../css/fonts.css);
    @import url(../css/colors.css);

    .chat-container {
        display: flex;
        flex-direction: column;

        background-color: var(--primary-color);
        border-radius: 0.25rem;
        font-size: 0.75rem;

        width: 100%;

        gap: 0.25rem;
        padding: 0.25rem;
        box-sizing: border-box;
    }

    .chat-icon {
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        background-color: var(--accent-color);
        overflow: hidden;

        box-sizing: border-box;

    }
    .chat-icon img {
        max-height: 100%;
        max-width: 100%;

        box-sizing: border-box;
    }

    .chat-bar {
        display: flex;
        gap: 0.25rem;
        align-items: center;

        box-sizing: border-box;

    }

    .chat-member-count {
        color: var(--accent-color);
    }

    .chat {
        display: flex;
        flex-direction: column;
        position: relative;
        gap: 0.25rem;

        background-color: var(--deep-color);
        color: var(--primary-color);

        width: 100%;
        height: 88vh;
        border-radius: 0.25rem;

        padding: 0.25rem 20%;
        overflow-x: hidden;
        overflow-y: scroll;
        
        scrollbar-color: var(--primary-color) var(--accent-color);
        scrollbar-width: thin;
        box-sizing: border-box;
    }

    .input-bar {
        position: sticky;
        bottom: 0;
        box-shadow: 0px 0px 16px 2px rgba(0, 0, 0, 25%);

        height: fit-content;
        max-height: 20vh;
        width: 100%;

        background-color: var(--primary-color);
        padding: 0.25rem;
        border-radius: 0.25rem;

        box-sizing: border-box;
    }

    .input-bar textarea {
        -ms-overflow-style: none;
        scrollbar-width: none;

        font-size: 0.7rem;
        border: none;
        outline: none;

        background-color: var(--primary-color);
        resize: none;
        field-sizing: content;

        width: 100%;
        max-height: 20vh;
        box-sizing: border-box;
    }
</style>
