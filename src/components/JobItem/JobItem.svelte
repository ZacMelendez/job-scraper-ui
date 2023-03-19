<script lang="ts">
	import type { JobItemProps } from '../../types';
	export let job: JobItemProps;
</script>

<div>
	<a target="_blank" href={job.url} rel="noreferrer">
		<h3>{job.title}</h3>
		<h5>{job.company}</h5>
	</a>
</div>

<style lang="scss">
	div {
		border: solid 1px black;
		box-sizing: border-box;
		border-radius: 10px;
		padding: 10px;

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

		&:hover {
			transform: scale(1.02);
		}
	}
</style>
