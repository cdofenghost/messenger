<template>
    <div class="other-message-container">
        <div class="message-sender nunito-800">
            Message Sender
        </div>
        <div class="message-content">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet eaque quas blanditiis velit iure. In placeat quam, suscipit ex vitae sequi culpa maiores rem quia itaque id officiis quo consequuntur.
        </div>
    </div>
    <div class="your-message-container">
        <div class="message-sender nunito-800">
            Message Sender
        </div>
        <div class="message-content">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet eaque quas blanditiis velit iure. In placeat quam, suscipit ex vitae sequi culpa maiores rem quia itaque id officiis quo consequuntur.
        </div>
    </div>
</template>

<script setup>
</script>

<style scoped>
    @import url(../css/fonts.css);
    @import url(../css/colors.css);

    .your-message-container {
        background-color: var(--accent-color);
        color: var(--primary-color);
        align-self: flex-end;

        width: fit-content;
        max-width: 90%;
        height: fit-content;

        padding: 0.25rem;
        border-radius: 0.25rem;
    }

    .other-message-container {
        background-color: var(--primary-color);
        background-color: var(--primary-color);
        color: black;

        width: fit-content;
        max-width: 90%;
        height: fit-content;

        padding: 0.25rem;
        border-radius: 0.25rem;
    }

    .other-message-container .message-sender {
        font-size: 0.6rem;
        color: var(--accent-color);
    }
    .your-message-container .message-sender {
        font-size: 0.6rem;
        color: var(--primary-color);
    }
</style>
