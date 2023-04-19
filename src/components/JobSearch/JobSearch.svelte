<script lang="ts">
	import { TextInput } from '@svelteuidev/core';
	import { JobFetch } from '../../helpers';
	import { formProps } from './store';
	import { modalState } from '../../routes/store';
	import { Button, Input, Label, Modal } from 'flowbite-svelte';

	import { jobList } from '../../routes/store';

	const onSubmit = async () => {
		const results = await JobFetch({
			must: $formProps.must == '' ? null : $formProps.must.split(','),
			include: $formProps.include == '' ? null : $formProps.include.split(','),
			exclude: $formProps.exclude == '' ? null : $formProps.exclude.split(','),
			locations: $formProps.locations == '' ? null : $formProps.locations.split(',')
		});

		const uniqueVals = [...new Map(results?.info.map((item) => [item['url'], item])).values()];
		$jobList.jobs = uniqueVals;
		$jobList.filteredJobs = uniqueVals;

		$modalState.opened = false;
	};

	const onClear = () => {
		$formProps.must = '';
		$formProps.include = '';
		$formProps.exclude = '';
		$formProps.locations = '';
	};
</script>

<Modal title="Search Parameters" bind:open={$modalState.opened} autoclose>
	<div>
		<Label class="mb-2">Must Have</Label>
		<p>List keywords that the job title must have all of, as a list of comma separated strings</p>
		<Input bind:value={$formProps.must} />
	</div>
	<div>
		<Label class="mb-2">Include</Label>
		<p>
			List keywords that the job title can have at least one of, as a list of comma separated
			strings
		</p>
		<Input bind:value={$formProps.include} />
	</div>
	<div>
		<Label class="mb-2">Locations</Label>
		<p>
			List locations in which the job posting should be in, as a list of comma separated strings
		</p>
		<Input bind:value={$formProps.locations} />
	</div>
	<div>
		<Label class="mb-2">Exclude</Label>
		<p>List keywords that the title must not have any of, as a list of comma separated strings</p>
		<Input bind:value={$formProps.exclude} />
	</div>

	<svelte:fragment slot="footer">
		<Button color="light" on:click={onClear}>Clear</Button>
		<Button color="light" on:click={onSubmit}>Search</Button>
	</svelte:fragment>
</Modal>
