<script lang="ts">
	import { TextInput } from '@svelteuidev/core';
	import { JobFetch } from '../../helpers';
	import { formProps } from './store';

	import type { JobItemProps } from '../../types';
	import { jobList } from '../../routes/store';

	const onSubmit = async () => {
		const { must, include, exclude } = $formProps;

		const results = await JobFetch({
			must: must == '' ? null : must.split(','),
			include: include == '' ? null : include.split(','),
			exclude: exclude == '' ? null : exclude.split(',')
		});
		$jobList.jobs = results?.info;
	};
</script>

<div>
	<form on:submit={onSubmit} class="content">
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
			label="Exclude"
			description="List keywords that the title must not have any of, as a list of comma separated strings"
			bind:value={$formProps.exclude}
		/>
		<button type="submit">Search</button>
	</form>
</div>

<style lang="scss">
	div {
		box-sizing: border-box;
		border-radius: 10px;
		padding: 10px;
	}
</style>
