import type { JobItemProps } from '../../types';

interface FetchResponse {
	info: JobItemProps[];
}

export default async function JobFetch({
	must,
	include,
	exclude,
	locations
}: {
	must: string[] | null;
	include: string[] | null;
	exclude: string[] | null;
	locations: string[] | null;
}): Promise<FetchResponse> {
	const url = new URL('https://fo7nireaw3.execute-api.us-east-1.amazonaws.com/Prod/jobs');

	must?.length && url.searchParams.set('must', must.join(','));
	include?.length && url.searchParams.set('include', include.join(','));
	exclude?.length && url.searchParams.set('exclude', exclude.join(','));
	locations?.length && url.searchParams.set('locations', locations.join(','));

	try {
		const response = await fetch(url, {
			method: 'GET',
			headers: {
				'x-api-key': 'S2XQnXqY5mDxidA3nnS71TgFl4s2KGX45t6Cwh1b'
			}
		});
		const data = await response.json();
		return data;
	} catch (err) {
		console.error(err);
		return { info: [] };
	}
}
