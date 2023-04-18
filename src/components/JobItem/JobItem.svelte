<script lang="ts">
	import type { JobItemProps } from '../../types';
	import { fade } from 'svelte/transition';
	import { linear } from 'svelte/easing';
	export let job: JobItemProps;
</script>

<div transition:fade={{ duration: 150, easing: linear }}>
	<a target="_blank" href={job.url} rel="noreferrer">
		<h3>{job.title}</h3>
		<p class="company">{job.company}</p>
		<p class="location">{job.location}</p>
	</a>
</div>

<style lang="scss">
	div {
		box-sizing: border-box;
		padding: 12px 15px;
		background: #e7ebea;

		transition: all linear 0.13s;

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
