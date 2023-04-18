<script lang="ts">
	import { JobFetch } from '../helpers/';
	import { JobItem, JobSearch } from '../components';
	import { onMount } from 'svelte';
	import { jobList, modalState, userStore } from './store';
	import { Modal, TextInput } from '@svelteuidev/core';
	import { formProps } from '../components/JobSearch/store';
	import { signIn, signOut } from '@auth/sveltekit/client';
	import { page } from '$app/stores';
	import { User, Filter } from 'lucide-svelte';

	onMount(async () => {
		const response = await JobFetch({
			must: [],
			include: ['software', 'developer'],
			exclude: ['manager', 'lead', 'principal'],
			locations: []
		});

		$formProps.include = 'software, developer';
		$formProps.exclude = 'manager, lead, principal';

		$jobList.jobs = response?.info;
		$jobList.filteredJobs = response?.info;

		$userStore.favorites = $page.data.session?.user?.favorites || [];
		$userStore.userId = $page.data.session?.user?.id || '';
	});

	const searchJobs = (props: any) => {
		const { target } = props;
		const data = target?.value;

		if (!data || data == '') return ($jobList.filteredJobs = $jobList.jobs);
		return ($jobList.filteredJobs = $jobList.jobs.filter((job) => {
			let jobTitle = job.title.toLowerCase();
			let jobLocation = job.location.toLowerCase();
			let jobCompany = job.company.toLowerCase();

			return (
				jobTitle.includes(data.toLowerCase()) ||
				jobLocation.includes(data.toLowerCase()) ||
				jobCompany.includes(data.toLowerCase())
			);
		}));
	};
</script>

<svelte:head>
	<title>Job Scraper</title>
	<meta name="description" content="SvelteKit Job Scraper" />
</svelte:head>

<Modal opened={$modalState.opened} on:close={() => ($modalState.opened = false)}>
	<JobSearch />
</Modal>

<div class="job-items">
	<div class="menu-bar">
		<TextInput placeholder="Search..." bind:value={$jobList.jobSearch} on:input={searchJobs} />
		<button
			on:click={() => {
				$modalState.opened = true;
			}}
			class="button"
		>
			<Filter size={16} />Filters
		</button>
		{#if Object.keys($page.data.session || {}).length}
			<button class="button" on:click={() => signOut()}> <User size={16} />Sign out</button>
		{:else}
			<button class="button" on:click={() => signIn('google')}> <User size={16} />Sign In</button>
		{/if}
	</div>
	<p>Found {$jobList.filteredJobs.length} items</p>
	<ul class="job-list">
		{#each $jobList.filteredJobs as item}
			<li>
				<JobItem
					job={item}
					favorite={$userStore.favorites.includes(
						`${item.company.toLowerCase().split(' ').join('-')}-${item.job_id}`
					)}
				/>
			</li>
		{/each}
	</ul>
</div>

<style lang="scss">
	.job-items {
		padding: 5px 15px;
		display: relative;
		width: 100%;
		ul {
			margin: 0;
			padding: 0;
			display: flex;
			flex-direction: column;
			gap: 0px;
			box-shadow: 3px 3px 55px rgba(0, 0, 0, 0.248);
			max-height: calc(100vh - 16px - 50px);
			overflow-y: scroll;

			li {
				list-style-type: none;
			}
			li + li {
				border-top: 1px solid rgb(212, 212, 212);
			}
		}
	}
	.button {
		background-color: #d4dedb;
		border: none;
		padding: 10px 15px;
		border-radius: 7px;
		cursor: pointer;

		display: flex;
		flex-direction: row;
		gap: 5px;
		align-items: center;

		transition: all 0.15s linear;

		&:hover {
			background-color: #c4caca;
			transform: scale(1.015);
		}
	}
	.menu-bar {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		width: 100%;
		align-items: center;
		gap: 15px;
		height: 50px;
	}
</style>
