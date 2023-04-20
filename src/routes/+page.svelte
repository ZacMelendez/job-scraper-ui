<script lang="ts">
	import { JobFetch } from '../helpers/';
	import { JobItem, JobSearch } from '../components';
	import { jobList, userStore } from './store';
	import { Input, Button, ButtonGroup } from 'flowbite-svelte';
	import { signIn, signOut } from '@auth/sveltekit/client';
	import { page } from '$app/stores';

	import { User, Search } from 'lucide-svelte';
	import { onMount } from 'svelte';

	const handleSearch = async () => {
		const response = await JobFetch({ search: $jobList.jobSearch });
		$jobList.jobs = response?.data;
		$jobList.filteredJobs = response?.data;
	};

	const fetchJobs = async () => {
		const response = await JobFetch({});

		$jobList.jobs = response?.data;
		$jobList.filteredJobs = response?.data;

		$userStore.favorites = $page.data.session?.user?.favorites || [];
		$userStore.userId = $page.data.session?.user?.id || '';
	};

	onMount(() => {
		fetchJobs();
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

<JobSearch />

<div class="job-items">
	<div class="menu-bar">
		<div class="search-bar">
			<ButtonGroup class="w-full">
				<Input
					class="search-bar"
					placeholder="Search..."
					bind:value={$jobList.jobSearch}
					on:input={searchJobs}
				/>
				<!-- <Button color="blue" on:click={handleSearch}><Search size={16} /></Button> -->
			</ButtonGroup>
		</div>
		<div class="actions">
			<!-- <Button
				on:click={() => {
					$modalState.opened = true;
				}}
				color="light"
			>
				<Filter size={16} /> Filters
			</Button> -->
			{#if Object.keys($page.data.session || {}).length}
				<Button color="light" on:click={() => signOut()}
					><User style="padding-right: 3px;" size={16} />Sign out</Button
				>
			{:else}
				<Button color="light" on:click={() => signIn('google')}><User size={16} /> Sign In</Button>
			{/if}
		</div>
	</div>
	<!-- {#if $jobList.filteredJobs.length}
		<p class="font-normal text-gray-700 dark:text-gray-400 leading-tight">
			Found {$jobList.filteredJobs.length} items
		</p>
	{/if} -->
	<ul class="job-list">
		{#each $jobList.filteredJobs as item, i}
			<li>
				<JobItem
					job={item}
					favorite={$userStore.favorites.includes(
						`${item.company.toLowerCase().split(' ').join('-')}-${item.job_id}`
					)}
					lastFetched={(i + 1) % 20 == 0}
				/>
			</li>
		{/each}
	</ul>
</div>

<style lang="scss">
	@import '../styles/breakpoints.scss';
	.job-items {
		padding: 5px 15px;
		position: relative;
		width: 100%;

		@include sm-max {
			padding: 0;
		}
		ul {
			margin: 0;
			padding: 0;
			display: flex;
			flex-direction: column;
			gap: 0px;
			// box-shadow: 3px 3px 55px rgba(0, 0, 0, 0.248);
			max-height: calc(100vh - 16px - 50px - 50px);
			overflow-y: scroll;

			li {
				list-style-type: none;
				// border: 1px solid rgb(75, 85, 99);
			}
			li {
				border-bottom: 1px solid rgb(75, 85, 99);
			}
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

		.actions {
			display: flex;
			flex-direction: row;
			gap: 15px;
		}
		.search-bar {
			flex-grow: 1;
			@include sm-max {
				width: 100%;
			}
		}

		@include sm-max {
			flex-direction: column;
			align-items: flex-start;
			height: auto;
			gap: 5px;
		}
	}

	.loading {
		ul {
			list-style-type: none;
		}

		.loading-item {
			padding: 0 30px;
		}
		.skeleton {
			border-radius: 0.25rem;
			animation: skeleton-loading 1s linear infinite alternate;
		}

		.skeleton-card-brand {
			width: 70%;
			height: 0.7rem;
			margin: 0.5rem;
			border-radius: 0.25rem;
			@include sm-max {
				width: 40%;
			}
		}

		.skeleton-card-text {
			padding: 10px;
		}

		.skeleton-card-title {
			width: 100%;
			height: 0.9rem;
			margin: 0.5rem;
		}

		.skeleton-item {
			width: 40%;
			@include sm-max {
				width: 90%;
			}
		}

		@keyframes skeleton-loading {
			0% {
				background-color: var(--skeleton-loader-dark);
			}
			100% {
				background-color: var(--skeleton-loader-light);
			}
		}
	}
</style>
