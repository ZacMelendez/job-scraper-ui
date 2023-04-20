<script lang="ts">
	import { JobFetch } from '../helpers';
	import { formProps } from './store';
	import { modalState } from '../routes/store';
	import { Button, Input, Label, Modal } from 'flowbite-svelte';

	import { jobList } from '../routes/store';

	const onSubmit = async () => {
		const results = await JobFetch({});

		$jobList.jobs = results?.data;
		$jobList.filteredJobs = results?.data;

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
