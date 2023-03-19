<script lang="ts">
	import { JobFetch } from '../helpers/';
	import { JobItem, JobSearch } from '../components';
	import { onMount } from 'svelte';
	import type { JobItemProps } from '../types';
	import { jobList } from './store';

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

<div class="job-items">
	<JobSearch jobs={$jobList.jobs} />
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
