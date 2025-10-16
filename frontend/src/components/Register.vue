<template>
	<div class="middle-container">
		<div class="heading nunito-600">mini messenger</div>
		<div class="desc nunito-300">private and safe place to chat with your friends</div>
		<div class="input-container nunito-200">
			<form id="registration-form" v-on:submit="validateForm">
				<ApprovePopup></ApprovePopup>
				<ErrorPopup></ErrorPopup>
				<input class="input-text" type="email" placeholder="your e-mail" v-model="email" required></input>
				<input class="input-text" type="password" placeholder="your password" minlength="8" v-model="password" required></input>
				<input class="input-text" type="password" placeholder="repeat your password" minlength="8" v-model="confirmPassword" required></input>
				<div class="button-container">
					<input type="submit" value="Sign Up" class="button-1 nunito-600"></input>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
	import { BASE_URL } from '@/other';
	import ApprovePopup from './ApprovePopup.vue';
	import ErrorPopup from './ErrorPopup.vue';

	const headers = new Headers();
	headers.append('Content-Type', 'application/json');

	export default {
		data() {
			return {
				email: '',
				password: '',
				confirmPassword: '',
			}
		},
		methods: {
			async validateForm()
			{
				const errorPopup = document.getElementById('error-msg');
				event.preventDefault();

				if(this.password !== this.confirmPassword){
					errorPopup.textContent = "Password doesn't match repeated password.";
					errorPopup.classList.add('show');
				}
				else {
					errorPopup.classList.remove('show');
					return await this.registerUser();
				}
			},
			async registerUser()
			{
				const errorPopup = document.getElementById('error-msg');
				const approvePopup = document.getElementById('approve-msg');
				try {
					const response = await fetch(`${BASE_URL}/users/register`, {
						method: "POST",
						headers: headers,
						body: JSON.stringify({
							email: this.email, 
							password: this.password, 
							repeated_password: this.confirmPassword,
						}),
					});

					if (!response.ok) throw new Error(`${(await response.json()).detail}`);

					else {
						approvePopup.textContent = "You have successfully register new account.";
						approvePopup.classList.add('show');
						errorPopup.classList.remove('show');

						setTimeout(() => {
							this.$router.push('/authorize');
						}, 1000);
					}

				} catch (error) {
					console.error(`Error: ${error.message}`);
					errorPopup.textContent = await error.message;
					errorPopup.classList.add('show');
					approvePopup.classList.remove('show');
				}
			} 
		}
	}
</script>
<script setup>
</script>

<style scoped>
	@import url(../css/colors.css);
	@import url(../css/fonts.css);

	.heading {
		text-align: center;
		font-size: 2rem;
		color: var(--primary-color);
	}

	.desc {
		text-align: center;
		font-size: 1rem;
		color: var(--primary-color);
	}

	.middle-container {
		border: 4px solid var(--accent-color-light);
		border-radius: 1rem;
		box-sizing: content-box;
		align-content: center;

		height: 94vh;
	}

	.input-container form {
		display: flex;
		flex-direction: column;
		box-sizing: border-box;

		align-items: center;
		justify-self: center;

		margin-top: 1rem;

		width: 24rem;
		gap: 0.5rem;
	}

	.button-container {
		display: flex;
		box-sizing: border-box;

		justify-content: center;
		justify-self: center;

		width: 24rem;
		gap: 0.5rem;
	}

	.button-1 {
		border: none;
		height: 1.5rem;
		width: 100%;

		border-radius: 0.25rem;
		background-color: var(--primary-color);
		color: var(--white-color);

		transition:
			background-color 0.1s ease-out,
			color 0.1s ease-out;
	}

	.button-1:hover {
		background-color: var(--accent-color-deep);

		transition:
			background-color 0.1s ease-in,
			color 0.1s ease-in;
	}

	.input-text {
		outline: none;
		border: solid 0.125rem transparent;
		box-sizing: border-box;

		font-size: 0.8rem;

		background-color: var(--grey-color);
		border-radius: 0.5rem;
		padding: 0.25rem 1rem;
		height: 2rem;
		
		color: var(--primary-color-contrast);
		caret-color: var(--accent-color-deep);

		width: 100%;

		text-align: left;
		justify-content: center;

		transition:
			border 0.1s ease-out;
	}

	.input-text:hover {
		border: solid 0.125rem var(--primary-color);
		transition: border 0.3s ease-in;
	}
</style>
