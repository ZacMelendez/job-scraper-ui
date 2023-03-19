export interface JobItemProps {
	company: string;
	job_id: string;
	title: string;
	url: string;
}

export interface JobSearchProps {
	must: string[];
	include: string[];
	exclude: string[];
}
