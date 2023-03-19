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
			exclude: ['manager', 'lead', 'principal']
		});
		$jobList.jobs = response?.info;
	});
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
	<Button
		on:click={() => {
			$modalState.opened = true;
		}}>Search Filters</Button
	>
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
		box-sizing: border-box;
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
</style>
