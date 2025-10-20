<template>
    <div class="misc-bar">
        <div class="bar-frame" v-on:click="() => flipContent('switch-content')">
            <div class="user-icon">
                <img :src="'/src/static/imgs/666175.png'"></img>
            </div>
            <div class="user-name nunito-400">{{ userName }}</div>
        </div>
        <div id="switch-content" class="hidden-content">
            <SwitchButton :text="'User Profile'" :icon="'user'" v-on:click="() => flipContent('switch-us')"></SwitchButton>
            <div id="switch-us" class="user-settings">
                <form v-on:submit="updateUserData">
                    <div class="label-input nunito-400">
                        <div>username</div>
                        <input v-model="newUserName" placeholder="your username"></input>
                    </div>
                    <div class="label-input nunito-400">
                        <div>e-mail</div>
                        <input v-model="newEmail" type="email" placeholder="your e-mail"></input>
                    </div>
                    <div class="label-input nunito-400">
                        <div>bio</div>
                        <textarea v-model="newBio" placeholder="your bio"></textarea>
                    </div>
                    <input class="button" type="submit" value="Change User Data"></input>
                </form>
            </div>
            
            <SwitchButton :text="'Create New Chat'" :icon="'message'" v-on:click="() => flipContent('new-chat')"></SwitchButton>
        </div> 
    </div>
    <CreateChatForm></CreateChatForm>
</template>

<script>
    export default {
        data() {
            return {
                newUserName: this.userName,
                newBio: this.bio,
                newEmail: this.email,
            }
        },
        props: {
            userName: {
                type: String,
                default: "User Name"
            },
            email: {
                type: String,
                default: "mail@email.com"
            },
            bio: {
                type: String,
                default: ""
            },
        },
        methods: {
            async updateUserData(event) {
                event.preventDefault();

                const response = await fetch(`/api/users/me?name=${this.newUserName}&email=${this.newEmail}&bio=${this.newBio}`, {
                    method: "PUT",
                })
                // console.log(await response.json());
            }
        }
    }
</script>
<script setup>
    import CreateChatForm from './CreateChatForm.vue';
    import SwitchButton from './SwitchButton.vue';

    function flipContent(switchType)
    {
        const hiddenContent = document.getElementById(switchType); 

        if (hiddenContent.classList.contains('show')) hiddenContent.classList.remove('show');
        else hiddenContent.classList.add('show');
    }
</script>

<style scoped>
    @import url(../css/fonts.css);
    @import url(../css/colors.css);
    
	.button {
		border: none;
		height: 1.5rem;
		width: 100%;

		border-radius: 0.25rem;
		background-color: var(--primary-color) !important;
		color: var(--background-color);

		transition:
			background-color 0.1s ease-out,
			color 0.1s ease-out;
	}

	.button:hover {
		background-color: var(--accent-color-deep) !important;

		transition:
			background-color 0.1s ease-in,
			color 0.1s ease-in;
	}

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

    .misc-bar {
        overflow: hidden;
        border-radius: 0.25rem;
        margin-bottom: 0.25rem;
    }

	.hidden-content, .user-settings {
		opacity: 0;
		display: none;

		transform: translateY(-10px), scale(0);
		position: relative;
		z-index: 1000;

        background-color: var(--background-color);
        box-sizing: border-box;

		transition: all 0.3s ease;
		transition-property: overlay display opacity transform;
		transition-duration: 0.3s;
		transition-behavior: allow-discrete;
	}

    .user-settings {
        padding-left: 0.25rem;
    }

    .hidden-content {
        padding: 0.25rem;
    }

    .hidden-content form {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .hidden-content form input, .hidden-content form textarea{
        resize: none;
        outline: none;
        border: none;
        border-radius: 0.25rem;
        padding: 0.25rem;
        width: 100%;
        box-sizing: border-box;

        background-color: var(--grey-color);
        color: var(--white-color);

    }

    .hidden-content .label-input {
        font-size: 0.5rem;
        font-style: italic;
        color: var(--accent-color-deep);
    }

	.show {
		display: block;

		opacity: 1;
		transform: translateY(0), scale(1);
		@starting-style {
			opacity: 0;
		}
	}

    .bar-frame {
        display: flex;
        height: fit-content;

        align-items: center;
        font-size: 0.7rem;
        box-shadow: 0px 4px 16px 2px rgba(0, 0, 0, 10%);

        gap: 0.25rem;
        background-color: var(--grey-color);
        
        padding: 0.25rem;
        transition: 0.3s ease-out background-color;
    }

    .bar-frame:hover {
        background-color: var(--grey-light-color);

        transition: 0.1s ease-in background-color;
    }

    .user-icon {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: linear-gradient(90deg, #7F56D9, #9E77ED);
        overflow: hidden;

        box-sizing: content-box;
        flex-shrink: 0;
    }

    .user-icon img {
        max-height: 100%;
        max-width: 100%;
    }

</style>
