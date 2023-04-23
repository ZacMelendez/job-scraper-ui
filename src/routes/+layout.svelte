<script>
	// import '../app.postcss';
	import { SvelteUIProvider } from '@svelteuidev/core';
	import '../styles/globals.scss';
	import { Icon } from '../components';
	import { signIn, signOut } from '@auth/sveltekit/client';

	import { page } from '$app/stores';
	import { Button } from 'flowbite-svelte';
	import { User } from 'lucide-svelte';
</script>

<div class="app">
	<header>
		<div class="logo">
			<Icon fill={'white'} size={36} />
			<h3>Svelte Job Scraper</h3>
		</div>
		{#if Object.keys($page.data.session || {}).length}
			<Button color="light" on:click={() => signOut()}
				><User style="padding-right: 3px;" size={16} />Sign out</Button
			>
		{:else}
			<Button color="light" on:click={() => signIn('google')}><User size={16} /> Sign In</Button>
		{/if}
	</header>
	<main>
		<SvelteUIProvider>
			<slot />
		</SvelteUIProvider>
	</main>

	<footer />
</div>

<style lang="scss">
	@import '../styles/breakpoints.scss';

	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 64rem;
		margin: 0 auto;
		box-sizing: border-box;

		max-height: calc(100vh - 60px);
		overflow: hidden;
	}

	header {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		padding: 1rem 1rem 0 1rem;
		width: 100%;
		max-width: 64rem;
		margin: 0 auto;
		box-sizing: border-box;

		max-height: 60px;

		.logo {
			display: flex;
			flex-direction: row;
			align-items: center;
			gap: 10px;
		}

		h3 {
			color: white;
			font-size: 24px;

			@include sm-max {
				font-size: 16px;
			}
		}
	}

	@media (min-width: 480px) {
		footer {
			padding: 12px 0;
		}
	}
</style>
