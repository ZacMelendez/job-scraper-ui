<script lang="ts">
	import type { JobItemProps } from '../../types';
	import { fade } from 'svelte/transition';
	import { linear } from 'svelte/easing';
	import { Star, MapPin } from 'lucide-svelte';
	import { userStore } from '../../routes/store';
	import { page } from '$app/stores';
	import { onMount, validate_component } from 'svelte/internal';

	export let job: JobItemProps;
	export let favorite: boolean = false;
	export const job_id: string = `${job.company.toLowerCase().split(' ').join('-')}-${job.job_id}`;

	const handleFavorite = async () => {
		favorite = !favorite;

		let newFavorites: string[] = [];
		const job_id = `${job.company.toLowerCase().split(' ').join('-')}-${job.job_id}`;

		console.log($userStore);

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

		await fetch('/', {
			method: 'POST',
			body: JSON.stringify({ user_id: $userStore.userId, favorites: newFavorites.join(',') }),
			headers: {
				'Content-Type': 'application/json'
			}
		});
	};
</script>

<div transition:fade={{ duration: 150, easing: linear }}>
	{#if Object.keys($page.data.session || {}).length}
		<button style="border: none; cursor: pointer" on:click={handleFavorite}>
			<Star class="star" color="black" fill={favorite ? 'gold' : '#00000000'} />
		</button>
	{/if}

	<a target="_blank" href={job.url} rel="noreferrer">
		<h3>{job.title}</h3>
		<p class="company">{job.company}</p>

		{#if job.location.trim() != ''}
			<p style="display: flex; flex-direction: row; align-items: center; gap: 2px" class="location">
				<MapPin size={16} />{job.location}
			</p>
		{/if}
	</a>
</div>

<style lang="scss">
	div {
		box-sizing: border-box;
		padding: 12px 15px;
		background: #e7ebea;

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
				color: #2e2c3d;
				padding: 0;
				margin: 0;
			}
		}

		cursor: pointer;

		overflow: hidden;

		&:hover {
			transform: scale(1.005);
		}
	}
</style>
