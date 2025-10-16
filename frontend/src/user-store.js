import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
    const userData = ref(null);

    async function loadUserData(params) {
        try {
            const response = await fetch(`/api/users/me`, {credentials: 'include'});
            userData.value = await response.json();
            // console.log(userData.value);
        } catch (error) {
            console.error(error);
        }
    }

    return {
        userData,
        loadUserData,
    }
});
