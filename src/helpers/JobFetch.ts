import type { JobItemProps } from '../types';

interface FetchResponse {
	data: JobItemProps[];
}

export default async function JobFetch({
	lastEvalKey,
	include,
	exclude,
	companies
}: {
	lastEvalKey?: string;
	include?: string[];
	exclude?: string[];
	companies?: string[];
}): Promise<FetchResponse> {
	let url = '/api';

	const queryParams: string[] = [];

	include &&
		include.toString() != '' &&
		queryParams.push(`include=${encodeURIComponent(include.join(','))}`);
	exclude &&
		exclude.toString() != '' &&
		queryParams.push(`exclude=${encodeURIComponent(exclude.join(','))}`);
	companies &&
		companies.toString() != '' &&
		queryParams.push(`companies=${encodeURIComponent(companies.join(','))}`);
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
