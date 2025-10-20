<template>
    <div class="switch-button nunito-200">
        <font-awesome-icon :icon=icon></font-awesome-icon>
        {{ text }}
    </div>
</template>

<script setup>
const props = defineProps({
    text: {
        type: String,
        default: "Switch Button",
    },
    icon: {
        type: String,
        default: "",
    }
});
</script>

<style scoped>
    @import url(../css/fonts.css);
    @import url(../css/colors.css);

    .switch-button {
        width: 100%;
        padding: 0.25rem;
        font-size: 0.7rem;
        box-sizing: border-box;

        transition: 0.3s ease-out background-color;
    }

    .switch-button:hover {
        background-color: var(--grey-color);
        border-radius: 0.25rem;

        transition: 0.1s ease-in background-color;
    }
</style>
