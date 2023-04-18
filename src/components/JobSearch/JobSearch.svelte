<script lang="ts">
	import { TextInput } from '@svelteuidev/core';
	import { JobFetch } from '../../helpers';
	import { formProps } from './store';
	import { modalState } from '../../routes/store';

	import { jobList } from '../../routes/store';

	const onSubmit = async () => {
		const results = await JobFetch({
			must: $formProps.must == '' ? null : $formProps.must.split(','),
			include: $formProps.include == '' ? null : $formProps.include.split(','),
			exclude: $formProps.exclude == '' ? null : $formProps.exclude.split(','),
			locations: $formProps.locations == '' ? null : $formProps.locations.split(',')
		});
		$jobList.jobs = results?.info;
		$jobList.filteredJobs = results?.info;

		$modalState.opened = false;
	};

	const onClear = () => {
		$formProps.must = '';
		$formProps.include = '';
		$formProps.exclude = '';
		$formProps.locations = '';
	};
</script>

<div>
	<div class="content">
		<TextInput
			label="Must have"
			description="List keywords that the job title must have all of, as a list of comma separated strings"
			bind:value={$formProps.must}
		/>
		<TextInput
			label="Include"
			description="List keywords that the job title can have at least one of, as a list of comma separated strings"
			bind:value={$formProps.include}
		/>
		<TextInput
			label="Locations"
			description="List locations in which the job posting should be in, as a list of comma separated strings"
			bind:value={$formProps.locations}
		/>
		<TextInput
			label="Exclude"
			description="List keywords that the title must not have any of, as a list of comma separated strings"
			bind:value={$formProps.exclude}
		/>
		<div class="actions">
			<button class="button" on:click={onClear}>Clear</button>
			<button class="button" on:click={onSubmit}>Search</button>
		</div>
	</div>
</div>

<style lang="scss">
	div {
		.content {
			display: flex;
			flex-direction: column;
			gap: 15px;

			.actions {
				display: flex;
				flex-direction: row;
				justify-content: space-between;
				.button {
					background-color: #d4dedb;
					border: none;
					padding: 10px 15px;
					border-radius: 7px;
					cursor: pointer;

					transition: all 0.15s linear;

					&:hover {
						background-color: #c4caca;
						transform: scale(1.015);
					}
				}
			}
		}
		box-sizing: border-box;
		border-radius: 10px;
		padding: 10px;
	}
</style>
