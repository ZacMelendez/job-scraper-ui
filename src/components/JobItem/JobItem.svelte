<script lang="ts">
	import type { JobItemProps } from '../../types';
	export let job: JobItemProps;
</script>

<div>
	<a target="_blank" href={job.url} rel="noreferrer">
		<h3>{job.title}</h3>
		<h5>{job.company}</h5>
		<h5>{job.location}</h5>
	</a>
</div>

<style lang="scss">
	div {
		* {
			color: #2e2c3d;
			padding: 2px 5px;
		}
		box-sizing: border-box;
		border-radius: 2px;
		padding: 10px;
		background-image: linear-gradient(180deg, #e7ebea 0%, #d5d8d8 90%);
		box-shadow: 2px 2px 10px #9696967d;

		a {
			&:link,
			&:visited,
			&:active,
			&:hover {
				text-decoration: none;
			}
		}

		cursor: pointer;

		transition: all ease-in-out 0.3s;
		overflow: hidden;

		&:hover {
			transform: scale(1.01);
		}
	}
</style>
