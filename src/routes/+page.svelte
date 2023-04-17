<script lang="ts">
	import { JobFetch } from '../helpers/';
	import { JobItem, JobSearch } from '../components';
	import { onMount } from 'svelte';
	import { jobList, modalState } from './store';
	import { Modal, Button } from '@svelteuidev/core';

	onMount(async () => {
		const response = await JobFetch({
			must: [],
			include: ['software', 'developer'],
			exclude: ['manager', 'lead', 'principal'],
			locations: []
		});
		$jobList.jobs = response?.info;
	});

	const buttonStyles = {
		backgroundColor: '#d4dedb'
	};
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<Modal
	opened={$modalState.opened}
	on:close={() => ($modalState.opened = false)}
	title="Introduce yourself!"
>
	<JobSearch />
</Modal>

<div class="job-items">
	<button
		on:click={() => {
			$modalState.opened = true;
		}}
		class="button"
	>
		Search Filters
	</button>
	<p>Found {$jobList.jobs.length} items</p>
	<ul>
		{#each $jobList.jobs as item, i}
			<li>
				<JobItem job={item} />
			</li>
		{/each}
	</ul>
</div>

<style lang="scss">
	.job-items {
		padding: 5px 15px;
		ul {
			margin: 0;
			padding: 0;
			display: flex;
			flex-direction: column;
			gap: 15px;
			li {
				list-style-type: none;
			}
		}
	}
	.button {
		background-color: #d4dedb;
		border: none;
		padding: 10px 15px;
		border-radius: 7px;
		cursor: pointer;

		transition: all 0.15s linear;

		&:hover {
			background-color: #c4caca;
			transform: scale(1.015);
		}
	}
</style>
