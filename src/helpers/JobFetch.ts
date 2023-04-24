import type { JobItemProps } from '../types';

interface FetchResponse {
	data: JobItemProps[];
}

export default async function JobFetch({
	lastEvalKey,
	search,
	exclude
}: {
	lastEvalKey?: string;
	search?: string;
	exclude?: string[];
}): Promise<FetchResponse> {
	let url = '/api';

	const queryParams: string[] = [];

	search && search != '' && queryParams.push(`search=${encodeURIComponent(search)}`);
	exclude &&
		exclude.toString() != '' &&
		queryParams.push(`exclude=${encodeURIComponent(exclude.join(','))}`);
	lastEvalKey && queryParams.push(`lastEvalKey=${encodeURIComponent(lastEvalKey)}`);

	if (queryParams.length > 0) {
		url = url.concat(`?${queryParams.join('&')}`);
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
