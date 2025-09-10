<template>
    <div class="chat-frame">
        <div class="chat-icon">
            <img src="../static/imgs/666175.png"></img>
        </div>
        <div class="chat-info">
            <div class="name-message">
                <div class="chat-name nunito-600">
                    Chat Name
                </div>
                <div class="last-message nunito-300">
                    Andrey: what the actual fuck how am i going to do this
                </div>
            </div>
            <div class="last-msg-time nunito-200">
                03:03
            </div>
        </div>
    </div>
</template>

<script>
</script>

<style scoped>
    @import url(../css/fonts.css);
    @import url(../css/colors.css);

    .chat-frame:hover {
        background-color: var(--background-color);

        transition: background-color 0.1s ease-in;
    }

    .chat-frame {
        background-color: var(--accent-color);

        transition: background-color 0.1s ease-in;
    }

    .chat-frame {
        font-size: 0.7rem;

        display: flex;
        background-color: var(--deep-color);
        border-radius: 0.5rem;

        color: var(--primary-color);
        font-size: 0.75rem;
        padding: 0.25rem;

        align-items: center;
        display: flex;
        gap: 0.25rem;
    }
    
    .chat-info {
        width: 100%;
        display: flex;

        justify-content: space-between;
    }

    .chat-icon {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background-color: var(--accent-color);
        overflow: hidden;

        box-sizing: content-box;
        flex-shrink: 0;
    }

    .chat-icon img {
        max-height: 100%;
        max-width: 100%;
    }

    .last-message {
        font-size: 0.7rem;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;

        max-width: 10vw;
    }
</style>
