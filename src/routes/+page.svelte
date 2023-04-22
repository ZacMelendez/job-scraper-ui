<script lang="ts">
	import { JobFetch } from '../helpers/';
	import { Drawer, JobItem } from '../components';
	import { jobList, userStore } from './store';
	import { Input, Button, ButtonGroup } from 'flowbite-svelte';
	import { page } from '$app/stores';

	import { Search, SlidersHorizontal } from 'lucide-svelte';
	import { onMount } from 'svelte';

	let drawer = true;

	const handleSearch = async () => {
		const response = await JobFetch({ search: $jobList.jobSearch });
		$jobList.jobs = response?.data;
		$jobList.filteredJobs = response?.data;

		$jobList.returnedJobCount = response?.data.length;
		$jobList.searched = true;
	};

	const fetchJobs = async () => {
		const response = await JobFetch({});

		$jobList.jobs = response?.data;
		$jobList.filteredJobs = response?.data;

		$userStore.favorites = $page.data.session?.user?.favorites || [];
		$userStore.userId = $page.data.session?.user?.id || '';

		$jobList.returnedJobCount = response?.data.length;

		$jobList.searched = false;
	};

	onMount(() => {
		if ($jobList.searched) return;
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

<Drawer hidden1={drawer} />

<div class="job-items">
	<div class="menu-bar">
		<div class="search-bar">
			<ButtonGroup class="w-full h-full">
				<Input placeholder="Search..." bind:value={$jobList.jobSearch} on:input={searchJobs} />
				<Button color="blue" on:click={handleSearch}><Search size={16} /></Button>
			</ButtonGroup>
		</div>
		<!-- <div class="actions">
			<Button
				color="light"
				on:click={() => {
					drawer = false;
				}}><SlidersHorizontal size={16} /></Button
			>
		</div> -->
	</div>

	<ul class="job-list">
		{#each $jobList.filteredJobs as item, i}
			<li>
				<JobItem
					job={item}
					favorite={$userStore.favorites.includes(
						`${item.company.toLowerCase().split(' ').join('-')}-${item.job_id}`
					)}
					lastFetched={(i + 1) % $jobList.returnedJobCount == 0}
					search={$jobList.searched ? $jobList.jobSearch : null}
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
		height: 40px;

		.actions {
			display: flex;
			flex-direction: row;
			gap: 15px;
			height: 100%;
		}
		.search-bar {
			flex-grow: 1;
			height: 100%;

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

	// .loading {
	// 	ul {
	// 		list-style-type: none;
	// 	}

	// 	.loading-item {
	// 		padding: 0 30px;
	// 	}
	// 	.skeleton {
	// 		border-radius: 0.25rem;
	// 		animation: skeleton-loading 1s linear infinite alternate;
	// 	}

	// 	.skeleton-card-brand {
	// 		width: 70%;
	// 		height: 0.7rem;
	// 		margin: 0.5rem;
	// 		border-radius: 0.25rem;
	// 		@include sm-max {
	// 			width: 40%;
	// 		}
	// 	}

	// 	.skeleton-card-text {
	// 		padding: 10px;
	// 	}

	// 	.skeleton-card-title {
	// 		width: 100%;
	// 		height: 0.9rem;
	// 		margin: 0.5rem;
	// 	}

	// 	.skeleton-item {
	// 		width: 40%;
	// 		@include sm-max {
	// 			width: 90%;
	// 		}
	// 	}

	// 	@keyframes skeleton-loading {
	// 		0% {
	// 			background-color: var(--skeleton-loader-dark);
	// 		}
	// 		100% {
	// 			background-color: var(--skeleton-loader-light);
	// 		}
	// 	}
	// }
</style>
