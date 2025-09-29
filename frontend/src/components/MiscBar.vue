<template>
    <div class="bar-frame">
        <div class="user-icon">
            <img :src="'/src/static/imgs/666175.png'"></img>
        </div>
        <div class="user-name nunito-400">{{ userName }}</div>
    </div>
</template>

<script>
    export default {
        props: {
            userName: {
                type: String,
                default: "User Name"
            }
        }
    }
</script>

<style scoped>
    @import url(../css/fonts.css);
    @import url(../css/colors.css);
    .bar-frame {
        display: flex;
        height: fit-content;

        align-items: center;
        font-size: 0.7rem;

        gap: 0.25rem;
        background-color: var(--primary-color);
        
        padding: 0.25rem;
        border-radius: 0.25rem;
    }

    .user-icon {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background-color: var(--accent-color);
        overflow: hidden;

        box-sizing: content-box;
        flex-shrink: 0;
    }

    .user-icon img {
        max-height: 100%;
        max-width: 100%;
    }

</style>
