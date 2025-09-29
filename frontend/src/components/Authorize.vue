<template>
	<div class="middle-container">
		<div class="heading nunito-600">mini messenger</div>
		<div class="desc nunito-300">private and safe place to chat with your friends</div>
		<div class="input-container nunito-300">
			<form id="authorization-form" v-on:submit="authorizeUser">
				<label class="error nunito-400" id="error-msg"></label>
				<label class="approve nunito-400" id="approve-msg"></label>
				<input class="input-text" type="email" placeholder="your e-mail" v-model="email" required></input>
				<input class="input-text" type="password" placeholder="your password" minlength="8" v-model="password" required></input>
				<div class="button-container">
					<input type="submit" value="Sign In" class="button-1 nunito-600"></input>
					<router-link style="width: 100%;" to="/register">
						<button class="button-1 nunito-600">Sign Up</button>
					</router-link>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
	import { BASE_URL } from '@/other';
	const headers = new Headers();
	headers.append('Content-Type', 'application/json');
	headers.append('Access-Control-Allow-Origin', `${BASE_URL}`)

	export default {
		data() {
			return {
				email: '',
				password: '',
			}
		},
		methods: {
			async authorizeUser(event)
			{
				event.preventDefault();
				const errorPopup = document.getElementById('error-msg');
				const approvePopup = document.getElementById('approve-msg');
				try {
					const response = await fetch(`/api/users/authorize`, {
						method: "POST",
						headers: headers,
						credentials: 'include',
						body: JSON.stringify({
							email: this.email, 
							password: this.password, 
						}),
					});

					console.log('Response headers:', response.headers);
					if (!response.ok) throw new Error(`${(await response.json()).detail}`);

					else {
						approvePopup.textContent = "Authorization complete.";
						approvePopup.classList.add('show');
						errorPopup.classList.remove('show');

						setTimeout(() => {
							this.$router.push('/funchat');
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
		border: 4px solid var(--accent-color);
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
		background-color: var(--accent-color);
		color: var(--primary-color);

		transition:
			background-color 0.1s ease-out,
			color 0.1s ease-out;
	}

	.button-1:hover {
		background-color: var(--primary-color);
		color: var(--accent-color);

		transition:
			background-color 0.1s ease-in,
			color 0.1s ease-in;
	}

	.input-text {
		outline: none;
		border: solid 0.125rem transparent;
		box-sizing: border-box;

		font-size: 0.8rem;

		background-color: var(--deep-color);
		border-radius: 0.5rem;
		padding: 0.25rem 1rem;
		height: 2rem;
		
		color: var(--primary-color);
		caret-color: var(--accent-color);

		width: 100%;

		text-align: left;
		justify-content: center;

		transition:
			border 0.1s ease-out;
	}

	.error, .approve {
		color: white;
		background-color: #9A3F3F;
		height: fit-content;

		border-radius: .25rem;
		font-style: italic;
		font-size: medium;

		opacity: 0;
		display: none;

		transform: translateY(-10px), scale(0);
		padding: 0.5em 1em;
		position: relative;
		z-index: 1000;

		transition: all 0.3s ease;
		transition-property: overlay display opacity transform;
		transition-duration: 0.3s;
		transition-behavior: allow-discrete;
	}

	.error.show, .approve.show {
		display: block;

		opacity: 1;
		transform: translateY(0), scale(1);
		@starting-style {
			opacity: 0;
		}
	}

	.approve {
		background-color: #59AC77;
	}


	.input-text:hover {
		border: solid 0.125rem var(--accent-color);
		transition: border 0.3s ease-in;
	}
</style>
