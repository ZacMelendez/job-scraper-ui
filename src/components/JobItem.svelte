<script lang="ts">
	import type { JobItemProps } from '../types';
	import { Star, MapPin } from 'lucide-svelte';
	import { jobList, userStore } from '../routes/store';
	import { page } from '$app/stores';
	import IntersectionObserver from 'svelte-intersection-observer';
	import { JobFetch, toTitleCase } from '../helpers';
	import { activeFilters } from './filterStore';

	let element: HTMLElement;
	let intersecting: boolean;
	export let lastFetched: boolean;

	export let job: JobItemProps;
	export let favorite = false;
	export const job_id = `${job.company.toLowerCase().split(' ').join('-')}-${job.job_id}`;

	const fetchMoreJobs = async () => {
		const response = await JobFetch({
			lastEvalKey: job.jobUrl,
			exclude: $activeFilters.excludeTags,
			include: $activeFilters.includeTags
		});

		$jobList.jobs = [...$jobList.jobs, ...(response?.data ? response.data : [])];
		$jobList.filteredJobs = [...$jobList.filteredJobs, ...(response?.data ? response.data : [])];

		$jobList.returnedJobCount = response?.data.length;
	};

	const handleFavorite = async () => {
		favorite = !favorite;

		let newFavorites: string[] = [];
		const job_id = `${job.company.toLowerCase().split(' ').join('-')}-${job.job_id}`;

		if (favorite) {
			newFavorites = [...$userStore.favorites, job_id];

			userStore.update((val) => {
				return { userId: val.userId, favorites: newFavorites };
			});
		} else {
			newFavorites = $userStore.favorites.filter((job) => job != job_id);

			userStore.update((val) => {
				return { userId: val.userId, favorites: newFavorites };
			});
		}

		await fetch('/api', {
			method: 'POST',
			body: JSON.stringify({ user_id: $userStore.userId, favorites: newFavorites.join(',') }),
			headers: {
				'Content-Type': 'application/json'
			}
		});
	};
</script>

<div class="card" bind:this={element}>
	{#if Object.keys($page.data.session || {}).length}
		<button style="border: none; cursor: pointer" on:click={handleFavorite}>
			<Star
				class="star"
				color={favorite ? '#00000000' : 'rgb(75, 85, 99)'}
				fill={favorite ? 'gold' : '#00000000'}
			/>
		</button>
	{/if}

	<a target="_blank" href={job.jobUrl} rel="noreferrer" class="job-text">
		<h3 class="mb-2 text-base md:text-xl font-bold tracking-tight text-gray-900 dark:text-white">
			{job.title}
		</h3>
		<p class="text-sm md:font-normal text-gray-700 dark:text-gray-400 leading-tight">
			{toTitleCase(job.company)}
		</p>

		{#if job.location.trim() != ''}
			<p
				style="display: flex; flex-direction: row; align-items: center; gap: 2px"
				class="text-sm md:font-normal text-gray-700 dark:text-gray-400 leading-tight"
			>
				<MapPin size={16} />{toTitleCase(job.location)}
			</p>
		{/if}
	</a>
	{#if lastFetched}
		<IntersectionObserver
			on:intersect={() => {
				if ($activeFilters.excludeTags.length > 0 || $activeFilters.includeTags.length > 0) return;
				fetchMoreJobs();
			}}
			once
			{element}
			bind:intersecting
		/>
	{/if}
</div>

<style lang="scss">
	.card {
		box-sizing: border-box;
		padding: 12px 15px;

		transition: all linear 0.13s;
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 10px;

		a {
			&:link,
			&:visited,
			&:active,
			&:hover {
				text-decoration: none;
			}

			&:hover {
				h3 {
					text-decoration: underline;
				}
			}
			* {
				padding: 0;
				margin: 0;
			}
			flex-grow: 1;
		}

		cursor: pointer;

		overflow: hidden;

		&:hover {
			transform: scale(1.005);
		}
	}
</style>
