import type { JobItemProps } from '../types';

interface FetchResponse {
	data: JobItemProps[];
}

export default async function JobFetch({
	lastEvalKey,
	search
}: {
	lastEvalKey?: string;
	search?: string;
}): Promise<FetchResponse> {
	let url = '/api';

	if (lastEvalKey || search) {
		url = url.concat('?');
		url = lastEvalKey ? url.concat(`lastEvalKey=${lastEvalKey}`) : url;
		url = search ? url.concat(`search=${search}`) : url;
	}
	try {
		const response = await fetch(url, {
			method: 'GET'
		});
		const data = await response.json();

		return data;
	} catch (err) {
		console.error(err);
		return { data: [] };
	}
}
