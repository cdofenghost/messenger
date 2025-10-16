<template>
    <label class="approve nunito-400" id="approve-msg"></label>
</template>

<script setup>
</script>

<style scoped>

	.approve {
		color: white;
		background-color: var(--success-color);
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

	.approve.show {
		display: block;

		opacity: 1;
		transform: translateY(0), scale(1);
		@starting-style {
			opacity: 0;
		}
	}

</style>
